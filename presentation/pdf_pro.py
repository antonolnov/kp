"""
WorkHere PDF Presentation — Professional Design
Строгая сетка, продуманные отступы, чистая типографика
"""

from weasyprint import HTML
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════

COLORS = {
    'primary': '#4F6AF5',      # Основной синий
    'primary_dark': '#3D56D4', # Тёмный синий
    'primary_light': '#E8ECFE', # Светлый синий фон
    'accent': '#10B981',       # Зелёный акцент
    'accent_warm': '#F59E0B',  # Оранжевый
    'dark': '#111827',         # Почти чёрный текст
    'gray': '#6B7280',         # Серый текст
    'gray_light': '#9CA3AF',   # Светло-серый
    'border': '#E5E7EB',       # Границы
    'bg_light': '#F9FAFB',     # Светлый фон
    'white': '#FFFFFF',
}

# ═══════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════

CSS = f"""
@page {{
    size: 297mm 210mm;
    margin: 0;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: {COLORS['dark']};
    -webkit-font-smoothing: antialiased;
}}

/* ═══════════════════════════════════════════════════════════════
   SLIDE LAYOUT
   ═══════════════════════════════════════════════════════════════ */

.slide {{
    width: 297mm;
    height: 210mm;
    padding: 25mm 30mm;
    page-break-after: always;
    position: relative;
    background: {COLORS['white']};
}}

.slide:last-child {{
    page-break-after: avoid;
}}

.slide-dark {{
    background: {COLORS['dark']};
    color: {COLORS['white']};
}}

.slide-primary {{
    background: {COLORS['primary']};
    color: {COLORS['white']};
}}

/* ═══════════════════════════════════════════════════════════════
   TYPOGRAPHY — Строгая иерархия
   ═══════════════════════════════════════════════════════════════ */

.tag {{
    display: inline-block;
    font-size: 9pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {COLORS['primary']};
    margin-bottom: 8mm;
}}

.tag-light {{
    color: rgba(255,255,255,0.8);
}}

h1 {{
    font-size: 48pt;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -1px;
    margin-bottom: 6mm;
}}

h2 {{
    font-size: 28pt;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.5px;
    margin-bottom: 10mm;
    color: {COLORS['dark']};
}}

.slide-dark h2,
.slide-primary h2 {{
    color: {COLORS['white']};
}}

h3 {{
    font-size: 14pt;
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: 4mm;
    color: {COLORS['dark']};
}}

h4 {{
    font-size: 11pt;
    font-weight: 600;
    margin-bottom: 3mm;
    color: {COLORS['dark']};
}}

p {{
    font-size: 11pt;
    line-height: 1.6;
    color: {COLORS['gray']};
}}

.text-small {{
    font-size: 9pt;
}}

.text-large {{
    font-size: 14pt;
}}

.text-muted {{
    color: {COLORS['gray_light']};
}}

.text-primary {{
    color: {COLORS['primary']};
}}

.text-white {{
    color: {COLORS['white']};
}}

/* ═══════════════════════════════════════════════════════════════
   GRID SYSTEM — 12 колонок
   ═══════════════════════════════════════════════════════════════ */

.row {{
    display: table;
    width: 100%;
    table-layout: fixed;
}}

.col {{
    display: table-cell;
    vertical-align: top;
    padding-right: 8mm;
}}

.col:last-child {{
    padding-right: 0;
}}

.col-2 {{ width: 50%; }}
.col-3 {{ width: 33.333%; }}
.col-4 {{ width: 25%; }}
.col-6 {{ width: 16.666%; }}

.gap-sm {{ padding-right: 5mm; }}
.gap-md {{ padding-right: 8mm; }}
.gap-lg {{ padding-right: 12mm; }}

/* ═══════════════════════════════════════════════════════════════
   CARDS
   ═══════════════════════════════════════════════════════════════ */

.card {{
    background: {COLORS['white']};
    border: 1px solid {COLORS['border']};
    border-radius: 4mm;
    padding: 6mm;
    margin-bottom: 5mm;
}}

.card-filled {{
    background: {COLORS['bg_light']};
    border: none;
}}

.card-primary {{
    background: {COLORS['primary_light']};
    border: 1px solid {COLORS['primary']};
}}

.card-dark {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
}}

.card-accent {{
    background: {COLORS['primary']};
    color: {COLORS['white']};
    border: none;
}}

/* ═══════════════════════════════════════════════════════════════
   STATS
   ═══════════════════════════════════════════════════════════════ */

.stat {{
    text-align: center;
    padding: 5mm 0;
}}

.stat-value {{
    font-size: 36pt;
    font-weight: 700;
    line-height: 1;
    color: {COLORS['primary']};
    margin-bottom: 2mm;
}}

.stat-value-lg {{
    font-size: 48pt;
}}

.stat-label {{
    font-size: 10pt;
    color: {COLORS['gray']};
}}

/* ═══════════════════════════════════════════════════════════════
   LISTS
   ═══════════════════════════════════════════════════════════════ */

ul {{
    list-style: none;
    margin: 0;
    padding: 0;
}}

li {{
    padding: 2mm 0 2mm 6mm;
    position: relative;
    font-size: 11pt;
    line-height: 1.5;
}}

li::before {{
    content: '';
    position: absolute;
    left: 0;
    top: 4.5mm;
    width: 1.5mm;
    height: 1.5mm;
    background: {COLORS['primary']};
    border-radius: 50%;
}}

.list-check li::before {{
    content: '✓';
    width: auto;
    height: auto;
    background: none;
    color: {COLORS['accent']};
    font-size: 10pt;
    font-weight: 700;
    top: 2mm;
}}

/* ═══════════════════════════════════════════════════════════════
   TABLES
   ═══════════════════════════════════════════════════════════════ */

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 4mm 5mm;
    text-align: left;
    font-size: 10pt;
    border-bottom: 1px solid {COLORS['border']};
}}

th {{
    background: {COLORS['primary']};
    color: {COLORS['white']};
    font-weight: 600;
    border-bottom: none;
}}

th:first-child {{
    border-radius: 2mm 0 0 0;
}}

th:last-child {{
    border-radius: 0 2mm 0 0;
}}

/* ═══════════════════════════════════════════════════════════════
   STEPS / TIMELINE
   ═══════════════════════════════════════════════════════════════ */

.steps {{
    display: table;
    width: 100%;
    table-layout: fixed;
}}

.step {{
    display: table-cell;
    text-align: center;
    padding: 5mm 3mm;
    background: {COLORS['bg_light']};
    border-right: 1px solid {COLORS['border']};
    vertical-align: top;
}}

.step:last-child {{
    border-right: none;
}}

.step-num {{
    font-size: 20pt;
    font-weight: 700;
    color: {COLORS['primary']};
    margin-bottom: 2mm;
}}

.step-title {{
    font-size: 10pt;
    font-weight: 600;
    color: {COLORS['dark']};
    margin-bottom: 1mm;
}}

.step-desc {{
    font-size: 8pt;
    color: {COLORS['gray']};
}}

/* ═══════════════════════════════════════════════════════════════
   ICONS (Emoji-based)
   ═══════════════════════════════════════════════════════════════ */

.icon {{
    font-size: 24pt;
    margin-bottom: 4mm;
    display: block;
}}

.icon-sm {{
    font-size: 18pt;
}}

.icon-lg {{
    font-size: 32pt;
}}

/* ═══════════════════════════════════════════════════════════════
   BADGES / TAGS
   ═══════════════════════════════════════════════════════════════ */

.badge {{
    display: inline-block;
    padding: 1.5mm 4mm;
    border-radius: 2mm;
    font-size: 8pt;
    font-weight: 600;
}}

.badge-primary {{
    background: {COLORS['primary']};
    color: {COLORS['white']};
}}

.badge-accent {{
    background: {COLORS['accent']};
    color: {COLORS['white']};
}}

.badge-outline {{
    background: transparent;
    border: 1px solid {COLORS['border']};
    color: {COLORS['gray']};
}}

/* ═══════════════════════════════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════════════════════════════ */

.footer {{
    position: absolute;
    bottom: 8mm;
    left: 30mm;
    right: 30mm;
    display: table;
    width: calc(100% - 60mm);
    font-size: 9pt;
    color: {COLORS['gray_light']};
}}

.footer-left {{
    display: table-cell;
    text-align: left;
}}

.footer-right {{
    display: table-cell;
    text-align: right;
}}

.logo {{
    font-weight: 700;
    color: {COLORS['primary']};
}}

.logo-box {{
    display: inline-block;
    width: 5mm;
    height: 5mm;
    background: {COLORS['primary']};
    color: {COLORS['white']};
    text-align: center;
    line-height: 5mm;
    font-size: 8pt;
    font-weight: 700;
    border-radius: 1mm;
    margin-right: 2mm;
    vertical-align: middle;
}}

/* ═══════════════════════════════════════════════════════════════
   UTILITIES
   ═══════════════════════════════════════════════════════════════ */

.mb-0 {{ margin-bottom: 0; }}
.mb-1 {{ margin-bottom: 3mm; }}
.mb-2 {{ margin-bottom: 5mm; }}
.mb-3 {{ margin-bottom: 8mm; }}
.mb-4 {{ margin-bottom: 12mm; }}

.mt-1 {{ margin-top: 3mm; }}
.mt-2 {{ margin-top: 5mm; }}
.mt-3 {{ margin-top: 8mm; }}
.mt-4 {{ margin-top: 12mm; }}

.pt-4 {{ padding-top: 12mm; }}

.center {{ text-align: center; }}
.right {{ text-align: right; }}

.valign-middle {{
    vertical-align: middle;
}}

/* ═══════════════════════════════════════════════════════════════
   SPECIFIC COMPONENTS
   ═══════════════════════════════════════════════════════════════ */

.hero-stat {{
    display: inline-block;
    margin-right: 15mm;
}}

.hero-stat-value {{
    font-size: 28pt;
    font-weight: 700;
    color: {COLORS['primary']};
}}

.hero-stat-label {{
    font-size: 10pt;
    color: {COLORS['gray']};
}}

.pricing-card {{
    text-align: center;
    padding: 8mm 5mm;
    border: 1px solid {COLORS['border']};
    border-radius: 4mm;
}}

.pricing-card.featured {{
    border: 2px solid {COLORS['primary']};
    background: {COLORS['primary_light']};
}}

.price {{
    font-size: 28pt;
    font-weight: 700;
    color: {COLORS['primary']};
}}

.price-period {{
    font-size: 9pt;
    color: {COLORS['gray']};
    margin-bottom: 5mm;
}}

.funnel-row {{
    margin-bottom: 2mm;
}}

.funnel-bar {{
    height: 8mm;
    background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
    border-radius: 1.5mm;
    color: {COLORS['white']};
    font-size: 9pt;
    font-weight: 500;
    line-height: 8mm;
    padding: 0 4mm;
}}

.integration-badge {{
    display: inline-block;
    padding: 2mm 4mm;
    margin: 1mm;
    border-radius: 2mm;
    font-size: 9pt;
    font-weight: 600;
    color: {COLORS['white']};
}}
"""

