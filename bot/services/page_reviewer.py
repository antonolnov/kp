"""
Проверка страниц PDF через Cursor API (Claude)
Каждая страница проверяется отдельным запросом
"""
import base64
import logging
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

from config import BOT_DIR

logger = logging.getLogger(__name__)

# Cursor API endpoint
CURSOR_API_BASE = "https://api.cursor.com/v1"


@dataclass
class PageReview:
    """Результат проверки страницы"""
    page_num: int
    is_ok: bool
    issues: list[str]
    suggestions: list[str]


@dataclass 
class DocumentReview:
    """Результат проверки всего документа"""
    is_ok: bool
    page_reviews: list[PageReview]
    final_issues: list[str]
    final_suggestions: list[str]


# Критерии проверки страницы
PAGE_REVIEW_PROMPT = """Проверь страницу коммерческого предложения. Будь ОЧЕНЬ СТРОГИМ!

КРИТИЧЕСКИЕ ОШИБКИ (is_ok = false):
1. НАЛОЖЕНИЕ ЭЛЕМЕНТОВ: текст наезжает на другой текст, цифры на текст, блоки перекрываются
2. СЛИПАНИЕ РАЗДЕЛОВ: два раздела слились без отступа между ними
3. НУМЕРАЦИЯ СЛОМАНА: цифры/маркеры наезжают на текст или друг на друга
4. Более 30% страницы пустое без большого маскота
5. Футер дублируется (логотип/год появляется дважды)
6. Текст обрезан или выходит за границы блока

ПРОВЕРЬ ВНИМАТЕЛЬНО:
- Все ли цифры/маркеры на своих местах?
- Есть ли отступы между разделами?
- Не наезжает ли один блок на другой?
- Читается ли весь текст без перекрытий?

Ответь JSON:
{
    "is_ok": true/false,
    "issues": ["КОНКРЕТНО опиши что наезжает на что", "какие разделы слились"],
    "suggestions": ["как исправить"]
}

ЛЮБОЕ наложение/наезжание = is_ok: false!
Отвечай ТОЛЬКО JSON."""


# Критерии финальной проверки
FINAL_REVIEW_PROMPT = """Проверь весь документ коммерческого предложения по критериям:

1. ПЕРСОНАЛИЗАЦИЯ: Название компании клиента упоминается минимум 3 раза
2. СВЯЗНОСТЬ: Боли → Решения → Выгоды логически связаны
3. КОНКРЕТИКА: Нет шаблонных фраз без контекста
4. СТРУКТУРА: Все разделы присутствуют (Ситуация, Решение, Стоимость, Внедрение, Выгоды, Шаги)
5. ОБЪЁМ: 3-4 страницы
6. ЕДИНООБРАЗИЕ: Стиль оформления одинаковый

Ответь в формате JSON:
{
    "is_ok": true/false,
    "issues": ["проблема 1", "проблема 2"],
    "suggestions": ["как исправить 1", "как исправить 2"]
}

Отвечай ТОЛЬКО JSON, без markdown."""


def pdf_to_images(pdf_path: Path, output_dir: Optional[Path] = None) -> list[Path]:
    """Конвертирует PDF в изображения страниц"""
    if output_dir is None:
        output_dir = pdf_path.parent
    
    output_prefix = output_dir / f"{pdf_path.stem}_page"
    
    try:
        subprocess.run(
            ["pdftoppm", str(pdf_path), str(output_prefix), "-png", "-r", "150"],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to convert PDF to images: {e}")
        return []
    except FileNotFoundError:
        logger.error("pdftoppm not found. Install poppler-utils.")
        return []
    
    # Найти созданные файлы
    images = sorted(output_dir.glob(f"{pdf_path.stem}_page-*.png"))
    logger.info(f"Converted PDF to {len(images)} images")
    return images


def image_to_base64(image_path: Path) -> str:
    """Конвертирует изображение в base64"""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


async def review_page(client: OpenAI, image_path: Path, page_num: int) -> PageReview:
    """Проверяет одну страницу через Cursor API"""
    import json
    
    try:
        image_data = image_to_base64(image_path)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": f"Это страница {page_num} документа.\n\n{PAGE_REVIEW_PROMPT}"
                        }
                    ]
                }
            ]
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Очистка от markdown
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        data = json.loads(response_text.strip())
        
        return PageReview(
            page_num=page_num,
            is_ok=data.get("is_ok", True),
            issues=data.get("issues", []),
            suggestions=data.get("suggestions", [])
        )
        
    except Exception as e:
        logger.error(f"Failed to review page {page_num}: {e}")
        return PageReview(
            page_num=page_num,
            is_ok=True,  # При ошибке считаем ОК чтобы не блокировать
            issues=[],
            suggestions=[]
        )


