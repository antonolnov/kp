"""
AI-powered meeting transcript analyzer using OpenAI API
"""
import json
import logging
from dataclasses import dataclass, field
from typing import Optional

from openai import OpenAI

from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)


@dataclass
class MeetingAnalysis:
    """Structured analysis of a meeting transcript"""
    company_name: str = ""
    contact_name: str = ""
    contact_role: str = ""
    num_recruiters: int = 1
    current_pain_points: list[str] = field(default_factory=list)
    needs: list[str] = field(default_factory=list)
    discussed_features: list[str] = field(default_factory=list)
    specific_request: Optional[str] = None
    hiring_situation: Optional[str] = None
    industry: str = ""
    current_tools: str = ""
    summary: str = ""


ANALYSIS_PROMPT = """Проанализируй транскрибацию встречи с клиентом по продукту WorkHere (ATS-система).

Твоя задача — извлечь информацию для раздела "Что обсуждали на встрече" в коммерческом предложении.

Пример хорошего формата для discussed_features:
- "Роли пользователей: рекрутеры работают в системе ежедневно, руководители выступают заказчиками и могут оставлять комментарии/менять статусы"
- "Интеграции с работными сайтами HH.ru и Авито для автоматического сбора откликов"
- "Инструменты внутри карточек: комментарии, напоминания, история изменений, вложения"
- "Коммуникации с кандидатами через мессенджеры (Telegram, WhatsApp) с шаблонами сообщений"
- "Отчётность и выгрузки данных в Excel"
- "Запрос согласия на обработку персональных данных (152-ФЗ)"
- "Уведомления и Telegram-бот: напоминания о собеседованиях, расписание"

Верни JSON:

{
    "company_name": "Название компании",
    "contact_name": "Имя контактного лица",
    "contact_role": "Должность",
    "num_recruiters": число_рекрутеров,
    "industry": "Сфера деятельности",
    "current_tools": "Текущие инструменты",
    "hiring_situation": "Описание ситуации с наймом — 2-3 предложения",
    "discussed_features": [
        "Развёрнутый пункт 1 — что именно обсуждали, с деталями",
        "Развёрнутый пункт 2",
        "Развёрнутый пункт 3",
        "Развёрнутый пункт 4",
        "Развёрнутый пункт 5",
        "Развёрнутый пункт 6",
        "Развёрнутый пункт 7",
        "Развёрнутый пункт 8"
    ],
    "current_pain_points": [
        "Проблема 1 — конкретно из слов клиента",
        "Проблема 2",
        "Проблема 3"
    ],
    "needs": [
        "Потребность 1",
        "Потребность 2",
        "Потребность 3"
    ],
    "summary": "Краткое резюме"
}

КРИТИЧЕСКИ ВАЖНО для discussed_features:
1. Минимум 6-8 пунктов
2. Каждый пункт — развёрнутое предложение, не 2-3 слова
3. Включай детали из разговора (какие мессенджеры, какие сайты, какие роли)
4. Формат: "Тема: детали и конкретика из разговора"

Транскрибация:
---
{transcript}
---

Верни ТОЛЬКО JSON."""


async def analyze_transcript(transcript: str) -> MeetingAnalysis:
    """
    Analyze meeting transcript using OpenAI API
    """
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set, using mock analysis")
        return _mock_analysis(transcript)
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Truncate transcript if too long (keep first 25000 chars)
        if len(transcript) > 25000:
            transcript = transcript[:25000] + "\n\n[...транскрибация обрезана...]"
        
        logger.info(f"Analyzing transcript with OpenAI ({len(transcript)} chars)")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты — эксперт по B2B продажам. Твоя задача — извлечь максимум конкретной информации из транскрибации для коммерческого предложения. Каждый пункт discussed_features должен быть развёрнутым предложением с деталями. Отвечай только валидным JSON."
                },
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(transcript=transcript)
                }
            ],
            max_tokens=2500,
            temperature=0.2
        )
        
        response_text = response.choices[0].message.content.strip()
        logger.info(f"OpenAI response received ({len(response_text)} chars)")
        
        # Clean up response
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        data = json.loads(response_text)
        
        analysis = MeetingAnalysis(
            company_name=data.get("company_name", "") or "",
            contact_name=data.get("contact_name", "") or "",
            contact_role=data.get("contact_role", "") or "",
            num_recruiters=int(data.get("num_recruiters", 1) or 1),
            industry=data.get("industry", "") or "",
            current_tools=data.get("current_tools", "") or "",
            current_pain_points=data.get("current_pain_points", []) or [],
            needs=data.get("needs", []) or [],
            discussed_features=data.get("discussed_features", []) or [],
            specific_request=data.get("specific_request"),
            hiring_situation=data.get("hiring_situation"),
            summary=data.get("summary", "") or ""
        )
        
        logger.info(f"Analysis complete: {analysis.contact_name}, {analysis.num_recruiters} recruiters, {len(analysis.discussed_features)} features")
        return analysis
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {e}")
        logger.error(f"Response was: {response_text[:500] if 'response_text' in dir() else 'N/A'}")
        return _mock_analysis(transcript)
    except Exception as e:
        logger.error(f"AI analysis error: {e}")
        return _mock_analysis(transcript)


