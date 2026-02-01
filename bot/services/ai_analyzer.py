"""
AI-powered meeting transcript analyzer
Роль: Копирайтер + Дизайнер коммерческих предложений
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
    """Структурированный анализ для персонализированного КП"""
    # Метаданные клиента
    company_name: str = ""
    contact_name: str = ""
    contact_role: str = ""
    num_recruiters: int = 1
    industry: str = ""
    
    # РАЗДЕЛ 1: Диагноз (боли и текущая ситуация)
    diagnosis_situation: str = ""  # Описание текущей ситуации
    diagnosis_pains: list[str] = field(default_factory=list)  # Конкретные боли
    
    # РАЗДЕЛ 2: Решение (персонализированное)
    solution_base: list[str] = field(default_factory=list)  # Базовый функционал под клиента
    solution_integrations: list[str] = field(default_factory=list)  # Нужные интеграции
    solution_automation: list[str] = field(default_factory=list)  # Нужная автоматизация
    solution_ai: list[str] = field(default_factory=list)  # AI если релевантно
    
    # РАЗДЕЛ 5: Почему WorkHere (персонализированные аргументы)
    why_recruiters: list[str] = field(default_factory=list)  # Для рекрутеров этого клиента
    why_managers: list[str] = field(default_factory=list)  # Для руководителей этого клиента
    
    # Ключевой посыл
    key_message: str = ""
    
    # Legacy поля для совместимости
    hiring_situation: Optional[str] = None
    discussed_features: list[str] = field(default_factory=list)
    current_pain_points: list[str] = field(default_factory=list)
    needs: list[str] = field(default_factory=list)
    summary: str = ""


ANALYSIS_PROMPT = """Ты — опытный копирайтер коммерческих предложений для B2B SaaS.

Твоя задача: проанализировать транскрибацию встречи и создать ПЕРСОНАЛИЗИРОВАННОЕ коммерческое предложение для конкретного клиента.

WorkHere — это ATS-система (Applicant Tracking System) для рекрутинга. Возможности:
- Единая база кандидатов
- Интеграции с HH.ru, Авито, SuperJob, Работа.ру
- Мессенджеры: Telegram, WhatsApp, Viber
- IP-телефония с записью
- Воронки и статусы
- Аналитика и отчёты
- Telegram-бот для уведомлений
- Заявки на подбор
- 152-ФЗ (согласия на обработку ПД)
- AI-поиск и матчинг кандидатов

---

ТВОЯ ЗАДАЧА — вернуть JSON:

{
    "company_name": "Название компании",
    "contact_name": "Имя контактного лица",
    "contact_role": "Должность",
    "num_recruiters": число,
    "industry": "Сфера бизнеса",
    
    "diagnosis_situation": "2-3 предложения о текущей ситуации клиента с наймом. Что сейчас происходит? Какие инструменты используют? В чём сложность?",
    
    "diagnosis_pains": [
        "Конкретная боль 1 — что именно не работает/мешает",
        "Конкретная боль 2 — что отнимает время",
        "Конкретная боль 3 — чего не хватает",
        "Боль 4 (если есть)",
        "Боль 5 (если есть)"
    ],
    
    "solution_base": [
        "Функция базового блока, которая РЕШАЕТ боль клиента — объяснение как именно",
        "Ещё функция — как решает проблему",
        "Ещё функция"
    ],
    
    "solution_integrations": [
        "Интеграция которая нужна ЭТОМУ клиенту — зачем именно ему",
        "Ещё интеграция"
    ],
    
    "solution_automation": [
        "Автоматизация которая сэкономит время ЭТОМУ клиенту",
        "Ещё автоматизация"
    ],
    
    "solution_ai": [
        "AI-функция если обсуждали или клиенту нужна"
    ],
    
    "why_recruiters": [
        "Аргумент для рекрутеров ЭТОГО клиента — конкретно под их ситуацию",
        "Ещё аргумент",
        "Ещё аргумент"
    ],
    
    "why_managers": [
        "Аргумент для руководителей ЭТОГО клиента — что получат",
        "Ещё аргумент",
        "Ещё аргумент"
    ],
    
    "key_message": "Одно предложение — главный посыл для этого клиента, почему им нужен WorkHere"
}

---

ВАЖНО:
1. Пиши от лица WorkHere, обращаясь к клиенту
2. Каждый пункт должен быть КОНКРЕТНЫМ, не общим
3. Связывай функции с болями клиента
4. Не выдумывай — используй информацию из транскрибации
5. Если чего-то нет в разговоре — не добавляй

---

ТРАНСКРИБАЦИЯ ВСТРЕЧИ:
{transcript}

---

