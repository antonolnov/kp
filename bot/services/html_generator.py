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
    margin: 20px 25px 40px 25px;
    @bottom-left {
        content: "WorkHere";
        font-size: 9pt;
        font-weight: bold;
        color: #597FFF;
    }
    @bottom-right {
        content: "© 2026";
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

.section { margin-bottom: 25px; page-break-inside: avoid; }
.section-title {
    font-size: 12pt;
    font-weight: bold;
    color: #1a1a2e;
    margin-bottom: 12px;
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
    margin: 18px 0 8px 0;
    padding-left: 8px;
    border-left: 3px solid #597FFF;
}

.subsection-block {
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #F0F0F0;
}

ul { list-style: none; margin: 0; padding: 0; }
ul li { padding: 6px 0 6px 16px; position: relative; font-size: 10pt; line-height: 1.4; }
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

## ПРАВИЛА ДИЗАЙНА

1. Документ 2-3 страницы A4
2. В НАЧАЛЕ документа — только логотип и простой заголовок, БЕЗ больших цветных блоков!
3. ЗАПРЕЩЕНО: несколько синих/цветных блоков подряд
4. Минималистичный дизайн — белый фон, акценты только в заголовках

## ПРАВИЛА ДЛЯ МАСКОТОВ (КРИТИЧНО!)

1. ПУСТОТА ВНИЗУ СТРАНИЦЫ = МАСКОТ! Это главное правило!
2. На КАЖДОЙ странице, где есть пустое пространство внизу — ОБЯЗАТЕЛЬНО вставить маскота
3. Особенно на ПЕРВОЙ странице — там почти всегда есть пустота, ОБЯЗАТЕЛЬНО кот!
4. Маскот размещается ПОСЕРЕДИНЕ пустого пространства (не прилеплен к тексту сверху, не прилеплен к футеру снизу)
5. ЗАПРЕЩЕНО вставлять маскотов между разделами в середине контента!
6. Каждый маскот с фразой в облачке

## ПРАВИЛА ОТСТУПОВ (КРИТИЧНО!)

1. Между подразделами (2.1, 2.2, 2.3...) — отступ минимум 15px margin-bottom
2. Между пунктами списка — padding 8px
3. Каждый подраздел должен визуально отделяться от соседнего
4. НЕ СЛИПАТЬ блоки! Пустое пространство между элементами обязательно
5. После заголовка подраздела — отступ 10px перед списком

## ПРАВИЛА ДЛЯ РАЗДЕЛА 2 (КРИТИЧНО!)

1. Раздел 2 ОБЯЗАН уместиться на ОДНОЙ странице! Это главное правило!
2. Максимум 4-5 подразделов (2.1, 2.2, 2.3, 2.4, 2.5)
3. Каждый подраздел — максимум 2 коротких пункта (не 3!)
4. Каждый пункт — максимум 1 строка текста
5. Если не влезает — СОКРАЩАЙ, не переноси на следующую страницу!

## ПРАВИЛА ДЛЯ ФУТЕРА

1. В конце КАЖДОЙ страницы — аккуратный футер
2. Текст футера: "WorkHere © 2026"
3. Маленький логотип рядом с текстом (высота 16px)
4. Цвет текста: серый (#999)
5. Размер: 8pt
6. НЕ писать техническую информацию типа "транскрибация" или "по итогам встречи"

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

## МАСКОТЫ ДЛЯ ЗАПОЛНЕНИЯ ПУСТОТЫ

Используй маскотов чтобы заполнить пустое пространство внизу страниц:
- Размещай ПОСЕРЕДИНЕ пустого пространства (не прилеплять к тексту или низу!)
- Можно несколько маскотов — по одному на каждую страницу где есть пустота
- НЕ вставляй между разделами в середине текста!

Пути к изображениям: {mascot_paths}

Фразы для маскотов (чередуй):
- "Меньше рутины, больше результата!"
- "Все отклики в одном месте — красота!"
- "Рекрутинг может быть простым!"
- "Подбор без хаоса — это реально!"

## ДАННЫЕ КЛИЕНТА

Тариф: {tariff}
Количество рекрутеров: {num_recruiters}
{bonus_info}

## ТРАНСКРИБАЦИЯ ВСТРЕЧИ

{transcript}

---

Сгенерируй ПОЛНЫЙ HTML-документ. Начни с <!DOCTYPE html> и закончи </html>.

Включи:
- <style> с CSS внутри <head>
- Логотип в header: <img src="{logo_path}">
- Все разделы
- Персонализированный контент на основе транскрибации
- Если есть бонус — добавь его в блок "Коммерческие условия"

КРИТИЧЕСКИ ВАЖНО:
1. НЕ добавляй футер в HTML! Футер "WorkHere © 2026" уже есть в CSS (@page), он добавится автоматически
2. На КАЖДОЙ странице с пустотой внизу — ОБЯЗАТЕЛЬНО маскот посередине пустого пространства
3. Возвращай ТОЛЬКО HTML, без ```html``` обёртки"""


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
    output_path: Path,
    bonus: str = None,
    previous_issues: list[str] = None
) -> Path:
    """
    Генерация КП через GPT-5.2.
    GPT сам создаёт HTML, выступая как дизайнер.
    Если previous_issues передан — это перегенерация для исправления ошибок.
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
    
    # Если есть ошибки от предыдущей генерации — добавляем в промпт
    issues_text = ""
    if previous_issues:
        issues_text = "\n\n⚠️ ИСПРАВЬ ЭТИ ОШИБКИ ИЗ ПРЕДЫДУЩЕЙ ВЕРСИИ:\n" + "\n".join(f"- {i}" for i in previous_issues)
    
    # Бонус при оплате на 2 года
    bonus_text = ""
    if bonus:
        bonus_text = f"\n\n**СПЕЦИАЛЬНОЕ ПРЕДЛОЖЕНИЕ (добавить в блок Коммерческие условия):**\n🎁 {bonus}"
    
    # Обрезаем транскрибацию если слишком длинная
    if len(transcript) > 20000:
        transcript = transcript[:20000] + "\n\n[...обрезано...]"
    
    prompt = GENERATION_PROMPT.format(
        css_styles=CSS_STYLES,
        mascot_paths=mascot_paths_str,
        tariff=tariff_label,
        num_recruiters=num_recruiters,
        bonus_info=bonus_text,
        transcript=transcript,
        logo_path=logo_path
    )
    
    is_retry = bool(previous_issues)
    logger.info(f"Generating HTML proposal via gpt-5.2 ({len(transcript)} chars, retry={is_retry})...")
    
    # GPT-5.2 uses new Responses API
    full_prompt = "Ты — дизайнер коммерческих предложений. Генерируй качественный HTML. Отвечай ТОЛЬКО HTML-кодом.\n\n" + prompt + issues_text
    
    response = client.responses.create(
        model="gpt-5.2",
        input=full_prompt
    )
    
    # Extract text from Responses API format
    html_content = response.output[0].content[0].text.strip()
    
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
