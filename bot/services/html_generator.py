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


# CSS стили для документа — ЖЕЛЕЗОБЕТОННЫЕ, без шансов на наложение
CSS_STYLES = """
@page {
    size: A4;
    margin: 25px 30px 45px 30px;
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

* { 
    margin: 0 !important; 
    padding: 0 !important; 
    box-sizing: border-box !important;
    position: static !important;  /* ЗАПРЕТ absolute/relative */
}

body {
    font-family: Arial, Helvetica, sans-serif !important;
    color: #1a1a2e !important;
    background: #fff !important;
    font-size: 10pt !important;
    line-height: 1.6 !important;
    padding: 0 !important;
}

/* Заголовок */
.header {
    display: table !important;
    width: 100% !important;
    padding-bottom: 10px !important;
    margin-bottom: 20px !important;
    border-bottom: 3px solid #597FFF !important;
}
.header-left, .header-right {
    display: table-cell !important;
    vertical-align: middle !important;
}
.header-left { width: 50% !important; }
.header-right { 
    width: 50% !important; 
    text-align: right !important; 
    font-size: 9pt !important; 
    color: #666 !important; 
}
.header img { height: 32px !important; }

/* Основной заголовок */
h1 {
    font-size: 16pt !important;
    font-weight: bold !important;
    color: #1a1a2e !important;
    text-align: center !important;
    margin: 15px 0 20px 0 !important;
}
h1 small {
    display: block !important;
    font-size: 10pt !important;
    font-weight: normal !important;
    color: #666 !important;
    margin-top: 5px !important;
}

/* Секции — ОБЯЗАТЕЛЬНЫЕ отступы */
.section {
    margin-bottom: 30px !important;
    padding-bottom: 10px !important;
    page-break-inside: avoid !important;
}

.section-title {
    font-size: 12pt !important;
    font-weight: bold !important;
    color: #1a1a2e !important;
    margin-bottom: 15px !important;
    padding: 8px 12px !important;
    background: #F0F4FF !important;
    border-left: 4px solid #597FFF !important;
}

/* Подразделы */
.subsection {
    font-size: 10pt !important;
    font-weight: bold !important;
    color: #597FFF !important;
    margin: 20px 0 10px 0 !important;
    padding-left: 10px !important;
    border-left: 3px solid #597FFF !important;
}

/* СПИСКИ — БЕЗ POSITION, ТАБЛИЧНАЯ ВЁРСТКА */
ul, ol {
    list-style: none !important;
    margin: 10px 0 !important;
    padding: 0 !important;
}

li {
    display: table !important;
    width: 100% !important;
    margin: 6px 0 !important;
    padding: 0 !important;
    font-size: 10pt !important;
    line-height: 1.5 !important;
}

li::before {
    content: '→' !important;
    display: table-cell !important;
    width: 20px !important;
    color: #597FFF !important;
    font-weight: bold !important;
    vertical-align: top !important;
    padding-right: 8px !important;
}

li span, li div {
    display: table-cell !important;
    vertical-align: top !important;
}

/* Альтернатива — чек-маркер */
.check li::before {
    content: '✓' !important;
    color: #10B981 !important;
}

/* Блоки-цитаты */
.box {
    background: #F0F4FF !important;
    border-left: 4px solid #597FFF !important;
    padding: 12px 15px !important;
    margin: 15px 0 !important;
    font-size: 10pt !important;
}

/* Таблица цен */
.price-table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 15px 0 !important;
}
.price-table th, .price-table td {
    padding: 10px 12px !important;
    text-align: left !important;
    border: 1px solid #E2E8F0 !important;
    font-size: 10pt !important;
}
.price-table th { 
    background: #597FFF !important; 
    color: white !important; 
}
.price-table td:last-child { 
    text-align: right !important; 
    font-weight: bold !important; 
    color: #597FFF !important; 
}

/* ШАГИ — ТОЛЬКО ТАБЛИЦА, НИКАКОГО FLEXBOX */
.steps-table {
    width: 100% !important;
    border-collapse: separate !important;
    border-spacing: 8px !important;
    margin: 15px 0 !important;
}
.steps-table td {
    background: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 6px !important;
    padding: 12px 8px !important;
    text-align: center !important;
    vertical-align: top !important;
    width: 16.66% !important;
}
.step-num {
    font-size: 14pt !important;
    font-weight: bold !important;
    color: #597FFF !important;
    display: block !important;
    margin-bottom: 5px !important;
}
.step-title {
    font-weight: bold !important;
    font-size: 9pt !important;
    display: block !important;
    margin-bottom: 3px !important;
}
.step-desc {
    font-size: 8pt !important;
    color: #666 !important;
}

/* Маскот */
.mascot {
    text-align: center !important;
    margin: 30px 0 !important;
    padding: 20px 0 !important;
}
.mascot img { 
    height: 150px !important; 
}
.speech-bubble {
    display: inline-block !important;
    background: #F0F4FF !important;
    border: 2px solid #597FFF !important;
    border-radius: 12px !important;
    padding: 10px 15px !important;
    font-size: 10pt !important;
    margin-left: 15px !important;
    max-width: 200px !important;
    vertical-align: middle !important;
}

/* Бонус */
.bonus-box {
    background: #ECFDF5 !important;
    border: 2px solid #10B981 !important;
    border-radius: 8px !important;
    padding: 15px !important;
    margin: 15px 0 !important;
    text-align: center !important;
}
.bonus-box strong {
    color: #059669 !important;
}
"""