def _mock_analysis(transcript: str) -> MeetingAnalysis:
    """Fallback mock analysis when AI is not available"""
    transcript_lower = transcript.lower()
    
    # Extract contact name
    contact_name = ""
    if "юлия" in transcript_lower or "юля" in transcript_lower:
        contact_name = "Юлия"
    
    # Try to find number of recruiters
    num_recruiters = 3
    if "3 рекрутер" in transcript_lower or "рекрутера 3" in transcript_lower:
        num_recruiters = 3
    if "эйчар" in transcript_lower or "hr" in transcript_lower:
        num_recruiters += 1
    
    # Detect industry
    industry = ""
    if "общепит" in transcript_lower or "официант" in transcript_lower or "бариста" in transcript_lower or "повар" in transcript_lower:
        industry = "Общепит / HoReCa"
    
    # Build detailed discussed features
    discussed = []
    if "интеграц" in transcript_lower or "хедхантер" in transcript_lower or "авито" in transcript_lower or "hh" in transcript_lower:
        discussed.append("Интеграции с работными сайтами: подключение HH.ru, Авито — автоматический сбор откликов в единую систему")
    if "воронк" in transcript_lower or "статус" in transcript_lower:
        discussed.append("Настраиваемые воронки и статусы: возможность создавать несколько воронок под разные типы подбора (массовый, точечный)")
    if "аналитик" in transcript_lower or "отчёт" in transcript_lower or "статистик" in transcript_lower or "excel" in transcript_lower:
        discussed.append("Аналитика и отчёты: конверсии воронки, Time-to-Hire, эффективность источников, выгрузка в Excel")
    if "телефон" in transcript_lower or "звон" in transcript_lower or "телефони" in transcript_lower:
        discussed.append("IP-телефония: звонки из карточки кандидата, запись разговоров, автоматическое создание задач")
    if "whatsapp" in transcript_lower or "ватсап" in transcript_lower or "мессендж" in transcript_lower or "telegram" in transcript_lower:
        discussed.append("Коммуникации через мессенджеры: Telegram, WhatsApp — переписка в карточке кандидата, шаблоны сообщений")
    if "календар" in transcript_lower or "телемост" in transcript_lower or "собеседован" in transcript_lower:
        discussed.append("Календарь собеседований: интеграция с Яндекс Телемост, автоматические приглашения кандидатам")
    if "заказчик" in transcript_lower or "руководител" in transcript_lower or "шеф" in transcript_lower:
        discussed.append("Работа с заказчиками: руководители видят кандидатов, оставляют комментарии и фидбек")
    if "персональн" in transcript_lower or "152" in transcript_lower or "фз" in transcript_lower:
        discussed.append("Соответствие 152-ФЗ: запрос согласия на обработку персональных данных, фиксация статуса в системе")
    if "уведомлен" in transcript_lower or "напоминан" in transcript_lower or "бот" in transcript_lower:
        discussed.append("Telegram-бот: уведомления о новых откликах, напоминания за 15 минут до собеседования, расписание")
    if "коммент" in transcript_lower or "истор" in transcript_lower:
        discussed.append("Инструменты внутри карточек: комментарии, напоминания, история изменений, вложения файлов")
    if "мобильн" in transcript_lower or "приложен" in transcript_lower:
        discussed.append("Мобильное приложение: работа с кандидатами с телефона, push-уведомления")
    if "заявк" in transcript_lower:
        discussed.append("Модуль заявок на подбор: карточка заявки со статусами, сроками, согласующими лицами")
    
    if len(discussed) < 6:
        defaults = [
            "Единая база кандидатов: все контакты, резюме и история взаимодействий в одном месте",
            "Интеграции с работными сайтами: HH.ru, Авито, SuperJob — автоматический сбор откликов",
            "Настраиваемые воронки и статусы под ваши процессы",
            "Аналитика и отчёты: конверсии, источники, Time-to-Hire",
            "Коммуникации с кандидатами через мессенджеры (WhatsApp, Telegram) с шаблонами",
            "Telegram-бот для уведомлений и напоминаний о собеседованиях"
        ]
        for d in defaults:
            if d not in discussed and len(discussed) < 8:
                discussed.append(d)
    
    return MeetingAnalysis(
        company_name="",
        contact_name=contact_name,
        contact_role="HR-директор" if "эйчар" in transcript_lower else "",
        num_recruiters=num_recruiters,
        industry=industry,
        current_tools="Битрикс" if "битрикс" in transcript_lower else "",
        current_pain_points=[
            "Работа ведётся в нескольких инструментах, нет единой системы",
            "Ручной перенос данных между площадками и таблицами",
            "Отсутствие прозрачной аналитики по процессу подбора"
        ],
        needs=[
            "Сократить время на рутинные операции",
            "Объединить все коммуникации и источники кандидатов в одном месте",
            "Получить прозрачную аналитику по эффективности подбора"
        ],
        discussed_features=discussed[:8],
        hiring_situation=f"Компания из сферы {industry or 'услуг'} ищет способы оптимизировать процесс подбора. Команда из {num_recruiters} рекрутеров работает с несколькими площадками и инструментами.",
        summary=f"Решение для автоматизации подбора персонала, объединяющее все инструменты в одной системе."
    )