# ═══════════════════════════════════════════════════════════════
# HTML SLIDES
# ═══════════════════════════════════════════════════════════════

HTML_CONTENT = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>WorkHere — Презентация</title>
<style>{CSS}</style>
</head>
<body>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 1: TITLE
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-dark">
    <div style="padding-top: 25mm;">
        <p class="tag tag-light">ATS + CRM для рекрутинга</p>
        <h1 style="font-size: 64pt; margin-bottom: 10mm;">WorkHere</h1>
        <p class="text-large" style="color: rgba(255,255,255,0.7); margin-bottom: 20mm;">
            Система управления наймом,<br>которая закрывает вакансии быстрее
        </p>
        <div>
            <span class="hero-stat">
                <span class="hero-stat-value" style="color: #fff;">8 500+</span><br>
                <span class="hero-stat-label" style="color: rgba(255,255,255,0.6);">компаний</span>
            </span>
            <span class="hero-stat">
                <span class="hero-stat-value" style="color: #fff;">350+</span><br>
                <span class="hero-stat-label" style="color: rgba(255,255,255,0.6);">городов России</span>
            </span>
            <span class="hero-stat">
                <span class="hero-stat-value" style="color: #fff;">3 года</span><br>
                <span class="hero-stat-label" style="color: rgba(255,255,255,0.6);">на рынке</span>
            </span>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 2: ПРОБЛЕМА
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Проблема</p>
    <h2>С чем сталкиваются HR-команды</h2>
    
    <div class="row">
        <div class="col col-3 gap-md">
            <div class="card card-filled">
                <span class="icon icon-sm">📊</span>
                <h4>Хаос в данных</h4>
                <p class="text-small">Кандидаты в Excel, почте, мессенджерах. Дубли, потери, путаница.</p>
            </div>
        </div>
        <div class="col col-3 gap-md">
            <div class="card card-filled">
                <span class="icon icon-sm">⏰</span>
                <h4>Долгое закрытие</h4>
                <p class="text-small">Нет контроля сроков. Кандидаты уходят к конкурентам.</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled">
                <span class="icon icon-sm">📉</span>
                <h4>Нет аналитики</h4>
                <p class="text-small">Не понятно, какие источники работают и где теряются кандидаты.</p>
            </div>
        </div>
    </div>
    
    <div class="row mt-2">
        <div class="col col-3 gap-md">
            <div class="card card-filled">
                <span class="icon icon-sm">🔐</span>
                <h4>Риски ПДн</h4>
                <p class="text-small">Согласия не собираются, нет контроля доступа, 152-ФЗ под вопросом.</p>
            </div>
        </div>
        <div class="col col-3 gap-md">
            <div class="card card-filled">
                <span class="icon icon-sm">🤯</span>
                <h4>Рутина</h4>
                <p class="text-small">80% времени на ручные операции вместо работы с людьми.</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled">
                <span class="icon icon-sm">🔌</span>
                <h4>Разрозненные инструменты</h4>
                <p class="text-small">CRM отдельно, почта отдельно, мессенджеры отдельно.</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">2</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 3: РЕШЕНИЕ
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-primary center">
    <div style="padding-top: 35mm;">
        <p class="tag tag-light">Решение</p>
        <h2 style="font-size: 36pt; color: #fff; margin-bottom: 15mm;">
            Одна система для всего<br>процесса найма
        </h2>
        <div style="background: rgba(255,255,255,0.15); padding: 8mm 12mm; border-radius: 4mm; display: inline-block;">
            <span style="font-size: 32pt; font-weight: 700;">WorkHere</span>
        </div>
        <p style="color: rgba(255,255,255,0.8); margin-top: 12mm; font-size: 12pt;">
            От заявки на подбор до выхода сотрудника —<br>
            всё в одном месте, под контролем, с аналитикой
        </p>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 4: ДЛЯ КОГО
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Аудитория</p>
    <h2>Для всех участников найма</h2>
    
    <div class="row">
        <div class="col col-4 gap-md">
            <div class="card" style="height: 52mm;">
                <span class="icon icon-sm">👨‍💼</span>
                <h4>Рекрутер</h4>
                <ul class="text-small">
                    <li>Единая база кандидатов</li>
                    <li>Автоматизация рутины</li>
                    <li>Шаблоны сообщений</li>
                </ul>
            </div>
        </div>
        <div class="col col-4 gap-md">
            <div class="card card-accent" style="height: 52mm;">
                <span class="icon icon-sm">👩‍💼</span>
                <h4 style="color: #fff;">Руководитель подбора</h4>
                <ul class="text-small" style="color: rgba(255,255,255,0.9);">
                    <li style="color: #fff;">Контроль SLA</li>
                    <li style="color: #fff;">Аналитика команды</li>
                    <li style="color: #fff;">Отчёты</li>
                </ul>
            </div>
        </div>
        <div class="col col-4 gap-md">
            <div class="card" style="height: 52mm;">
                <span class="icon icon-sm">🧑‍💻</span>
                <h4>Нанимающий менеджер</h4>
                <ul class="text-small">
                    <li>Просмотр кандидатов</li>
                    <li>Быстрый фидбек</li>
                    <li>Уведомления</li>
                </ul>
            </div>
        </div>
        <div class="col col-4">
            <div class="card" style="height: 52mm;">
                <span class="icon icon-sm">📊</span>
                <h4>HRD / Бизнес</h4>
                <ul class="text-small">
                    <li>Стоимость найма</li>
                    <li>Прогнозирование</li>
                    <li>Unit-экономика</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">4</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 5: ВОРОНКА
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Процесс</p>
    <h2>Полный цикл найма</h2>
    
    <div class="steps mt-3">
        <div class="step">
            <div class="step-num">01</div>
            <div class="step-title">Заявка</div>
            <div class="step-desc">От менеджера</div>
        </div>
        <div class="step">
            <div class="step-num">02</div>
            <div class="step-title">Публикация</div>
            <div class="step-desc">На job-сайтах</div>
        </div>
        <div class="step">
            <div class="step-num">03</div>
            <div class="step-title">Отклики</div>
            <div class="step-desc">Единый поток</div>
        </div>
        <div class="step">
            <div class="step-num">04</div>
            <div class="step-title">Скрининг</div>
            <div class="step-desc">Отбор + AI</div>
        </div>
        <div class="step">
            <div class="step-num">05</div>
            <div class="step-title">Интервью</div>
            <div class="step-desc">Оценка</div>
        </div>
        <div class="step" style="background: {COLORS['primary_light']};">
            <div class="step-num">06</div>
            <div class="step-title">Оффер</div>
            <div class="step-desc">Выход</div>
        </div>
    </div>
    
    <div class="card card-primary mt-4" style="padding: 5mm 8mm;">
        <div class="row">
            <div class="col col-2 valign-middle">
                <strong>Ключевое:</strong> контроль на каждом этапе с SLA и автоматическими напоминаниями
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">5</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 6: БАЗА КАНДИДАТОВ
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Возможности</p>
    <h2>Единая база кандидатов</h2>
    
    <div class="row">
        <div class="col col-2 gap-lg">
            <ul class="list-check">
                <li>Все резюме в одном месте</li>
                <li>Полная история взаимодействий</li>
                <li>Комментарии и теги</li>
                <li>Умный поиск по тексту</li>
                <li>Защита от дублей</li>
                <li>Слияние карточек</li>
            </ul>
            
            <div class="card card-primary mt-3" style="padding: 4mm 6mm;">
                <p class="text-small mb-0"><strong>Результат:</strong> ни один кандидат не теряется, вся история под рукой</p>
            </div>
        </div>
        <div class="col col-2">
            <div style="background: {COLORS['dark']}; border-radius: 3mm; padding: 5mm;">
                <div style="display: flex; gap: 2mm; margin-bottom: 4mm;">
                    <span style="width: 3mm; height: 3mm; border-radius: 50%; background: #ff5f57;"></span>
                    <span style="width: 3mm; height: 3mm; border-radius: 50%; background: #febc2e;"></span>
                    <span style="width: 3mm; height: 3mm; border-radius: 50%; background: #28c840;"></span>
                </div>
                <div style="background: rgba(255,255,255,0.08); padding: 4mm; border-radius: 2mm; margin-bottom: 3mm;">
                    <div style="display: flex; align-items: center; gap: 3mm;">
                        <div style="width: 10mm; height: 10mm; background: {COLORS['primary']}; border-radius: 2mm; color: #fff; text-align: center; line-height: 10mm; font-size: 9pt; font-weight: 700;">АИ</div>
                        <div style="flex: 1; color: #fff; font-size: 9pt;"><strong>Алексей Иванов</strong><br><span style="color: rgba(255,255,255,0.5); font-size: 8pt;">Senior Developer</span></div>
                        <span style="background: rgba(16,185,129,0.3); color: #10B981; padding: 1mm 3mm; border-radius: 2mm; font-size: 8pt;">Оффер</span>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.08); padding: 4mm; border-radius: 2mm; margin-bottom: 3mm;">
                    <div style="display: flex; align-items: center; gap: 3mm;">
                        <div style="width: 10mm; height: 10mm; background: {COLORS['primary']}; border-radius: 2mm; color: #fff; text-align: center; line-height: 10mm; font-size: 9pt; font-weight: 700;">МП</div>
                        <div style="flex: 1; color: #fff; font-size: 9pt;"><strong>Мария Петрова</strong><br><span style="color: rgba(255,255,255,0.5); font-size: 8pt;">Product Manager</span></div>
                        <span style="background: rgba(245,158,11,0.3); color: #F59E0B; padding: 1mm 3mm; border-radius: 2mm; font-size: 8pt;">Интервью</span>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.08); padding: 4mm; border-radius: 2mm;">
                    <div style="display: flex; align-items: center; gap: 3mm;">
                        <div style="width: 10mm; height: 10mm; background: {COLORS['primary']}; border-radius: 2mm; color: #fff; text-align: center; line-height: 10mm; font-size: 9pt; font-weight: 700;">ДС</div>
                        <div style="flex: 1; color: #fff; font-size: 9pt;"><strong>Дмитрий Сидоров</strong><br><span style="color: rgba(255,255,255,0.5); font-size: 8pt;">UX Designer</span></div>
                        <span style="background: rgba(79,106,245,0.3); color: {COLORS['primary']}; padding: 1mm 3mm; border-radius: 2mm; font-size: 8pt;">Скрининг</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">6</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 7: ИНТЕГРАЦИИ
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Интеграции</p>
    <h2>Подключено к экосистеме</h2>
    
    <div class="row">
        <div class="col col-2 gap-lg">
            <h4 class="mb-2">Job-сайты</h4>
            <div>
                <span class="integration-badge" style="background: #d6001c;">HeadHunter</span>
                <span class="integration-badge" style="background: #00a859;">Авито</span>
                <span class="integration-badge" style="background: #ff6600;">SuperJob</span>
                <span class="integration-badge" style="background: #0066cc;">Работа.ру</span>
            </div>
            
            <h4 class="mb-2 mt-3">Мессенджеры</h4>
            <div>
                <span class="integration-badge" style="background: #0088cc;">Telegram</span>
                <span class="integration-badge" style="background: #25d366;">WhatsApp</span>
                <span class="integration-badge" style="background: #7360f2;">Viber</span>
            </div>
        </div>
        <div class="col col-2">
            <h4 class="mb-2">Видеозвонки</h4>
            <div>
                <span class="integration-badge" style="background: #fc3f1d;">Яндекс.Телемост</span>
            </div>
            
            <h4 class="mb-2 mt-3">Корпоративные</h4>
            <div>
                <span class="integration-badge" style="background: #ffcc00; color: #000;">1С:Предприятие</span>
                <span class="integration-badge" style="background: #333;">Open API</span>
            </div>
            
            <div class="card card-filled mt-3" style="padding: 4mm;">
                <p class="text-small mb-0">Чаты HH и Авито прямо в системе — не нужно переключаться</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">7</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 8: AI
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-dark">
    <p class="tag tag-light">AI-модуль</p>
    <h2 style="color: #fff;">Искусственный интеллект в найме</h2>
    
    <div class="row mt-3">
        <div class="col col-4 gap-md">
            <div class="card-dark">
                <span class="icon icon-sm">🔍</span>
                <h4 style="color: #fff;">Умный поиск</h4>
                <p class="text-small" style="color: rgba(255,255,255,0.7);">Семантический поиск по базе, синонимы, похожие кандидаты</p>
            </div>
        </div>
        <div class="col col-4 gap-md">
            <div class="card-dark">
                <span class="icon icon-sm">🎯</span>
                <h4 style="color: #fff;">Матчинг</h4>
                <p class="text-small" style="color: rgba(255,255,255,0.7);">Оценка соответствия кандидата вакансии</p>
            </div>
        </div>
        <div class="col col-4 gap-md">
            <div class="card-dark">
                <span class="icon icon-sm">📊</span>
                <h4 style="color: #fff;">Ранжирование</h4>
                <p class="text-small" style="color: rgba(255,255,255,0.7);">Автоматическая сортировка по релевантности</p>
            </div>
        </div>
        <div class="col col-4">
            <div class="card-dark">
                <span class="icon icon-sm">📝</span>
                <h4 style="color: #fff;">Саммари</h4>
                <p class="text-small" style="color: rgba(255,255,255,0.7);">Краткое резюме кандидата за 20 секунд</p>
            </div>
        </div>
    </div>
    
    <div style="background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); padding: 4mm 6mm; border-radius: 2mm; margin-top: 8mm;">
        <p class="text-small mb-0" style="color: #F59E0B;">⚠️ AI ускоряет рутину и подсвечивает сигналы, но решение всегда за человеком</p>
    </div>
    
    <div class="footer" style="color: rgba(255,255,255,0.4);">
        <div class="footer-left"><span class="logo-box">W</span> <span style="color: #fff;">WorkHere</span></div>
        <div class="footer-right">8</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 9: АНАЛИТИКА
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Аналитика</p>
    <h2>Данные вместо догадок</h2>
    
    <div class="row">
        <div class="col col-2 gap-lg">
            <h4 class="mb-2">Воронка конверсий</h4>
            <div class="funnel-row">
                <div class="funnel-bar" style="width: 100%;">Отклики — 1000</div>
            </div>
            <div class="funnel-row">
                <div class="funnel-bar" style="width: 60%;">Скрининг — 600</div>
            </div>
            <div class="funnel-row">
                <div class="funnel-bar" style="width: 30%;">Интервью — 300</div>
            </div>
            <div class="funnel-row">
                <div class="funnel-bar" style="width: 15%;">Оффер — 150</div>
            </div>
            <div class="funnel-row">
                <div class="funnel-bar" style="width: 10%;">Выход — 100</div>
            </div>
        </div>
        <div class="col col-2">
            <div class="row">
                <div class="col col-2 gap-md">
                    <div class="card card-filled center">
                        <div class="stat-value">14</div>
                        <p class="text-small text-muted">дней до найма</p>
                        <p class="text-small text-primary" style="margin-top: 2mm;"><strong>↓ 40%</strong></p>
                    </div>
                </div>
                <div class="col col-2">
                    <div class="card card-filled center">
                        <div class="stat-value">12K</div>
                        <p class="text-small text-muted">₽ за найм</p>
                        <p class="text-small text-primary" style="margin-top: 2mm;"><strong>↓ 35%</strong></p>
                    </div>
                </div>
            </div>
            
            <div class="card card-filled mt-2">
                <h4>Источники</h4>
                <p class="text-small" style="margin-top: 2mm;">
                    <span style="color: #d6001c;">●</span> HH.ru — 45%<br>
                    <span style="color: #00a859;">●</span> Авито — 30%<br>
                    <span style="color: {COLORS['primary']};">●</span> Реферал — 25%
                </p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">9</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 10: БЕЗОПАСНОСТЬ
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Безопасность</p>
    <h2>Защита данных</h2>
    
    <div class="row">
        <div class="col col-3 gap-md">
            <div class="card card-filled center" style="height: 42mm;">
                <span class="icon">📜</span>
                <h4>ФЗ-152</h4>
                <p class="text-small">Полное соответствие закону о ПДн</p>
            </div>
        </div>
        <div class="col col-3 gap-md">
            <div class="card card-filled center" style="height: 42mm;">
                <span class="icon">✍️</span>
                <h4>Согласия</h4>
                <p class="text-small">Автосбор и хранение согласий</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled center" style="height: 42mm;">
                <span class="icon">👥</span>
                <h4>Роли</h4>
                <p class="text-small">Гибкое разграничение доступа</p>
            </div>
        </div>
    </div>
    
    <div class="row mt-2">
        <div class="col col-3 gap-md">
            <div class="card card-filled center" style="height: 42mm;">
                <span class="icon">📋</span>
                <h4>Аудит</h4>
                <p class="text-small">Логирование всех действий</p>
            </div>
        </div>
        <div class="col col-3 gap-md">
            <div class="card card-filled center" style="height: 42mm;">
                <span class="icon">🔒</span>
                <h4>Шифрование</h4>
                <p class="text-small">Данные зашифрованы</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled center" style="height: 42mm;">
                <span class="icon">🇷🇺</span>
                <h4>Реестр ПО</h4>
                <p class="text-small">Российское ПО</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">10</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 11: РЕЗУЛЬТАТЫ
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-primary">
    <p class="tag tag-light">Результаты</p>
    <h2 style="color: #fff;">Что получите</h2>
    
    <div class="row mt-3">
        <div class="col col-3 gap-md">
            <div class="card center">
                <div class="stat-value-lg">−40%</div>
                <p class="text-small text-muted">расходы на найм</p>
            </div>
        </div>
        <div class="col col-3 gap-md">
            <div class="card center">
                <div class="stat-value-lg">×4</div>
                <p class="text-small text-muted">производительность</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card center">
                <div class="stat-value-lg">−60%</div>
                <p class="text-small text-muted">время закрытия</p>
            </div>
        </div>
    </div>
    
    <div class="row mt-2">
        <div class="col col-3 gap-md">
            <div class="card center">
                <div class="stat-value-lg">×3</div>
                <p class="text-small text-muted">конверсия</p>
            </div>
        </div>
        <div class="col col-3 gap-md">
            <div class="card center">
                <div class="stat-value-lg">0</div>
                <p class="text-small text-muted">потерянных кандидатов</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card center">
                <div class="stat-value-lg">100%</div>
                <p class="text-small text-muted">прозрачность</p>
            </div>
        </div>
    </div>
    
    <div class="footer" style="color: rgba(255,255,255,0.5);">
        <div class="footer-left"><span class="logo-box" style="background: #fff; color: {COLORS['primary']};">W</span> <span style="color: #fff;">WorkHere</span></div>
        <div class="footer-right">11</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 12: ТАРИФЫ
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Тарифы</p>
    <h2>Прозрачное ценообразование</h2>
    
    <div class="row">
        <div class="col col-3 gap-md">
            <div class="pricing-card">
                <h4>Стандартный</h4>
                <div class="price">20 000 ₽</div>
                <div class="price-period">за лицензию / год</div>
                <ul class="list-check text-small" style="text-align: left;">
                    <li>Единая база</li>
                    <li>Все интеграции</li>
                    <li>Воронки и этапы</li>
                    <li>Аналитика</li>
                    <li>Поддержка 24/7</li>
                </ul>
            </div>
        </div>
        <div class="col col-3 gap-md">
            <div class="pricing-card featured">
                <span class="badge badge-primary" style="margin-bottom: 3mm;">Популярный</span>
                <h4>Премиум</h4>
                <div class="price">42 000 ₽</div>
                <div class="price-period">за лицензию / год</div>
                <ul class="list-check text-small" style="text-align: left;">
                    <li>Всё из Стандартного</li>
                    <li><strong>AI-модуль</strong></li>
                    <li>Умный поиск</li>
                    <li>Матчинг</li>
                    <li>Приоритетная поддержка</li>
                </ul>
            </div>
        </div>
        <div class="col col-3">
            <div class="pricing-card" style="border-color: {COLORS['accent']};">
                <h4>Руководители</h4>
                <div class="price" style="color: {COLORS['accent']};">Бесплатно</div>
                <div class="price-period">без ограничений</div>
                <ul class="list-check text-small" style="text-align: left;">
                    <li>Просмотр кандидатов</li>
                    <li>Согласования</li>
                    <li>Фидбек</li>
                    <li>Отчёты</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">12</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 13: ВНЕДРЕНИЕ
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Внедрение</p>
    <h2>Запуск за 1 день</h2>
    
    <div class="steps mt-4">
        <div class="step">
            <div class="step-num" style="font-size: 28pt;">30</div>
            <div class="step-desc">минут</div>
            <div class="step-title" style="margin-top: 3mm;">Демо</div>
        </div>
        <div class="step">
            <div class="step-num" style="font-size: 28pt;">1</div>
            <div class="step-desc">день</div>
            <div class="step-title" style="margin-top: 3mm;">Договор</div>
        </div>
        <div class="step">
            <div class="step-num" style="font-size: 28pt;">2–3</div>
            <div class="step-desc">дня</div>
            <div class="step-title" style="margin-top: 3mm;">Настройка</div>
        </div>
        <div class="step">
            <div class="step-num" style="font-size: 28pt;">1</div>
            <div class="step-desc">час</div>
            <div class="step-title" style="margin-top: 3mm;">Обучение</div>
        </div>
        <div class="step" style="background: {COLORS['primary_light']};">
            <div class="step-num" style="font-size: 28pt;">∞</div>
            <div class="step-desc">&nbsp;</div>
            <div class="step-title" style="margin-top: 3mm;">Поддержка 24/7</div>
        </div>
    </div>
    
    <div class="card card-filled mt-4" style="padding: 5mm 8mm;">
        <p class="mb-0">Персональный менеджер на всех этапах внедрения и работы с системой</p>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">13</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 14: КОНТАКТЫ
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide center">
    <p class="tag">Контакты</p>
    <h2>Начните сегодня</h2>
    
    <div class="row mt-3" style="max-width: 180mm; margin-left: auto; margin-right: auto;">
        <div class="col col-4 gap-md">
            <div class="card card-filled center" style="padding: 6mm;">
                <span class="icon icon-sm">🌐</span>
                <p class="text-small mb-0"><strong style="color: {COLORS['primary']};">workhere.ru</strong></p>
            </div>
        </div>
        <div class="col col-4 gap-md">
            <div class="card card-filled center" style="padding: 6mm;">
                <span class="icon icon-sm">✉️</span>
                <p class="text-small mb-0"><strong style="color: {COLORS['primary']};">info@workhere.ru</strong></p>
            </div>
        </div>
        <div class="col col-4 gap-md">
            <div class="card card-filled center" style="padding: 6mm;">
                <span class="icon icon-sm">📞</span>
                <p class="text-small mb-0"><strong style="color: {COLORS['primary']};">8 (800) 123-45-67</strong></p>
            </div>
        </div>
        <div class="col col-4">
            <div class="card card-filled center" style="padding: 6mm;">
                <span class="icon icon-sm">✈️</span>
                <p class="text-small mb-0"><strong style="color: {COLORS['primary']};">@workhere</strong></p>
            </div>
        </div>
    </div>
    
    <div style="margin-top: 12mm;">
        <span style="display: inline-block; background: {COLORS['primary']}; color: #fff; padding: 5mm 15mm; border-radius: 3mm; font-size: 14pt; font-weight: 600;">
            Записаться на демо →
        </span>
    </div>
    
    <div class="footer">
        <div class="footer-left"><span class="logo-box">W</span> <span class="logo">WorkHere</span></div>
        <div class="footer-right">14</div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 15: ФИНАЛ
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-dark center">
    <div style="padding-top: 30mm;">
        <h2 style="font-size: 32pt; color: #fff; line-height: 1.4; font-weight: 400;">
            ATS-систем много,<br>
            но вершину найма покоряет<br>
            <strong style="font-size: 40pt;">лишь одна</strong>
        </h2>
        
        <div style="margin-top: 15mm;">
            <span style="display: inline-block; width: 18mm; height: 18mm; background: {COLORS['primary']}; border-radius: 4mm; color: #fff; font-size: 28pt; font-weight: 700; line-height: 18mm; vertical-align: middle;">W</span>
            <span style="font-size: 36pt; font-weight: 700; margin-left: 5mm; vertical-align: middle;">WorkHere</span>
        </div>
        
        <p style="color: rgba(255,255,255,0.5); margin-top: 10mm; font-size: 14pt;">
            Ваши кандидаты уже ждут
        </p>
    </div>
</div>

</body>
</html>
"""

# ═══════════════════════════════════════════════════════════════
# GENERATE PDF
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Генерация PDF...")
    
    html = HTML(string=HTML_CONTENT)
    output_path = Path("WorkHere_Presentation.pdf")
    html.write_pdf(str(output_path))
    
    print(f"✅ PDF создан: {output_path}")
    print(f"   Размер: {output_path.stat().st_size / 1024:.0f} KB")
    
    import subprocess
    result = subprocess.run(['pdfinfo', str(output_path)], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Pages' in line:
            print(f"   {line.strip()}")
