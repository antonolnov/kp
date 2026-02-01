"""
Генерация HTML коммерческого предложения через GPT-4o
GPT работает как дизайнер — сам решает структуру и наполнение
"""
import logging
import random
from pathlib import Path

from openai import OpenAI
from weasyprint import HTML

from config import OPENAI_API_KEY, ASSETS_DIR

logger = logging.getLogger(__name__)


# CSS стили для документа
CSS_STYLES = """
@page {
    size: A4;
    margin: 20px 25px 25px 25px;
    @bottom-right {
        content: "Страница " counter(page);
        font-size: 8pt;
        color: #999;
    }
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: Arial, Helvetica, sans-serif;
    color: #1a1a2e;
    background: #fff;
    font-size: 10pt;
    line-height: 1.5;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    margin-bottom: 15px;
    border-bottom: 3px solid #597FFF;
}
.header img { height: 32px; }
.header-right { text-align: right; font-size: 9pt; color: #666; }
.header-right strong { color: #1a1a2e; font-size: 11pt; }

.title {
    text-align: center;
    margin-bottom: 20px;
    padding: 15px;
    background: #597FFF;
    border-radius: 10px;
    color: white;
}
.title h1 { font-size: 18pt; font-weight: bold; margin-bottom: 3px; }
.title p { font-size: 9pt; }

.section { margin-bottom: 18px; page-break-inside: avoid; }
.section-title {
    font-size: 12pt;
    font-weight: bold;
    color: #1a1a2e;
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 2px solid #E2E8F0;
}
.num {
    display: inline-block;
    width: 22px; height: 22px;
    background: #597FFF;
    color: white;
    border-radius: 50%;
    text-align: center;
    line-height: 22px;
    font-size: 11pt;
    font-weight: bold;
    margin-right: 6px;
}

.subsection { 
    font-size: 10pt; 
    font-weight: bold; 
    color: #597FFF; 
    margin: 10px 0 5px 0;
    padding-left: 8px;
    border-left: 3px solid #597FFF;
}

ul { list-style: none; margin: 0; padding: 0; }
ul li { padding: 4px 0 4px 16px; position: relative; font-size: 10pt; }
ul li::before {
    content: '→';
    position: absolute;
    left: 0;
    color: #597FFF;
    font-weight: bold;
}
ul.check li::before { content: '✓'; color: #10B981; }

.box {
    background: #F0F4FF;
    border-left: 4px solid #597FFF;
    padding: 10px 12px;
    margin: 10px 0;
    border-radius: 0 6px 6px 0;
    font-size: 10pt;
}

.box-green {
    background: #ECFDF5;
    border-left: 4px solid #10B981;
    padding: 10px 12px;
    margin: 10px 0;
    border-radius: 0 6px 6px 0;
}
.box-green strong { color: #059669; }

.key-message {
    background: #597FFF;
    color: white;
    padding: 12px 15px;
    margin: 12px 0;
    border-radius: 8px;
    text-align: center;
    font-size: 10pt;
}

.price-table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
}
.price-table th, .price-table td {
    padding: 8px 10px;
    text-align: left;
    border-bottom: 1px solid #E2E8F0;
    font-size: 10pt;
}
.price-table th { background: #597FFF; color: white; font-size: 9pt; }
.price-table td:last-child { text-align: right; font-weight: bold; color: #597FFF; }

.price-total {
    background: #597FFF;
    color: white;
    padding: 10px 15px;
    border-radius: 6px;
    margin-top: 10px;
    text-align: center;
}
.price-total-label { font-size: 9pt; }
.price-total-value { font-size: 14pt; font-weight: bold; }

.steps {
    display: flex;
    gap: 8px;
    margin: 10px 0;
}
.step {
    flex: 1;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 10px 6px;
    text-align: center;
}
.step-num { font-size: 12pt; font-weight: bold; color: #597FFF; }
.step-title { font-weight: bold; font-size: 9pt; margin: 4px 0 2px 0; }
.step-desc { font-size: 8pt; color: #666; }

.columns {
    display: flex;
    gap: 12px;
    margin: 10px 0;
}
.column {
    flex: 1;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 12px;
}
.column-title { font-weight: bold; font-size: 9pt; margin-bottom: 8px; color: #597FFF; }
.column ul li { padding: 6px 0 6px 16px; font-size: 9pt; }

.mascot {
    text-align: center;
    margin: 15px 0;
}
.mascot img { height: 100px; vertical-align: middle; }
.speech-bubble {
    display: inline-block;
    background: #F0F4FF;
    border: 2px solid #597FFF;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 9pt;
    margin: 0 10px;
    vertical-align: middle;
    max-width: 180px;
}
"""


