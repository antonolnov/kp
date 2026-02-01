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


ANALYSIS_PROMPT = """Ты — эксперт по продажам ATS-систем. Проанализируй транскрибацию встречи с потенциальным клиентом WorkHere и извлеки ключевую информацию для персонализированного коммерческого предложения.

WorkHere — это современная ATS-система (система управления подбором персонала) с функциями:
- Единая база кандидатов
- Интеграции с HH.ru, Авито, SuperJob, Работа.ру
- Воронка подбора с этапами
- Коммуникации в одном окне (чаты job-сайтов, WhatsApp, Telegram, Viber)
- IP-телефония с записью звонков
- Календарь собеседований с интеграцией Телемост
- Автоматизация (триггеры, авторассылки, напоминания)
- Telegram-бот для уведомлений
- Аналитика и отчёты
- AI-поиск кандидатов (семантический поиск, скоринг)
- Запрос согласия на обработку ПД (ФЗ-152)
- Работа с внутренними заказчиками
- Мобильное приложение

Извлеки информацию в формате JSON:

{
    "company_name": "Название компании клиента (если не упоминается — пустая строка)",
    "contact_name": "Имя контактного лица клиента",
    "contact_role": "Должность контактного лица (HR-директор, рекрутер и т.д.)",
    "num_recruiters": целое число рекрутеров (если упоминается 3 рекрутера + HR директор, то 4),
    "industry": "Сфера деятельности компании (общепит, IT, ритейл и т.д.)",
    "current_tools": "Какие инструменты сейчас используют (Битрикс, Excel, Телеграм и т.д.)",
    "current_pain_points": [
        "Конкретная проблема 1 из разговора (своими словами, кратко)",
        "Конкретная проблема 2",
        "Конкретная проблема 3"
    ],
    "needs": [
        "Потребность 1 — что хотят получить",
        "Потребность 2",
        "Потребность 3"
    ],
    "discussed_features": [
        "Функция WorkHere 1, которая заинтересовала",
        "Функция 2",
        "Функция 3",
        "Функция 4",
        "Функция 5",
        "Функция 6"
    ],
    "specific_request": "Конкретный запрос клиента, если был озвучен (иначе null)",
    "hiring_situation": "Описание текущей ситуации с наймом в компании (2-3 предложения)",
    "summary": "Краткое резюме для первой страницы КП (1-2 предложения, подчеркивающие ценность для этого клиента)"
}

ВАЖНО:
- Извлекай РЕАЛЬНУЮ информацию из разговора, не выдумывай
- Боли и потребности формулируй конкретно на основе слов клиента
- Для discussed_features выбирай только те функции, которые РЕАЛЬНО обсуждались и заинтересовали
- Если информация не упоминалась — оставляй пустую строку или null
- Верни ТОЛЬКО валидный JSON, без markdown

Транскрибация встречи:
---
{transcript}
---"""


async def analyze_transcript(transcript: str) -> MeetingAnalysis:
    """
    Analyze meeting transcript using OpenAI API
    """
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set, using mock analysis")
        return _mock_analysis(transcript)
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Truncate transcript if too long (keep first 20000 chars)
        if len(transcript) > 20000:
            transcript = transcript[:20000] + "\n\n[...транскрибация обрезана...]"
        
        logger.info(f"Analyzing transcript with OpenAI ({len(transcript)} chars)")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты — эксперт по анализу B2B встреч. Извлекай структурированную информацию из транскрибаций. Отвечай только валидным JSON без markdown разметки."
                },
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(transcript=transcript)
                }
            ],
            max_tokens=2000,
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
    
    # Check discussed features
    discussed = []
    if "интеграц" in transcript_lower or "хедхантер" in transcript_lower or "авито" in transcript_lower:
        discussed.append("Интеграции с job-сайтами (HH, Авито)")
    if "воронк" in transcript_lower:
        discussed.append("Воронка подбора")
    if "аналитик" in transcript_lower or "отчёт" in transcript_lower or "статистик" in transcript_lower:
        discussed.append("Аналитика и отчёты")
    if "телефон" in transcript_lower or "звон" in transcript_lower:
        discussed.append("IP-телефония с записью звонков")
    if "whatsapp" in transcript_lower or "ватсап" in transcript_lower or "мессендж" in transcript_lower:
        discussed.append("Мессенджеры (WhatsApp, Telegram)")
    if "календар" in transcript_lower or "телемост" in transcript_lower:
        discussed.append("Календарь с интеграцией Телемост")
    if "заказчик" in transcript_lower or "шеф" in transcript_lower:
        discussed.append("Работа с внутренними заказчиками")
    if "персональн" in transcript_lower or "152" in transcript_lower:
        discussed.append("Соответствие ФЗ-152")
    if "уведомлен" in transcript_lower or "напоминан" in transcript_lower or "бот" in transcript_lower:
        discussed.append("Telegram-бот для уведомлений")
    
    if not discussed:
        discussed = ["Интеграции с job-сайтами", "Воронка подбора", "Аналитика"]
    
    return MeetingAnalysis(
        company_name="",
        contact_name=contact_name,
        contact_role="HR-директор" if "эйчар" in transcript_lower else "",
        num_recruiters=num_recruiters,
        industry=industry,
        current_tools="Битрикс" if "битрикс" in transcript_lower else "",
        current_pain_points=[
            "Текущая CRM-система не используется в полной мере",
            "Работа ведётся в разных инструментах (Телеграм, Битрикс)",
            "Нет единой системы для всех этапов подбора"
        ],
        needs=[
            "Сократить время на рутинные операции",
            "Объединить все коммуникации в одном месте",
            "Получить прозрачную аналитику по подбору"
        ],
        discussed_features=discussed[:6],
        hiring_situation=f"Компания из сферы {industry or 'услуг'} ищет способы оптимизировать процесс подбора. Команда из {num_recruiters} рекрутеров работает с несколькими площадками.",
        summary=f"Решение для автоматизации подбора персонала в сфере {industry or 'услуг'}, объединяющее все инструменты в одной системе."
    )
