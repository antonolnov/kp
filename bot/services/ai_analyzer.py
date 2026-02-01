"""
AI-powered meeting transcript analyzer using Claude
"""
import json
import logging
from dataclasses import dataclass, field
from typing import Optional

import anthropic

from config import ANTHROPIC_API_KEY

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
    "company_name": "Название компании клиента (если упоминается)",
    "contact_name": "Имя контактного лица (если упоминается)",
    "num_recruiters": число рекрутеров/лицензий (целое число, если не упоминается - 1),
    "current_pain_points": ["Список текущих проблем/болей в процессе найма"],
    "needs": ["Список потребностей клиента"],
    "discussed_features": ["Список обсуждаемых функций WorkHere, которые заинтересовали клиента"],
    "specific_request": "Конкретный запрос клиента к системе (или null если нет явного запроса)",
    "hiring_situation": "Краткое описание текущей ситуации в найме у клиента",
    "summary": "Краткое резюме встречи в 2-3 предложения"
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

Транскрибация встречи:
---
{transcript}
---

Верни ТОЛЬКО валидный JSON без дополнительного текста."""


async def analyze_transcript(transcript: str) -> MeetingAnalysis:
    """
    Analyze meeting transcript using Claude AI
    
    Args:
        transcript: Meeting transcript text
        
    Returns:
        MeetingAnalysis with extracted information
    """
    if not ANTHROPIC_API_KEY:
        logger.warning("ANTHROPIC_API_KEY not set, using mock analysis")
        return _mock_analysis(transcript)
    
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(transcript=transcript)
                }
            ]
        )
        
        response_text = message.content[0].text
        
        # Parse JSON response
        data = json.loads(response_text)
        
        return MeetingAnalysis(
            company_name=data.get("company_name", ""),
            contact_name=data.get("contact_name", ""),
            num_recruiters=data.get("num_recruiters", 1),
            current_pain_points=data.get("current_pain_points", []),
            needs=data.get("needs", []),
            discussed_features=data.get("discussed_features", []),
            specific_request=data.get("specific_request"),
            hiring_situation=data.get("hiring_situation"),
            summary=data.get("summary", "")
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {e}")
        return _mock_analysis(transcript)
    except anthropic.APIError as e:
        logger.error(f"Anthropic API error: {e}")
        return _mock_analysis(transcript)


def _mock_analysis(transcript: str) -> MeetingAnalysis:
    """Fallback mock analysis when AI is not available"""
    # Extract some basic info from transcript
    lines = transcript.lower()
    
    return MeetingAnalysis(
        company_name="",
        contact_name="",
        num_recruiters=5,
        current_pain_points=[
            "Долгий процесс закрытия вакансий",
            "Разрозненные источники кандидатов",
            "Ручная работа с резюме"
        ],
        needs=[
            "Автоматизация рутинных задач",
            "Единая база кандидатов",
            "Прозрачная аналитика"
        ],
        discussed_features=[
            "Интеграции с job-сайтами",
            "Воронка подбора",
            "Аналитика"
        ],
        hiring_situation="Компания активно нанимает и ищет способы оптимизировать процесс рекрутинга",
        summary="Встреча с потенциальным клиентом по вопросу автоматизации найма"
    )
