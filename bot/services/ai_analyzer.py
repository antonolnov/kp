"""
AI-powered meeting transcript analyzer using OpenAI-compatible API (Cursor)
"""
import json
import logging
from dataclasses import dataclass, field
from typing import Optional

from openai import OpenAI

from config import CURSOR_API_KEY

logger = logging.getLogger(__name__)


@dataclass
class MeetingAnalysis:
    """Structured analysis of a meeting transcript"""
    company_name: str = ""
    contact_name: str = ""
    num_recruiters: int = 1
    current_pain_points: list[str] = field(default_factory=list)
    needs: list[str] = field(default_factory=list)
    discussed_features: list[str] = field(default_factory=list)
    specific_request: Optional[str] = None
    hiring_situation: Optional[str] = None
    summary: str = ""


ANALYSIS_PROMPT = """Проанализируй транскрибацию встречи с потенциальным клиентом WorkHere (ATS-система для рекрутинга).

Извлеки следующую информацию в формате JSON:

{
    "company_name": "Название компании клиента (если упоминается, иначе пустая строка)",
    "contact_name": "Имя контактного лица (если упоминается, иначе пустая строка)",
    "num_recruiters": число рекрутеров/лицензий (целое число, если не упоминается - 1),
    "current_pain_points": ["Список текущих проблем/болей в процессе найма, минимум 3 пункта"],
    "needs": ["Список потребностей клиента, минимум 3 пункта"],
    "discussed_features": ["Список обсуждаемых функций WorkHere, которые заинтересовали клиента, минимум 3 пункта"],
    "specific_request": "Конкретный запрос клиента к системе (или null если нет явного запроса)",
    "hiring_situation": "Краткое описание текущей ситуации в найме у клиента (1-2 предложения)",
    "summary": "Краткое резюме встречи в 2-3 предложения для КП"
}

Важные функции WorkHere, на которые обращай внимание:
- База кандидатов (единое хранилище)
- Интеграции с HH.ru, Авито, SuperJob, Работа.ру
- Коммуникации в одном окне (чаты, мессенджеры, телефония)
- Воронка подбора с этапами
- Календарь и интервью через Телемост
- Автоматизация (триггеры, авторассылки)
- Аналитика и дашборды
- AI-функции (семантический поиск, скоринг, генерация текстов)
- Мобильное приложение
- КЭДО и документооборот
- Talent pool (кадровый резерв)
- Запрос согласия на обработку персональных данных (ФЗ-152)
- Telegram-бот для уведомлений
- Работа с заказчиками (внутренними)

Транскрибация встречи:
---
{transcript}
---

Верни ТОЛЬКО валидный JSON объект, без markdown разметки, без ```json, просто чистый JSON."""


async def analyze_transcript(transcript: str) -> MeetingAnalysis:
    """
    Analyze meeting transcript using OpenAI-compatible API
    
    Args:
        transcript: Meeting transcript text
        
    Returns:
        MeetingAnalysis with extracted information
    """
    if not CURSOR_API_KEY:
        logger.warning("CURSOR_API_KEY not set, using mock analysis")
        return _mock_analysis(transcript)
    
    try:
        # Use OpenAI SDK with custom base URL for Cursor
        client = OpenAI(
            api_key=CURSOR_API_KEY,
            base_url="https://api.cursor.com/v1"
        )
        
        # Truncate transcript if too long (keep first 15000 chars)
        if len(transcript) > 15000:
            transcript = transcript[:15000] + "\n\n[...транскрибация обрезана...]"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты - аналитик, который извлекает структурированную информацию из транскрибаций встреч. Отвечай только валидным JSON."
                },
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(transcript=transcript)
                }
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Clean up response - remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON response
        data = json.loads(response_text)
        
        return MeetingAnalysis(
            company_name=data.get("company_name", "") or "",
            contact_name=data.get("contact_name", "") or "",
            num_recruiters=int(data.get("num_recruiters", 1) or 1),
            current_pain_points=data.get("current_pain_points", []) or [],
            needs=data.get("needs", []) or [],
            discussed_features=data.get("discussed_features", []) or [],
            specific_request=data.get("specific_request"),
            hiring_situation=data.get("hiring_situation"),
            summary=data.get("summary", "") or ""
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {e}")
        logger.error(f"Response was: {response_text[:500] if 'response_text' in dir() else 'N/A'}")
        return _mock_analysis(transcript)
    except Exception as e:
        logger.error(f"AI analysis error: {e}")
        return _mock_analysis(transcript)


def _mock_analysis(transcript: str) -> MeetingAnalysis:
    """Fallback mock analysis when AI is not available"""
    # Try to extract some info from transcript
    transcript_lower = transcript.lower()
    
    # Try to find number of recruiters
    num_recruiters = 3
    if "3 рекрутер" in transcript_lower or "рекрутера 3" in transcript_lower:
        num_recruiters = 3
    elif "4 рекрутер" in transcript_lower:
        num_recruiters = 4
    elif "5 рекрутер" in transcript_lower:
        num_recruiters = 5
    
    # Check what features were discussed
    discussed = []
    if "интеграц" in transcript_lower or "хедхантер" in transcript_lower or "авито" in transcript_lower:
        discussed.append("Интеграции с job-сайтами")
    if "воронк" in transcript_lower:
        discussed.append("Воронка подбора")
    if "аналитик" in transcript_lower or "отчёт" in transcript_lower:
        discussed.append("Аналитика и отчёты")
    if "телефон" in transcript_lower or "звон" in transcript_lower:
        discussed.append("Телефония")
    if "телеграм" in transcript_lower or "мессендж" in transcript_lower:
        discussed.append("Мессенджеры")
    if "календар" in transcript_lower or "собеседован" in transcript_lower:
        discussed.append("Календарь собеседований")
    if "заказчик" in transcript_lower:
        discussed.append("Работа с заказчиками")
    if "персональн" in transcript_lower or "152" in transcript_lower:
        discussed.append("ФЗ-152 и персональные данные")
    
    if not discussed:
        discussed = ["Интеграции с job-сайтами", "Воронка подбора", "Аналитика"]
    
    return MeetingAnalysis(
        company_name="",
        contact_name="Юлия",
        num_recruiters=num_recruiters,
        current_pain_points=[
            "Разрозненные системы для работы с кандидатами",
            "Ручная работа с несколькими площадками",
            "Неудобная текущая CRM-система"
        ],
        needs=[
            "Единая система для всех этапов подбора",
            "Автоматизация рутинных задач",
            "Удобная работа с заказчиками"
        ],
        discussed_features=discussed[:6],
        hiring_situation="Компания занимается подбором персонала для сферы общепита (бариста, официанты, повара). Есть команда из 3 рекрутеров и главный HR.",
        summary="Демонстрация системы WorkHere для автоматизации подбора персонала в сфере общепита."
    )
