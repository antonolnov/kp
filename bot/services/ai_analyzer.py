"""
AI-генератор персонализированных коммерческих предложений
Модель: gpt-4o (думает глубоко)
Подход: сначала анализ, потом генерация развёрнутого контента
"""
import json
import logging
from dataclasses import dataclass, field
from typing import Optional

from openai import OpenAI

from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)


# Полная информация о продукте
PRODUCT_KNOWLEDGE = """
# WorkHere — ATS + CRM для найма и рекрутмента

## Для кого
- Рекрутеры — ежедневная работа с кандидатами, откликами, коммуникациями
- Руководитель подбора — контроль SLA, загрузки, конверсий, качества источников
- Нанимающие менеджеры — интервью, фидбек, согласования
- HR/HRD — аналитика найма, стандарты процесса, контроль качества

## Источники и интеграции
- Интеграции: HH.ru, Avito, SuperJob, Работа.ру
- Мессенджеры: Telegram, WhatsApp, Viber
- Телефония: звонки из системы, запись, логирование
- Email и календари
- 1С интеграция
- Яндекс Телемост

## Воронки и процесс
- Неограниченное число воронок (массовый/точечный найм, разные типы)
- Kanban-доска с этапами
- SLA и дедлайны на этапах
- Причины отказов с аналитикой
- Массовые действия (письма, перемещения, теги)

## Коммуникации
- Единая история в карточке (письма, звонки, сообщения)
- Шаблоны сообщений
- Telegram-бот для уведомлений рекрутерам
- Триггеры и автоматизации

## AI-модуль (Премиум)
- Умный поиск по базе (семантический, синонимы)
- Матчинг кандидат ↔ вакансия
- Ранжирование кандидатов
- Краткое резюме карточки за 20 секунд

## Аналитика
- Конверсия по этапам воронки
- Time-to-Hire, Time-to-Interview
- Эффективность источников
- Нагрузка и активность рекрутеров
- Выгрузки в Excel

## Безопасность
- Роли и права доступа
- Аудит действий
- ФЗ-152 (согласия на обработку ПД)

## Тарифы
- Стандартный: 20 000 ₽/лицензия/год
- Премиум (с AI): 42 000 ₽/лицензия/год
- Руководители-заказчики: бесплатно
"""


EXAMPLE_GOOD_CP = """
# ПРИМЕР ХОРОШЕГО КП (структура и стиль)

## 1. Текущая ситуация (Диагноз)

**Что мы услышали:** Команда из 5 рекрутеров работает с массовым наймом в сфере общепита. 
Сейчас используют Битрикс для CRM и Excel для отслеживания кандидатов. Система громоздкая, 
не заточена под рекрутинг — много ручной работы, теряются отклики, руководство не видит картину.

**Основные сложности:**
- Отклики с HH и Авито приходится вручную переносить — теряется время и кандидаты
- Нет единой истории коммуникаций — рекрутеры дублируют звонки, не видят кто уже общался
- Руководитель не понимает сколько кандидатов на каком этапе — нет прозрачности процесса
- Напоминания о собеседованиях делаются вручную в календаре — часто забывают
- Аналитика собирается в Excel раз в месяц — долго и неточно

## 2. Как WorkHere решит эти задачи

**Базовый функционал под ваши задачи:**
- Единая база кандидатов — все резюме с HH и Авито автоматически в одном месте, 
  дубли объединяются, история сохраняется
- Воронка с дашбордом — руководитель видит в реальном времени сколько кандидатов 
  на каком этапе, где застревают, какие вакансии горят
- История коммуникаций — каждый рекрутер видит все звонки и переписки коллег 
  в карточке кандидата, не нужно спрашивать "а ты ему звонил?"

**Интеграции:**
- HH.ru и Авито подключаются за 1 день — новые отклики появляются автоматически,
  не нужно проверять почту и переносить вручную
- WhatsApp и Telegram — переписка прямо в системе, вся история в карточке,
  шаблоны для типовых сообщений

**Автоматизация:**
- Напоминания о собеседованиях — кандидатам автоматически уходит SMS/сообщение,
  рекрутеру напоминание в Telegram-бот
- Уведомления о новых откликах — рекрутер не пропустит горячего кандидата

## 5. Что получит ваша команда

**Для рекрутеров:**
- Экономия 2+ часов в день — не нужно переносить отклики вручную и искать историю
- Вся информация в одном месте — резюме, контакты, переписки, звонки, комментарии
- Массовые действия — отправить SMS 50 кандидатам за минуту, а не по одному

**Для руководителя:**
- Дашборд в реальном времени — видно где узкие места, какие вакансии горят
- Понятно какой рекрутер сколько закрывает — аналитика эффективности
- Отчёты для руководства — выгрузка в Excel за 1 клик, не нужно собирать вручную

**Ключевой посыл:**
WorkHere уберёт ручную работу и даст прозрачность — рекрутеры сфокусируются на кандидатах, 
а руководитель будет видеть реальную картину подбора.
"""