# Промпт для генерации HTML
GENERATION_PROMPT = """Ты — опытный B2B копирайтер. Создай ДЕТАЛЬНОЕ коммерческое предложение на основе транскрибации встречи.

## ЭТАЛОН КП (следуй этому стилю!)

### Раздел 1. Что обсуждали на встрече
Должен содержать 5-7 КОНКРЕТНЫХ пунктов со встречи:
• Роли пользователей: рекрутеры работают в системе ежедневно, руководители выступают заказчиками и могут оставлять комментарии/менять статусы.
• Инструменты внутри карточек: комментарии, напоминания, история изменений, вложения.
• Интеграции с работными сайтами и коммуникации с кандидатами (мессенджеры, шаблоны).
• Отчетность и выгрузки (в том числе в Excel).
• Запрос согласия на обработку персональных данных (152-ФЗ).

### Раздел 2. Предлагаемое решение WorkHere (ДЕТАЛЬНО!)
Разбей на подразделы 2.1, 2.2, 2.3 и т.д. Каждый подраздел — отдельная тема:

**2.1. Базовый функционал ATS/CRM**
• Комментарии и внутренний «диалог» внутри карточек (рекрутер ↔ заказчик), история изменений, вложения.
• Напоминания и ежедневник: постановка задач/напоминаний по кандидатам и заявкам.
• Настраиваемые статусы и несколько воронок (например: линейный персонал и топ-менеджмент).
• Аналитика и отчеты по движению кандидатов, причинам отказов, источникам и др., с выгрузкой в Excel.

**2.2. Заявки и согласование**
Модуль «Заявки» добавляется по запросу (без доплаты) и позволяет вести карточку заявки на подбор: статусы, сроки, документы, согласующие лица.

**2.3. Уведомления и Telegram-бот**
• Уведомления на события (например, смена статуса) с доставкой в Telegram и/или на почту.
• Telegram-бот: напоминания за 15 минут до собеседования и доступ к расписанию.

**2.4. Интеграции и коммуникации**
• Интеграции с работными сайтами: Avito, HeadHunter, SuperJob, Rabota.ru.
• Коммуникации с кандидатами через мессенджеры (Telegram, WhatsApp) с использованием шаблонов.

И т.д. — добавляй подразделы по темам, которые обсуждались на встрече!

## ФУНКЦИОНАЛ WORKHERE (используй при написании раздела 2)

- Единая база кандидатов с историей
- Интеграции: HH.ru, Авито, SuperJob, Rabota.ru
- Мессенджеры: Telegram, WhatsApp, Viber + шаблоны
- Настраиваемые воронки и статусы
- Аналитика и отчёты с выгрузкой в Excel
- Telegram-бот: уведомления, расписание, импорт резюме
- Модуль заявок и согласований
- Запрос согласия 152-ФЗ
- Мобильное приложение iOS/Android
- Открытый API
- AI-поиск кандидатов (Премиум)

## ТАРИФЫ

- Стандартный: 20 000 ₽/лицензия/год
- Премиум (с AI): 42 000 ₽/лицензия/год
- Руководители: бесплатно

## СТРУКТУРА КП

1. **Что обсуждали на встрече** — 5-7 конкретных пунктов из транскрибации
2. **Предлагаемое решение WorkHere** — подразделы 2.1, 2.2, 2.3... с детальным описанием
3. **Коммерческие условия** — таблица с ценами (без суммирования!)
4. **Внедрение и запуск** — 5-6 шагов
5. **Следующие шаги** — что делать дальше

## ПРАВИЛА

1. Документ 2-3 страницы A4
2. Маскот ТОЛЬКО ОДИН раз в самом конце документа
3. Раздел 2 должен быть ДЕТАЛЬНЫМ с подразделами 2.1, 2.2, 2.3...
4. Каждый пункт — полное предложение, не обрывки
5. Привязывай функции к потребностям клиента из транскрибации

## ПРАВИЛА ДЛЯ ЦЕНЫ (ВАЖНО!)

- НЕ суммировать тарифы! Клиент сам посчитает
- Показывать ТОЛЬКО цену за 1 лицензию в год
- Таблица: Тариф | Цена за лицензию
- Стандартный: 20 000 ₽/год
- Премиум (с AI): 42 000 ₽/год  
- Руководители: бесплатно
- ЗАПРЕЩЕНО: колонка "Количество", колонка "Итого", блок с общей суммой

## ПРАВИЛА ДЛЯ НАЗВАНИЯ КОМПАНИИ (ВАЖНО!)

- Если в транскрибации есть ЧЁТКОЕ название — используй
- Если названия НЕТ — НЕ выдумывай! Не пиши "ООО Клиент"
- В шапке справа: пусто если названия нет
- В тексте: "ваша компания", "вашей команде" вместо выдуманного названия

## CSS СТИЛИ (используй эти классы)

{css_styles}

## МАСКОТ (ТОЛЬКО ОДИН, ТОЛЬКО В КОНЦЕ!)

СТРОГОЕ ПРАВИЛО: Маскот размещается ТОЛЬКО ОДИН РАЗ — после раздела 6 "Следующие шаги", перед призывом к действию. 
ЗАПРЕЩЕНО вставлять маскотов между разделами 1-6!

Путь к изображению: {mascot_paths}

Фраза для маскота (выбери одну):
- "Меньше рутины, больше результата!"
- "Рекрутинг может быть простым!"

## ДАННЫЕ КЛИЕНТА

Тариф: {tariff}
Количество рекрутеров: {num_recruiters}

## ТРАНСКРИБАЦИЯ ВСТРЕЧИ

{transcript}

---

Сгенерируй ПОЛНЫЙ HTML-документ. Начни с <!DOCTYPE html> и закончи </html>.

Включи:
- <style> с CSS внутри <head>
- Логотип в header: <img src="{logo_path}">
- Все 6 разделов
- 2-3 маскота между разделами
- Персонализированный контент на основе транскрибации

ВАЖНО: Возвращай ТОЛЬКО HTML, без ```html``` обёртки."""