# Промпт для генерации HTML — СТРОГИЙ ШАБЛОН
GENERATION_PROMPT = """Создай HTML коммерческого предложения. КОПИРУЙ СТРУКТУРУ ТОЧНО!

## CSS (ВСТАВЬ В <style>)
{css_styles}

## ШАБЛОН HTML (КОПИРУЙ И ЗАПОЛНЯЙ!)

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
[ВСТАВЬ CSS СЮДА]
</style>
</head>
<body>

<!-- ШАПКА -->
<div class="header">
  <div class="header-left"><img src="{logo_path}"></div>
  <div class="header-right">[Название компании или пусто]</div>
</div>
<h1>Коммерческое предложение<small>ATS/CRM WorkHere для подбора персонала</small></h1>

<!-- РАЗДЕЛ 1 -->
<div class="section">
  <div class="section-title">1. Что обсуждали на встрече</div>
  <ul>
    <li><span>[Пункт из транскрибации]</span></li>
    <li><span>[Пункт из транскрибации]</span></li>
    <li><span>[Пункт из транскрибации]</span></li>
    <li><span>[Пункт из транскрибации]</span></li>
    <li><span>[Пункт из транскрибации]</span></li>
  </ul>
</div>

<!-- РАЗДЕЛ 2 — КОМПАКТНЫЙ! -->
<div class="section">
  <div class="section-title">2. Предлагаемое решение WorkHere</div>
  
  <div class="subsection">2.1. [Тема]</div>
  <ul>
    <li><span>[Короткий пункт]</span></li>
    <li><span>[Короткий пункт]</span></li>
  </ul>
  
  <div class="subsection">2.2. [Тема]</div>
  <ul>
    <li><span>[Короткий пункт]</span></li>
    <li><span>[Короткий пункт]</span></li>
  </ul>
  
  <div class="subsection">2.3. [Тема]</div>
  <ul>
    <li><span>[Короткий пункт]</span></li>
    <li><span>[Короткий пункт]</span></li>
  </ul>
  
  <div class="subsection">2.4. [Тема]</div>
  <ul>
    <li><span>[Короткий пункт]</span></li>
    <li><span>[Короткий пункт]</span></li>
  </ul>
</div>

<!-- РАЗДЕЛ 3 -->
<div class="section">
  <div class="section-title">3. Коммерческие условия</div>
  <table class="price-table">
    <tr><th>Тариф</th><th>Цена за лицензию/год</th></tr>
    <tr><td>Стандартный</td><td>20 000 ₽</td></tr>
    <tr><td>Премиум (с AI)</td><td>42 000 ₽</td></tr>
    <tr><td>Руководители</td><td>Бесплатно</td></tr>
  </table>
  [БОНУС ЕСЛИ ЕСТЬ]
</div>

<!-- РАЗДЕЛ 4 — ТОЛЬКО ТАБЛИЦА! -->
<div class="section">
  <div class="section-title">4. Внедрение и запуск</div>
  <table class="steps-table">
    <tr>
      <td><span class="step-num">1</span><span class="step-title">Демо</span><span class="step-desc">30 мин</span></td>
      <td><span class="step-num">2</span><span class="step-title">Договор</span><span class="step-desc">1 день</span></td>
      <td><span class="step-num">3</span><span class="step-title">Настройка</span><span class="step-desc">2-3 дня</span></td>
      <td><span class="step-num">4</span><span class="step-title">Обучение</span><span class="step-desc">1 час</span></td>
      <td><span class="step-num">5</span><span class="step-title">Запуск</span><span class="step-desc">1 день</span></td>
      <td><span class="step-num">6</span><span class="step-title">Поддержка</span><span class="step-desc">24/7</span></td>
    </tr>
  </table>
</div>

<!-- РАЗДЕЛ 5 -->
<div class="section">
  <div class="section-title">5. Следующие шаги</div>
  <ul>
    <li><span>Назначить демо-презентацию</span></li>
    <li><span>Подписать договор и выставить счёт</span></li>
    <li><span>Начать работу в системе</span></li>
  </ul>
</div>

<!-- МАСКОТ В КОНЦЕ -->
<div class="mascot">
  <img src="[ПУТЬ К МАСКОТУ]">
  <div class="speech-bubble">Меньше рутины, больше результата!</div>
</div>

</body>
</html>

## ДАННЫЕ ДЛЯ ЗАПОЛНЕНИЯ

Тариф: {tariff}
{bonus_info}

Маскоты: {mascot_paths}

## ТРАНСКРИБАЦИЯ
{transcript}

## КРИТИЧЕСКИЕ ПРАВИЛА

1. СПИСКИ: Всегда <li><span>текст</span></li> — НИКОГДА без <span>!
2. ШАГИ: ТОЛЬКО <table class="steps-table"> — ЗАПРЕЩЕНО div/flexbox/position!
3. ЦЕНЫ: ТОЛЬКО таблица с ценой за 1 лицензию! ЗАПРЕЩЕНО:
   - "Итого по запросу: X рекрутеров × Y ₽ = Z ₽"
   - Любые расчёты с количеством рекрутеров
   - Блоки с итоговой суммой
   - Клиент сам посчитает, не считай за него!
3. ФУТЕР: НЕ добавляй! Он в CSS автоматически!
4. КОМПАНИЯ: Нет названия = пустая строка, НЕ выдумывай!
5. РАЗДЕЛ 2: Максимум 4 подраздела по 2 пункта = 8 пунктов всего!
6. ОТСТУПЫ: class="section" имеет margin — НЕ добавляй лишние div!

Возвращай ТОЛЬКО готовый HTML без ```."""