@dataclass
class MeetingAnalysis:
    """Результат анализа и сгенерированный контент для КП"""
    # Метаданные
    company_name: str = ""
    contact_name: str = ""
    contact_role: str = ""
    num_recruiters: int = 1
    industry: str = ""
    
    # РАЗДЕЛ 1: Диагноз
    diagnosis_situation: str = ""
    diagnosis_pains: list[str] = field(default_factory=list)
    
    # РАЗДЕЛ 2: Решение
    solution_base: list[str] = field(default_factory=list)
    solution_integrations: list[str] = field(default_factory=list)
    solution_automation: list[str] = field(default_factory=list)
    solution_ai: list[str] = field(default_factory=list)
    
    # РАЗДЕЛ 5: Почему WorkHere
    why_recruiters: list[str] = field(default_factory=list)
    why_managers: list[str] = field(default_factory=list)
    
    # Ключевой посыл
    key_message: str = ""
    
    # Legacy
    hiring_situation: Optional[str] = None
    discussed_features: list[str] = field(default_factory=list)
    current_pain_points: list[str] = field(default_factory=list)
    needs: list[str] = field(default_factory=list)
    summary: str = ""


GENERATION_PROMPT = """Ты — опытный B2B-копирайтер коммерческих предложений для SaaS-продуктов.

Твоя задача: на основе транскрибации встречи создать ПЕРСОНАЛИЗИРОВАННОЕ коммерческое предложение 
для конкретного клиента. Не шаблонное, а именно под этого клиента — его боли, его ситуацию, его задачи.

---

{product_knowledge}

---

{example_cp}

---

## ТВОЯ ЗАДАЧА

Проанализируй транскрибацию встречи и создай контент для КП. 

ВАЖНО:
1. Пиши РАЗВЁРНУТО — каждый пункт это полноценное предложение с деталями
2. Связывай решения с болями клиента: "У вас проблема X → WorkHere решает через Y"
3. Используй конкретику из разговора — названия, цифры, детали
4. Не выдумывай то, чего не было в разговоре
5. Пиши живым языком, не канцеляритом
6. Каждый раздел должен быть УНИКАЛЬНЫМ для этого клиента

Верни JSON:

{{
    "company_name": "Название компании из разговора",
    "contact_name": "Имя контактного лица",
    "contact_role": "Должность",
    "num_recruiters": число_рекрутеров,
    "industry": "Сфера бизнеса",
    
    "diagnosis_situation": "2-4 предложения. Опиши текущую ситуацию клиента своими словами: что у них сейчас происходит с наймом, какие инструменты используют, в чём сложность. Это 'диагноз' — ты услышал клиента и резюмируешь его ситуацию.",
    
    "diagnosis_pains": [
        "Развёрнутая боль 1 — полное предложение, что конкретно не работает/мешает",
        "Развёрнутая боль 2 — что отнимает время или деньги",
        "Развёрнутая боль 3 — чего не хватает для эффективной работы",
        "Боль 4 если есть",
        "Боль 5 если есть"
    ],
    
    "solution_base": [
        "Функция 1 которая решает конкретную боль клиента — развёрнуто, как именно поможет",
        "Функция 2 — связь с проблемой клиента и как решается",
        "Функция 3 — что получит клиент"
    ],
    
    "solution_integrations": [
        "Интеграция которая нужна ЭТОМУ клиенту — почему именно им это важно",
        "Ещё интеграция с объяснением ценности"
    ],
    
    "solution_automation": [
        "Автоматизация которая сэкономит время ЭТОЙ команде — конкретно что автоматизируется",
        "Ещё автоматизация"
    ],
    
    "solution_ai": [
        "AI-функция если обсуждали или если клиенту явно нужна — с объяснением"
    ],
    
    "why_recruiters": [
        "Что получат рекрутеры ЭТОГО клиента — конкретно под их ситуацию, развёрнуто",
        "Ещё выгода для рекрутеров",
        "Ещё выгода"
    ],
    
    "why_managers": [
        "Что получит руководитель ЭТОГО клиента — под их задачи",
        "Ещё выгода для руководителя",
        "Ещё выгода"
    ],
    
    "key_message": "Одно-два предложения — главный посыл для ЭТОГО клиента, почему им нужен WorkHere. Должно резонировать с их ситуацией."
}}

---

ТРАНСКРИБАЦИЯ ВСТРЕЧИ:

{transcript}

---

Создай УНИКАЛЬНОЕ коммерческое предложение для этого клиента. Думай глубоко. 
Верни ТОЛЬКО валидный JSON без markdown-обёртки."""