def get_mascot_paths() -> list[str]:
    """Получить пути к маскотам"""
    mascots_dir = ASSETS_DIR / "mascots"
    if mascots_dir.exists():
        mascots = list(mascots_dir.glob("*.svg")) + list(mascots_dir.glob("*.png"))
        if mascots:
            return [str(m) for m in mascots[:5]]
    return []


async def generate_html_proposal(
    transcript: str,
    tariff: str,
    num_recruiters: int,
    output_path: Path
) -> Path:
    """
    Генерация КП через GPT-4o.
    GPT сам создаёт HTML, выступая как дизайнер.
    """
    
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Подготовка данных
    logo_path = str(ASSETS_DIR / "logo.png")
    mascot_paths = get_mascot_paths()
    mascot_paths_str = "\n".join(f"- {p}" for p in mascot_paths) or "- (нет маскотов)"
    
    tariff_label = {
        "standard": "Стандартный (20 000 ₽/год)",
        "premium": "Премиум (42 000 ₽/год)",
        "both": "Оба варианта"
    }.get(tariff, "Стандартный")
    
    # Обрезаем транскрибацию если слишком длинная
    if len(transcript) > 20000:
        transcript = transcript[:20000] + "\n\n[...обрезано...]"
    
    prompt = GENERATION_PROMPT.format(
        css_styles=CSS_STYLES,
        mascot_paths=mascot_paths_str,
        tariff=tariff_label,
        num_recruiters=num_recruiters,
        transcript=transcript,
        logo_path=logo_path
    )
    
    logger.info(f"Generating HTML proposal via gpt-4.1 ({len(transcript)} chars transcript)...")
    
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "Ты — дизайнер коммерческих предложений. Генерируй качественный HTML. Отвечай ТОЛЬКО HTML-кодом."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        max_tokens=16000,
        temperature=0.7
    )
    
    html_content = response.choices[0].message.content.strip()
    
    # Очистка от markdown если есть
    if html_content.startswith("```html"):
        html_content = html_content[7:]
    if html_content.startswith("```"):
        html_content = html_content[3:]
    if html_content.endswith("```"):
        html_content = html_content[:-3]
    html_content = html_content.strip()
    
    logger.info(f"Generated HTML: {len(html_content)} chars")
    
    # Генерируем PDF
    html = HTML(string=html_content, base_url=str(ASSETS_DIR))
    html.write_pdf(str(output_path))
    
    logger.info(f"PDF generated: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    
    return output_path