def get_mascot_paths() -> list[str]:
    """Получить пути к маскотам"""
    mascots_dir = ASSETS_DIR / "mascots"
    if mascots_dir.exists():
        mascots = list(mascots_dir.glob("*.svg")) + list(mascots_dir.glob("*.png"))
        if mascots:
            return [str(m) for m in mascots[:5]]
    return []


def sanitize_html(html: str) -> str:
    """
    Пост-обработка HTML для исправления типичных ошибок GPT.
    Удаляет опасные стили, исправляет структуру.
    """
    import re
    
    # 1. Удаляем position:absolute и position:relative из inline стилей
    html = re.sub(r'position\s*:\s*(absolute|relative)\s*;?', '', html, flags=re.IGNORECASE)
    
    # 2. Удаляем left/right/top/bottom позиционирование
    html = re.sub(r'(left|right|top|bottom)\s*:\s*-?\d+[^;]*;?', '', html, flags=re.IGNORECASE)
    
    # 3. Убираем z-index
    html = re.sub(r'z-index\s*:\s*\d+\s*;?', '', html, flags=re.IGNORECASE)
    
    # 4. Исправляем <li> без <span> — добавляем span
    # Паттерн: <li> за которым НЕ следует <span
    html = re.sub(r'<li>(?!\s*<span)', '<li><span>', html)
    html = re.sub(r'(?<!</span>)</li>', '</span></li>', html)
    # Убираем двойные span если GPT уже добавил
    html = re.sub(r'<span>\s*<span>', '<span>', html)
    html = re.sub(r'</span>\s*</span>', '</span>', html)
    
    # 5. Убираем пустые стили
    html = re.sub(r'style="\s*"', '', html)
    
    # 6. Убираем дублирование футера если GPT добавил
    # Ищем паттерны типа "WorkHere © 2026" или "© 2026" в body
    html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<div[^>]*class="[^"]*footer[^"]*"[^>]*>.*?</div>', '', html, flags=re.IGNORECASE | re.DOTALL)
    
    # 7. Убираем transform
    html = re.sub(r'transform\s*:\s*[^;]+;?', '', html, flags=re.IGNORECASE)
    
    # 8. Удаляем блоки "Итого по запросу" с расчётами
    # Паттерны: "Итого: X рекрутеров × Y ₽", "Итого по запросу:", любые div с итогами
    html = re.sub(r'<div[^>]*>.*?[Ии]того.*?рекрутер.*?</div>', '', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<p[^>]*>.*?[Ии]того.*?рекрутер.*?</p>', '', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<div[^>]*class="[^"]*total[^"]*"[^>]*>.*?</div>', '', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<div[^>]*class="[^"]*price-total[^"]*"[^>]*>.*?</div>', '', html, flags=re.IGNORECASE | re.DOTALL)
    # Удаляем строки с "× 20 000" или "= 60 000" и т.п.
    html = re.sub(r'<[^>]+>.*?\d+\s*рекрутер[а-я]*\s*[×x]\s*\d+.*?</[^>]+>', '', html, flags=re.IGNORECASE | re.DOTALL)
    
    logger.info("HTML sanitized")
    return html


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
    
    # Санитизация HTML — исправляем типичные ошибки GPT
    html_content = sanitize_html(html_content)
    
    # Генерируем PDF
    html = HTML(string=html_content, base_url=str(ASSETS_DIR))
    html.write_pdf(str(output_path))
    
    logger.info(f"PDF generated: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    
    return output_path