async def analyze_transcript(transcript: str) -> MeetingAnalysis:
    """
    Генерация персонализированного КП через GPT-4o
    Модель думает глубоко, создаёт уникальный контент
    """
    
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set, using mock analysis")
        return _mock_analysis(transcript)
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Обрезаем если слишком длинно
        if len(transcript) > 30000:
            transcript = transcript[:30000] + "\n\n[...транскрибация обрезана...]"
        
        logger.info(f"Generating personalized CP for transcript ({len(transcript)} chars)...")
        
        prompt = GENERATION_PROMPT.format(
            product_knowledge=PRODUCT_KNOWLEDGE,
            example_cp=EXAMPLE_GOOD_CP,
            transcript=transcript
        )
        
        response = client.chat.completions.create(
            model="gpt-4o",  # Полноценная модель, думает глубже
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — senior B2B копирайтер с 10-летним опытом в SaaS. "
                        "Твои коммерческие предложения конвертируют потому что они ПЕРСОНАЛИЗИРОВАННЫЕ — "
                        "клиент читает и думает 'они понимают мою ситуацию'. "
                        "Никакого шаблонного текста. Только конкретика под клиента. "
                        "Отвечай валидным JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=4000,
            temperature=0.7  # Креативность для уникального контента
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
        
        # Логируем что получили
        logger.info(
            f"Generated CP: company={analysis.company_name}, "
            f"pains={len(analysis.diagnosis_pains)}, "
            f"solutions={len(analysis.solution_base)}, "
            f"situation_len={len(analysis.diagnosis_situation)}"
        )
        
        return analysis
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response: {e}")
        logger.error(f"Response was: {response_text[:500]}...")
        return _mock_analysis(transcript)
    except Exception as e:
        logger.error(f"AI generation error: {e}")
        return _mock_analysis(transcript)


def _mock_analysis(transcript: str) -> MeetingAnalysis:
    """Fallback если AI недоступен"""
    transcript_lower = transcript.lower()
    
    contact_name = ""
    for name in ["юлия", "анна", "мария", "елена", "ольга", "наталья"]:
        if name in transcript_lower:
            contact_name = name.capitalize()
            break
    
    num_recruiters = 3
    for word in ["пять", "5", "четыре", "4", "шесть", "6"]:
        if word in transcript_lower:
            num_recruiters = int(word) if word.isdigit() else {"пять": 5, "четыре": 4, "шесть": 6}.get(word, 3)
            break
    
    industry = ""
    if any(word in transcript_lower for word in ["общепит", "ресторан", "кафе", "повар"]):
        industry = "HoReCa"
    elif any(word in transcript_lower for word in ["it", "разработ", "программ"]):
        industry = "IT"
    elif any(word in transcript_lower for word in ["производств", "завод", "фабрик"]):
        industry = "Производство"
    elif any(word in transcript_lower for word in ["ритейл", "магазин", "продаж"]):
        industry = "Ритейл"
    
    return MeetingAnalysis(
        company_name="",
        contact_name=contact_name,
        contact_role="HR-директор" if "директор" in transcript_lower else "HR-менеджер",
        num_recruiters=num_recruiters,
        industry=industry,
        
        diagnosis_situation=(
            "Компания активно развивается и масштабирует найм. "
            "Текущие инструменты — Excel и почта — не справляются с объёмом. "
            "Команде не хватает системности и прозрачности в процессе подбора."
        ),
        diagnosis_pains=[
            "Отклики с разных площадок приходится вручную сводить в таблицы — теряется время и кандидаты",
            "Нет единой истории коммуникаций — рекрутеры не видят кто уже общался с кандидатом",
            "Руководство не видит реальную картину подбора — сколько кандидатов на каком этапе",
            "Аналитика собирается вручную в Excel — долго и часто неточно",
        ],
        
        solution_base=[
            "Единая база кандидатов — все резюме и контакты в одном месте, дубли объединяются автоматически",
            "Воронка подбора с визуальным дашбордом — видно сколько кандидатов на каждом этапе",
            "История коммуникаций в карточке — все звонки, письма и переписки коллег на виду",
        ],
        solution_integrations=[
            "Интеграция с HH.ru и Авито — отклики попадают в систему автоматически, не нужно переносить вручную",
            "Мессенджеры (Telegram, WhatsApp) — переписка с кандидатами прямо в системе",
        ],
        solution_automation=[
            "Уведомления о новых откликах в Telegram — рекрутер не пропустит горячего кандидата",
            "Напоминания о собеседованиях — автоматически кандидату и рекрутеру",
        ],
        solution_ai=[],
        
        why_recruiters=[
            "Экономия 2+ часов в день — не нужно переносить отклики вручную и искать информацию",
            "Вся история в одном месте — резюме, контакты, переписки, комментарии коллег",
            "Массовые действия — отправить сообщение десяткам кандидатов за минуту",
        ],
        why_managers=[
            "Дашборд в реальном времени — видно где узкие места и какие вакансии горят",
            "Аналитика по рекрутерам — понятно кто сколько закрывает и где задержки",
            "Отчёты для руководства — выгрузка в Excel за 1 клик",
        ],
        
        key_message=(
            "WorkHere уберёт ручную работу и даст прозрачность — "
            "рекрутеры сфокусируются на кандидатах, а руководство будет видеть реальную картину."
        ),
        
        hiring_situation="Компания масштабирует найм, текущие инструменты не справляются.",
        discussed_features=["Интеграции", "Воронки", "Аналитика"],
    )