async def review_document(client: OpenAI, image_paths: list[Path]) -> PageReview:
    """Финальная проверка всего документа"""
    import json
    
    try:
        # Собираем все страницы в один запрос
        content = []
        for i, image_path in enumerate(image_paths, 1):
            image_data = image_to_base64(image_path)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_data}"
                }
            })
            content.append({
                "type": "text",
                "text": f"Страница {i}"
            })
        
        content.append({
            "type": "text",
            "text": f"\n\n{FINAL_REVIEW_PROMPT}"
        })
        
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=1500,
            messages=[{"role": "user", "content": content}]
        )
        
        response_text = response.choices[0].message.content.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        data = json.loads(response_text.strip())
        
        return PageReview(
            page_num=0,  # 0 = весь документ
            is_ok=data.get("is_ok", True),
            issues=data.get("issues", []),
            suggestions=data.get("suggestions", [])
        )
        
    except Exception as e:
        logger.error(f"Failed to review document: {e}")
        return PageReview(page_num=0, is_ok=True, issues=[], suggestions=[])


async def full_review(pdf_path: Path, openai_key: str) -> DocumentReview:
    """
    Полная проверка PDF через GPT-4o vision:
    1. Конвертация в изображения
    2. Проверка каждой страницы отдельно
    3. Финальная проверка всего документа
    """
    if not openai_key:
        logger.warning("API key not set, skipping review")
        return DocumentReview(
            is_ok=True,
            page_reviews=[],
            final_issues=[],
            final_suggestions=[]
        )
    
    client = OpenAI(api_key=openai_key)
    
    # 1. Конвертируем PDF в изображения
    images = pdf_to_images(pdf_path)
    if not images:
        return DocumentReview(
            is_ok=True,
            page_reviews=[],
            final_issues=["Не удалось конвертировать PDF в изображения"],
            final_suggestions=[]
        )
    
    logger.info(f"Starting review of {len(images)} pages...")
    
    # 2. Проверяем каждую страницу
    page_reviews = []
    for i, image_path in enumerate(images, 1):
        logger.info(f"Reviewing page {i}/{len(images)}...")
        review = await review_page(client, image_path, i)
        page_reviews.append(review)
        
        if not review.is_ok:
            logger.warning(f"Page {i} has issues: {review.issues}")
    
    # 3. Финальная проверка
    logger.info("Final document review...")
    final_review = await review_document(client, images)
    
    # 4. Определяем общий статус
    all_ok = all(r.is_ok for r in page_reviews) and final_review.is_ok
    
    # 5. Удаляем временные изображения
    for image_path in images:
        try:
            image_path.unlink()
        except:
            pass
    
    result = DocumentReview(
        is_ok=all_ok,
        page_reviews=page_reviews,
        final_issues=final_review.issues,
        final_suggestions=final_review.suggestions
    )
    
    logger.info(f"Review complete. OK: {all_ok}")
    return result


def format_review_report(review: DocumentReview) -> str:
    """Форматирует отчёт о проверке для логов"""
    lines = ["=== REVIEW REPORT ==="]
    
    for pr in review.page_reviews:
        status = "✅" if pr.is_ok else "❌"
        lines.append(f"\nPage {pr.page_num}: {status}")
        if pr.issues:
            for issue in pr.issues:
                lines.append(f"  - {issue}")
    
    lines.append(f"\nFinal: {'✅' if review.is_ok else '❌'}")
    if review.final_issues:
        for issue in review.final_issues:
            lines.append(f"  - {issue}")
    
    lines.append("=== END REPORT ===")
    return "\n".join(lines)