Верни ТОЛЬКО JSON, без markdown."""


async def analyze_transcript(transcript: str) -> MeetingAnalysis:
    """Анализ транскрибации как копирайтер КП"""
    
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set, using mock analysis")
        return _mock_analysis(transcript)
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Обрезаем если слишком длинно
        if len(transcript) > 25000:
            transcript = transcript[:25000] + "\n\n[...транскрибация обрезана...]"
        
        logger.info(f"Analyzing transcript ({len(transcript)} chars) as copywriter...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты — копирайтер B2B коммерческих предложений. Твоя задача — создать персонализированное КП на основе транскрибации встречи. Отвечай только валидным JSON."
                },
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(transcript=transcript)
                }
            ],
            max_tokens=3000,
            temperature=0.3
        )
        
        response_text = response.choices[0].message.content.strip()
        logger.info(f"AI response received ({len(response_text)} chars)")
        
        # Очистка от markdown
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        data = json.loads(response_text)
        
        analysis = MeetingAnalysis(
            company_name=data.get("company_name", "") or "",
            contact_name=data.get("contact_name", "") or "",
            contact_role=data.get("contact_role", "") or "",
            num_recruiters=int(data.get("num_recruiters", 1) or 1),
            industry=data.get("industry", "") or "",
            
            diagnosis_situation=data.get("diagnosis_situation", "") or "",
            diagnosis_pains=data.get("diagnosis_pains", []) or [],
            
            solution_base=data.get("solution_base", []) or [],
            solution_integrations=data.get("solution_integrations", []) or [],
            solution_automation=data.get("solution_automation", []) or [],
            solution_ai=data.get("solution_ai", []) or [],
            
            why_recruiters=data.get("why_recruiters", []) or [],
            why_managers=data.get("why_managers", []) or [],
            
            key_message=data.get("key_message", "") or "",
            
            # Legacy
            hiring_situation=data.get("diagnosis_situation", ""),
            discussed_features=data.get("diagnosis_pains", []),
            current_pain_points=data.get("diagnosis_pains", []),
        )
        
        logger.info(f"Analysis complete: {analysis.company_name}, {len(analysis.diagnosis_pains)} pains, {len(analysis.solution_base)} solutions")
        return analysis
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response: {e}")
        return _mock_analysis(transcript)
    except Exception as e:
        logger.error(f"AI analysis error: {e}")
        return _mock_analysis(transcript)


def _mock_analysis(transcript: str) -> MeetingAnalysis:
    """Fallback анализ без AI"""
    transcript_lower = transcript.lower()
    
    contact_name = ""
    if "юлия" in transcript_lower:
        contact_name = "Юлия"
    
    num_recruiters = 3
    if "эйчар" in transcript_lower or "hr" in transcript_lower:
        num_recruiters += 1
    
    industry = ""
    if any(word in transcript_lower for word in ["общепит", "ресторан", "кафе", "повар"]):
        industry = "HoReCa"
    elif any(word in transcript_lower for word in ["it", "разработ", "программ"]):
        industry = "IT"
    
    return MeetingAnalysis(
        company_name="",
        contact_name=contact_name,
        contact_role="HR-директор" if "директор" in transcript_lower else "",
        num_recruiters=num_recruiters,
        industry=industry,
        
        diagnosis_situation="Компания ищет способы оптимизировать процесс подбора персонала. Текущие инструменты не закрывают все потребности команды.",
        diagnosis_pains=[
            "Работа ведётся в нескольких инструментах — нет единой системы",
            "Много времени уходит на ручной перенос данных между площадками",
            "Сложно отслеживать статусы кандидатов и историю коммуникаций",
            "Нет прозрачной аналитики по эффективности подбора",
        ],
        
        solution_base=[
            "Единая база кандидатов — все резюме, контакты и история в одном месте",
            "Воронки подбора — визуальный контроль статусов на каждом этапе",
            "Аналитика — понимание конверсий, источников, времени закрытия",
        ],
        solution_integrations=[
            "HH.ru, Авито — отклики автоматически попадают в систему",
            "Мессенджеры — переписка с кандидатами прямо в карточке",
        ],
        solution_automation=[
            "Уведомления в Telegram — рекрутер не пропустит важное",
            "Напоминания о собеседованиях — автоматически",
        ],
        solution_ai=[],
        
        why_recruiters=[
            "Все отклики в одном месте — не нужно переключаться",
            "Меньше рутины — больше времени на кандидатов",
        ],
        why_managers=[
            "Прозрачность — видно что происходит с подбором",
            "Контроль сроков — понятно где задержки",
        ],
        
        key_message="WorkHere объединит все инструменты подбора в одной системе и сэкономит время команды.",
        
        hiring_situation="Компания ищет способы оптимизировать процесс подбора.",
        discussed_features=["Интеграции", "Воронки", "Аналитика"],
    )
