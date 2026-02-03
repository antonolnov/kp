"""
Генерация PDF презентации WorkHere
Каждый слайд — отдельная страница A4 Landscape
"""

from weasyprint import HTML, CSS
from pathlib import Path

# CSS для PDF
CSS_STYLES = """
@page {
    size: A4 landscape;
    margin: 0;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    color: #1a1a2e;
    background: white;
}

.slide {
    width: 297mm;
    height: 210mm;
    padding: 30px 50px;
    page-break-after: always;
    position: relative;
    overflow: hidden;
}

.slide:last-child {
    page-break-after: avoid;
}

/* Backgrounds */
.bg-dark {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 100%);
    color: white;
}

.bg-gradient {
    background: linear-gradient(135deg, #597FFF 0%, #8BA3FF 100%);
    color: white;
}

.bg-light {
    background: #F8FAFF;
}

.bg-accent {
    background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
    color: white;
}

/* Typography */
h1 {
    font-size: 72pt;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 20px;
}

h2 {
    font-size: 42pt;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 30px;
}

h3 {
    font-size: 24pt;
    font-weight: 700;
    margin-bottom: 15px;
}

h4 {
    font-size: 18pt;
    font-weight: 600;
    margin-bottom: 10px;
}

p {
    font-size: 14pt;
    line-height: 1.5;
}

.tag {
    display: inline-block;
    background: rgba(89, 127, 255, 0.2);
    color: #597FFF;
    padding: 8px 20px;
    border-radius: 30px;
    font-size: 14pt;
    font-weight: 600;
    margin-bottom: 20px;
}

.tag-white {
    background: rgba(255, 255, 255, 0.2);
    color: white;
}

.gradient-text {
    color: #597FFF;
}

/* Layout */
.center {
    text-align: center;
}

.flex {
    display: flex;
    gap: 30px;
}

.flex-center {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
}

.grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 25px;
}

.grid-4 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 20px;
}

.grid-6 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr;
    gap: 15px;
}

/* Cards */
.card {
    background: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.card-dark {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 15px;
    padding: 25px;
}

.card-outline {
    background: transparent;
    border: 2px solid #E2E8F0;
    border-radius: 15px;
    padding: 25px;
}

.card-accent {
    background: #597FFF;
    color: white;
    border-radius: 15px;
    padding: 25px;
}

/* Stats */
.stat-value {
    font-size: 60pt;
    font-weight: 900;
    color: #597FFF;
    line-height: 1;
}

.stat-label {
    font-size: 14pt;
    color: #666;
    margin-top: 10px;
}

/* Icons */
.icon {
    font-size: 36pt;
    margin-bottom: 15px;
}

.icon-large {
    font-size: 60pt;
    margin-bottom: 20px;
}

/* Lists */
ul {
    list-style: none;
    padding: 0;
}

li {
    font-size: 14pt;
    padding: 8px 0;
    padding-left: 25px;
    position: relative;
}

li::before {
    content: '→';
    position: absolute;
    left: 0;
    color: #597FFF;
    font-weight: bold;
}

.check li::before {
    content: '✓';
    color: #10B981;
}

/* Tables */
.price-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

.price-table th {
    background: #597FFF;
    color: white;
    padding: 15px;
    text-align: left;
    font-size: 14pt;
}

.price-table td {
    padding: 15px;
    border-bottom: 1px solid #E2E8F0;
    font-size: 14pt;
}

.price-table tr:nth-child(even) {
    background: #F8FAFF;
}

/* Steps */
.steps {
    display: flex;
    gap: 10px;
    margin-top: 30px;
}

.step {
    flex: 1;
    background: #F8FAFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 20px 15px;
    text-align: center;
}

.step-num {
    font-size: 24pt;
    font-weight: 800;
    color: #597FFF;
}

.step-title {
    font-size: 11pt;
    font-weight: 700;
    margin: 8px 0 5px;
}

.step-desc {
    font-size: 10pt;
    color: #666;
}

/* Footer */
.slide-footer {
    position: absolute;
    bottom: 25px;
    left: 50px;
    right: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11pt;
    color: #999;
}

.logo-small {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
    color: #597FFF;
}

.logo-mark {
    width: 30px;
    height: 30px;
    background: #597FFF;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 900;
    font-size: 14pt;
}

/* Hero specific */
.hero-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
}

.hero-stats {
    display: flex;
    gap: 60px;
    margin-top: 40px;
}

.hero-stat-value {
    font-size: 36pt;
    font-weight: 800;
    color: #597FFF;
}

.hero-stat-label {
    font-size: 12pt;
    color: rgba(255,255,255,0.7);
}

/* Problem cards */
.problem-icon {
    font-size: 30pt;
    margin-bottom: 10px;
}

.problem-card {
    background: rgba(255,107,107,0.1);
    border: 1px solid rgba(255,107,107,0.3);
    border-radius: 12px;
    padding: 20px;
}

.problem-card h4 {
    color: #FF6B6B;
    font-size: 14pt;
}

.problem-card p {
    font-size: 11pt;
    color: #666;
}

/* Feature split */
.split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 50px;
    height: calc(100% - 80px);
    align-items: center;
}

/* Funnel */
.funnel-bar {
    height: 35px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 15px;
    margin-bottom: 8px;
    color: white;
    font-size: 12pt;
    font-weight: 600;
}

/* Pricing */
.pricing-card {
    background: white;
    border: 2px solid #E2E8F0;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
}

.pricing-card.featured {
    border-color: #597FFF;
    background: linear-gradient(135deg, rgba(89,127,255,0.05) 0%, rgba(89,127,255,0.1) 100%);
    transform: scale(1.05);
}

.pricing-card.free {
    border-color: #10B981;
    background: rgba(16,185,129,0.05);
}

.price-value {
    font-size: 36pt;
    font-weight: 900;
    color: #597FFF;
}

.price-period {
    font-size: 12pt;
    color: #666;
    margin-bottom: 20px;
}

.price-features {
    text-align: left;
    margin-bottom: 20px;
}

.price-btn {
    display: inline-block;
    background: #597FFF;
    color: white;
    padding: 12px 30px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 12pt;
}

/* Contact */
.contact-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 30px 0;
}

.contact-card {
    background: #F8FAFF;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
}

.cta-button {
    display: inline-block;
    background: linear-gradient(135deg, #597FFF 0%, #FF6B6B 100%);
    color: white;
    padding: 20px 60px;
    border-radius: 50px;
    font-size: 18pt;
    font-weight: 700;
    margin-top: 30px;
}
"""

# HTML слайдов
SLIDES_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>WorkHere — Презентация</title>
<style>
""" + CSS_STYLES + """
</style>
</head>
<body>

<!-- SLIDE 1: TITLE -->
<div class="slide bg-dark">
    <div class="hero-content">
        <div class="tag tag-white">🚀 ATS + CRM нового поколения</div>
        <h1>WorkHere</h1>
        <p style="font-size: 24pt; color: rgba(255,255,255,0.8); margin-bottom: 30px;">
            Система, которая закрывает вакансии<br>
            <span style="color: #597FFF;">пока другие только планируют</span>
        </p>
        <div class="hero-stats">
            <div>
                <div class="hero-stat-value">8500+</div>
                <div class="hero-stat-label">компаний</div>
            </div>
            <div>
                <div class="hero-stat-value">350+</div>
                <div class="hero-stat-label">городов</div>
            </div>
            <div>
                <div class="hero-stat-value">3 года</div>
                <div class="hero-stat-label">развития</div>
            </div>
        </div>
    </div>
</div>

<!-- SLIDE 2: PROBLEM -->
<div class="slide bg-light">
    <div class="tag">😤 Боль</div>
    <h2>Знакомо?</h2>
    <div class="grid-3">
        <div class="problem-card">
            <div class="problem-icon">📊</div>
            <h4>Excel-ад</h4>
            <p>Кандидаты в 15 разных таблицах, версии путаются</p>
        </div>
        <div class="problem-card">
            <div class="problem-icon">💬</div>
            <h4>Чат-хаос</h4>
            <p>Переписка в Telegram, WhatsApp, почте — ничего не найти</p>
        </div>
        <div class="problem-card">
            <div class="problem-icon">🔥</div>
            <h4>Горящие вакансии</h4>
            <p>Про кандидата забыли — ушёл к конкурентам</p>
        </div>
        <div class="problem-card">
            <div class="problem-icon">📉</div>
            <h4>Ноль аналитики</h4>
            <p>Не понятно, откуда приходят хорошие кандидаты</p>
        </div>
        <div class="problem-card">
            <div class="problem-icon">🤯</div>
            <h4>Рутина съедает</h4>
            <p>80% времени — на ручные операции</p>
        </div>
        <div class="problem-card">
            <div class="problem-icon">🔐</div>
            <h4>Риски ПДн</h4>
            <p>Согласия не собираются, 152-ФЗ под вопросом</p>
        </div>
    </div>
    <div class="slide-footer">
        <div class="logo-small"><div class="logo-mark">W</div> WorkHere</div>
        <span>2</span>
    </div>
</div>

<!-- SLIDE 3: SOLUTION -->
<div class="slide bg-gradient center">
    <div style="padding-top: 50px;">
        <div class="tag tag-white">💡 Решение</div>
        <h2 style="color: white;">Один WorkHere<br>заменяет всё</h2>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin: 40px 0;">
            <span style="background: rgba(255,255,255,0.2); padding: 15px 30px; border-radius: 10px; text-decoration: line-through; opacity: 0.7;">Excel</span>
            <span style="background: rgba(255,255,255,0.2); padding: 15px 30px; border-radius: 10px; text-decoration: line-through; opacity: 0.7;">Trello</span>
            <span style="background: rgba(255,255,255,0.2); padding: 15px 30px; border-radius: 10px; text-decoration: line-through; opacity: 0.7;">Notion</span>
            <span style="background: rgba(255,255,255,0.2); padding: 15px 30px; border-radius: 10px; text-decoration: line-through; opacity: 0.7;">Google Sheets</span>
            <span style="background: rgba(255,255,255,0.2); padding: 15px 30px; border-radius: 10px; text-decoration: line-through; opacity: 0.7;">amoCRM</span>
        </div>
        <div style="font-size: 48pt; margin: 30px 0;">↓</div>
        <div style="display: inline-flex; align-items: center; gap: 15px; background: white; color: #597FFF; padding: 20px 40px; border-radius: 15px; font-size: 24pt; font-weight: 800;">
            <div style="width: 50px; height: 50px; background: #597FFF; color: white; border-radius: 12px; display: flex; align-items: center; justify-content: center;">W</div>
            WorkHere
        </div>
    </div>
</div>

<!-- SLIDE 4: AUDIENCE -->
<div class="slide bg-light">
    <div class="tag">👥 Аудитория</div>
    <h2>Для тех, кто нанимает</h2>
    <div class="grid-4">
        <div class="card">
            <div class="icon">👨‍💼</div>
            <h4>Рекрутер</h4>
            <ul>
                <li>Работа с откликами в один клик</li>
                <li>Автоматизация рутины</li>
                <li>История по каждому кандидату</li>
            </ul>
        </div>
        <div class="card-accent">
            <div class="icon">👩‍💼</div>
            <h4>Руководитель подбора</h4>
            <ul style="color: rgba(255,255,255,0.9);">
                <li style="color: white;">Контроль SLA и дедлайнов</li>
                <li style="color: white;">Аналитика по рекрутерам</li>
                <li style="color: white;">Отчёты для топов</li>
            </ul>
        </div>
        <div class="card">
            <div class="icon">🧑‍💻</div>
            <h4>Нанимающий менеджер</h4>
            <ul>
                <li>Быстрый фидбек</li>
                <li>Согласование кандидатов</li>
                <li>Уведомления в Telegram</li>
            </ul>
        </div>
        <div class="card">
            <div class="icon">📊</div>
            <h4>HRD / Бизнес</h4>
            <ul>
                <li>Стоимость найма</li>
                <li>Прогнозирование</li>
                <li>Качество источников</li>
            </ul>
        </div>
    </div>
    <div class="slide-footer">
        <div class="logo-small"><div class="logo-mark">W</div> WorkHere</div>
        <span>4</span>
    </div>
</div>

<!-- SLIDE 5: FUNNEL -->
<div class="slide bg-dark">
    <div class="tag tag-white">🎯 Процесс</div>
    <h2 style="color: white;">Полный цикл найма</h2>
    <div class="steps">
        <div class="step" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2);">
            <div class="step-num">01</div>
            <div class="step-title" style="color: white;">Заявка</div>
            <div class="step-desc" style="color: rgba(255,255,255,0.6);">От менеджера</div>
        </div>
        <div class="step" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2);">
            <div class="step-num">02</div>
            <div class="step-title" style="color: white;">Публикация</div>
            <div class="step-desc" style="color: rgba(255,255,255,0.6);">На job-сайтах</div>
        </div>
        <div class="step" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2);">
            <div class="step-num">03</div>
            <div class="step-title" style="color: white;">Отклики</div>
            <div class="step-desc" style="color: rgba(255,255,255,0.6);">Единый поток</div>
        </div>
        <div class="step" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2);">
            <div class="step-num">04</div>
            <div class="step-title" style="color: white;">Скрининг</div>
            <div class="step-desc" style="color: rgba(255,255,255,0.6);">+ AI</div>
        </div>
        <div class="step" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.2);">
            <div class="step-num">05</div>
            <div class="step-title" style="color: white;">Интервью</div>
            <div class="step-desc" style="color: rgba(255,255,255,0.6);">Телемост</div>
        </div>
        <div class="step" style="background: rgba(89,127,255,0.3); border-color: #597FFF;">
            <div class="step-num">06</div>
            <div class="step-title" style="color: white;">Оффер</div>
            <div class="step-desc" style="color: rgba(255,255,255,0.6);">Выход</div>
        </div>
    </div>
    <div class="slide-footer" style="color: rgba(255,255,255,0.5);">
        <div class="logo-small"><div class="logo-mark">W</div> <span style="color: white;">WorkHere</span></div>
        <span>5</span>
    </div>
</div>

<!-- SLIDE 6: DATABASE -->
<div class="slide bg-light">
    <div class="split">
        <div>
            <div class="tag">📁 Функция #1</div>
            <h2>Единая база кандидатов</h2>
            <ul class="check" style="font-size: 16pt;">
                <li>Все резюме в одном месте</li>
                <li>Полная история взаимодействий</li>
                <li>Комментарии и теги</li>
                <li>Умный поиск по тексту резюме</li>
                <li>Защита от дублей</li>
                <li>Слияние карточек</li>
            </ul>
            <div style="background: rgba(89,127,255,0.1); border-left: 4px solid #597FFF; padding: 15px 20px; margin-top: 20px; border-radius: 0 10px 10px 0;">
                💡 Больше никаких потерянных кандидатов в переписках!
            </div>
        </div>
        <div style="background: #1a1a2e; border-radius: 15px; padding: 20px;">
            <div style="display: flex; gap: 8px; margin-bottom: 15px;">
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f57;"></span>
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #febc2e;"></span>
                <span style="width: 12px; height: 12px; border-radius: 50%; background: #28c840;"></span>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center; gap: 15px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #597FFF, #FF6B6B); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700;">АИ</div>
                <div style="flex: 1; color: white;"><strong>Алексей Иванов</strong><br><span style="font-size: 11pt; color: rgba(255,255,255,0.5);">Senior Developer</span></div>
                <span style="background: rgba(40,200,64,0.2); color: #28c840; padding: 5px 12px; border-radius: 20px; font-size: 11pt;">Оффер</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center; gap: 15px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #597FFF, #FF6B6B); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700;">МП</div>
                <div style="flex: 1; color: white;"><strong>Мария Петрова</strong><br><span style="font-size: 11pt; color: rgba(255,255,255,0.5);">Product Manager</span></div>
                <span style="background: rgba(254,188,46,0.2); color: #febc2e; padding: 5px 12px; border-radius: 20px; font-size: 11pt;">Интервью</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; display: flex; align-items: center; gap: 15px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #597FFF, #FF6B6B); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700;">ДС</div>
                <div style="flex: 1; color: white;"><strong>Дмитрий Сидоров</strong><br><span style="font-size: 11pt; color: rgba(255,255,255,0.5);">UX Designer</span></div>
                <span style="background: rgba(89,127,255,0.2); color: #597FFF; padding: 5px 12px; border-radius: 20px; font-size: 11pt;">Скрининг</span>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <div class="logo-small"><div class="logo-mark">W</div> WorkHere</div>
        <span>6</span>
    </div>
</div>

<!-- SLIDE 7: INTEGRATIONS -->
<div class="slide bg-light">
    <div class="tag">🔗 Интеграции</div>
    <h2>Подключено к экосистеме</h2>
    <div class="grid-2" style="margin-top: 30px;">
        <div class="card">
            <h4>Job-сайты</h4>
            <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-top: 15px;">
                <div style="background: #d6001c; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700;">hh HeadHunter</div>
                <div style="background: #00a859; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700;">A Авито</div>
                <div style="background: #ff6600; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700;">SJ SuperJob</div>
                <div style="background: #0066cc; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700;">R Работа.ру</div>
            </div>
        </div>
        <div class="card">
            <h4>Мессенджеры</h4>
            <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-top: 15px;">
                <div style="background: #0088cc; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700;">✈ Telegram</div>
                <div style="background: #25d366; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700;">📱 WhatsApp</div>
                <div style="background: #7360f2; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700;">📞 Viber</div>
            </div>
        </div>
        <div class="card">
            <h4>Видеозвонки</h4>
            <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-top: 15px;">
                <div style="background: #fc3f1d; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700;">Я Яндекс.Телемост</div>
            </div>
        </div>
        <div class="card">
            <h4>Корпоративные</h4>
            <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-top: 15px;">
                <div style="background: #ffcc00; color: #000; padding: 10px 20px; border-radius: 8px; font-weight: 700;">1С Предприятие</div>
                <div style="background: #333; color: white; padding: 10px 20px; border-radius: 8px; font-weight: 700;">{ } Open API</div>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <div class="logo-small"><div class="logo-mark">W</div> WorkHere</div>
        <span>7</span>
    </div>
</div>

<!-- SLIDE 8: AI -->
<div class="slide bg-dark">
    <div class="tag tag-white">🤖 AI-модуль</div>
    <h2 style="color: white;">Искусственный интеллект<br><span style="color: #597FFF;">в найме</span></h2>
    <div class="grid-4" style="margin-top: 30px;">
        <div class="card-dark">
            <div class="icon">🔍</div>
            <h4 style="color: white;">Умный поиск</h4>
            <p style="color: rgba(255,255,255,0.7); font-size: 12pt;">Семантический поиск, синонимы, похожие кандидаты</p>
        </div>
        <div class="card-dark">
            <div class="icon">🎯</div>
            <h4 style="color: white;">Матчинг</h4>
            <p style="color: rgba(255,255,255,0.7); font-size: 12pt;">Оценка соответствия кандидат ↔ вакансия</p>
        </div>
        <div class="card-dark">
            <div class="icon">📊</div>
            <h4 style="color: white;">Ранжирование</h4>
            <p style="color: rgba(255,255,255,0.7); font-size: 12pt;">Автоматическая сортировка по релевантности</p>
        </div>
        <div class="card-dark">
            <div class="icon">📝</div>
            <h4 style="color: white;">Саммари</h4>
            <p style="color: rgba(255,255,255,0.7); font-size: 12pt;">Суть кандидата за 20 секунд</p>
        </div>
    </div>
    <div style="background: rgba(255,230,109,0.1); border: 1px solid rgba(255,230,109,0.3); padding: 15px 25px; border-radius: 10px; margin-top: 30px; text-align: center; color: #FFE66D;">
        ⚠️ AI ускоряет рутину, но решение всегда за человеком
    </div>
    <div class="slide-footer" style="color: rgba(255,255,255,0.5);">
        <div class="logo-small"><div class="logo-mark">W</div> <span style="color: white;">WorkHere</span></div>
        <span>8</span>
    </div>
</div>

<!-- SLIDE 9: ANALYTICS -->
<div class="slide bg-light">
    <div class="tag">📊 Аналитика</div>
    <h2>Данные вместо догадок</h2>
    <div class="grid-2">
        <div class="card">
            <h4>Воронка конверсий</h4>
            <div style="margin-top: 15px;">
                <div class="funnel-bar" style="width: 100%; background: linear-gradient(90deg, #597FFF, #FF6B6B);"><span>Отклики</span><span>1000</span></div>
                <div class="funnel-bar" style="width: 60%; background: linear-gradient(90deg, #597FFF, #FF6B6B);"><span>Скрининг</span><span>600</span></div>
                <div class="funnel-bar" style="width: 30%; background: linear-gradient(90deg, #597FFF, #FF6B6B);"><span>Интервью</span><span>300</span></div>
                <div class="funnel-bar" style="width: 15%; background: linear-gradient(90deg, #597FFF, #FF6B6B);"><span>Оффер</span><span>150</span></div>
                <div class="funnel-bar" style="width: 10%; background: linear-gradient(90deg, #597FFF, #FF6B6B);"><span>Выход</span><span>100</span></div>
            </div>
        </div>
        <div>
            <div class="grid-2">
                <div class="card center">
                    <div class="stat-value">14</div>
                    <div class="stat-label">дней Time to Hire</div>
                    <div style="color: #10B981; font-weight: 600; margin-top: 5px;">↓ 40% быстрее</div>
                </div>
                <div class="card center">
                    <div class="stat-value">12K</div>
                    <div class="stat-label">₽ стоимость найма</div>
                    <div style="color: #10B981; font-weight: 600; margin-top: 5px;">↓ 35% дешевле</div>
                </div>
            </div>
            <div class="card" style="margin-top: 20px;">
                <h4>Источники</h4>
                <div style="margin-top: 10px;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <span style="width: 12px; height: 12px; border-radius: 50%; background: #d6001c;"></span>
                        HH.ru — 45%
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <span style="width: 12px; height: 12px; border-radius: 50%; background: #00a859;"></span>
                        Авито — 30%
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="width: 12px; height: 12px; border-radius: 50%; background: #597FFF;"></span>
                        Реферал — 25%
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <div class="logo-small"><div class="logo-mark">W</div> WorkHere</div>
        <span>9</span>
    </div>
</div>

<!-- SLIDE 10: SECURITY -->
<div class="slide bg-light">
    <div class="tag">🔐 Безопасность</div>
    <h2>Защита данных</h2>
    <div class="grid-3">
        <div class="card center">
            <div class="icon-large">📜</div>
            <h4>ФЗ-152</h4>
            <p>Полное соответствие закону о персональных данных</p>
        </div>
        <div class="card center">
            <div class="icon-large">✍️</div>
            <h4>Согласия</h4>
            <p>Автоматический запрос и хранение согласий на обработку ПД</p>
        </div>
        <div class="card center">
            <div class="icon-large">👥</div>
            <h4>Роли и доступы</h4>
            <p>Гибкое разграничение прав по подразделениям</p>
        </div>
        <div class="card center">
            <div class="icon-large">📋</div>
            <h4>Аудит</h4>
            <p>Логирование всех действий: кто, что, когда изменил</p>
        </div>
        <div class="card center">
            <div class="icon-large">🔒</div>
            <h4>Шифрование</h4>
            <p>Данные зашифрованы при хранении и передаче</p>
        </div>
        <div class="card center">
            <div class="icon-large">🇷🇺</div>
            <h4>Российское ПО</h4>
            <p>В реестре отечественного софта</p>
        </div>
    </div>
    <div class="slide-footer">
        <div class="logo-small"><div class="logo-mark">W</div> WorkHere</div>
        <span>10</span>
    </div>
</div>

<!-- SLIDE 11: RESULTS -->
<div class="slide bg-gradient center">
    <div style="padding-top: 30px;">
        <div class="tag tag-white">🏆 Результаты</div>
        <h2 style="color: white;">Что получите</h2>
        <div class="grid-3" style="margin-top: 40px;">
            <div class="card center">
                <div class="stat-value" style="font-size: 48pt;">-40%</div>
                <div class="stat-label">расходы на найм</div>
            </div>
            <div class="card center">
                <div class="stat-value" style="font-size: 48pt;">×4</div>
                <div class="stat-label">производительность рекрутера</div>
            </div>
            <div class="card center">
                <div class="stat-value" style="font-size: 48pt;">-60%</div>
                <div class="stat-label">срок закрытия вакансии</div>
            </div>
            <div class="card center">
                <div class="stat-value" style="font-size: 48pt;">×3</div>
                <div class="stat-label">конверсия до оффера</div>
            </div>
            <div class="card center">
                <div class="stat-value" style="font-size: 48pt;">0%</div>
                <div class="stat-label">потерянных кандидатов</div>
            </div>
            <div class="card center">
                <div class="stat-value" style="font-size: 48pt;">100%</div>
                <div class="stat-label">прозрачность процесса</div>
            </div>
        </div>
    </div>
</div>

<!-- SLIDE 12: PRICING -->
<div class="slide bg-light">
    <div class="tag">💰 Тарифы</div>
    <h2>Прозрачное ценообразование</h2>
    <div class="grid-3" style="margin-top: 20px;">
        <div class="pricing-card">
            <h3>Стандартный</h3>
            <div class="price-value">20 000 ₽</div>
            <div class="price-period">за лицензию / год</div>
            <ul class="check price-features">
                <li>Единая база кандидатов</li>
                <li>Все интеграции</li>
                <li>Воронки и этапы</li>
                <li>Аналитика</li>
                <li>Мобильное приложение</li>
                <li>Поддержка 24/7</li>
            </ul>
        </div>
        <div class="pricing-card featured">
            <div style="background: linear-gradient(135deg, #597FFF, #FF6B6B); color: white; padding: 5px 20px; border-radius: 20px; font-size: 11pt; font-weight: 600; position: absolute; top: -12px; left: 50%; transform: translateX(-50%);">Популярный</div>
            <h3>Премиум</h3>
            <div class="price-value">42 000 ₽</div>
            <div class="price-period">за лицензию / год</div>
            <ul class="check price-features">
                <li>Всё из Стандартного</li>
                <li><strong>AI-модуль</strong></li>
                <li>Умный поиск кандидатов</li>
                <li>Матчинг и ранжирование</li>
                <li>Саммари резюме</li>
                <li>Приоритетная поддержка</li>
            </ul>
        </div>
        <div class="pricing-card free">
            <h3>Руководители</h3>
            <div class="price-value" style="color: #10B981;">Бесплатно</div>
            <div class="price-period">без ограничений</div>
            <ul class="check price-features">
                <li>Просмотр кандидатов</li>
                <li>Согласования</li>
                <li>Фидбек</li>
                <li>Отчёты</li>
            </ul>
        </div>
    </div>
    <div class="slide-footer">
        <div class="logo-small"><div class="logo-mark">W</div> WorkHere</div>
        <span>12</span>
    </div>
</div>

<!-- SLIDE 13: ONBOARDING -->
<div class="slide bg-light">
    <div class="tag">🚀 Внедрение</div>
    <h2>Запуск за 1 день</h2>
    <div class="steps" style="margin-top: 50px;">
        <div class="step">
            <div class="step-num" style="font-size: 36pt;">30</div>
            <div class="step-title">минут</div>
            <div style="font-size: 14pt; font-weight: 600; margin-top: 10px;">Демо</div>
            <div class="step-desc">Показываем систему</div>
        </div>
        <div class="step">
            <div class="step-num" style="font-size: 36pt;">1</div>
            <div class="step-title">день</div>
            <div style="font-size: 14pt; font-weight: 600; margin-top: 10px;">Договор</div>
            <div class="step-desc">Подписание и оплата</div>
        </div>
        <div class="step">
            <div class="step-num" style="font-size: 36pt;">2-3</div>
            <div class="step-title">дня</div>
            <div style="font-size: 14pt; font-weight: 600; margin-top: 10px;">Настройка</div>
            <div class="step-desc">Импорт базы, воронки</div>
        </div>
        <div class="step">
            <div class="step-num" style="font-size: 36pt;">1</div>
            <div class="step-title">час</div>
            <div style="font-size: 14pt; font-weight: 600; margin-top: 10px;">Обучение</div>
            <div class="step-desc">Онлайн-сессия</div>
        </div>
        <div class="step" style="background: rgba(89,127,255,0.1); border-color: #597FFF;">
            <div class="step-num" style="font-size: 36pt;">∞</div>
            <div class="step-title"></div>
            <div style="font-size: 14pt; font-weight: 600; margin-top: 10px;">Поддержка</div>
            <div class="step-desc">24/7 помощь</div>
        </div>
    </div>
    <div class="slide-footer">
        <div class="logo-small"><div class="logo-mark">W</div> WorkHere</div>
        <span>13</span>
    </div>
</div>

<!-- SLIDE 14: CONTACT -->
<div class="slide bg-light center">
    <div class="tag">📞 Контакты</div>
    <h2>Начните сегодня</h2>
    <div class="contact-grid">
        <div class="contact-card">
            <div class="icon">🌐</div>
            <h4>Сайт</h4>
            <p style="color: #597FFF; font-weight: 600;">workhere.ru</p>
        </div>
        <div class="contact-card">
            <div class="icon">✉️</div>
            <h4>Email</h4>
            <p style="color: #597FFF; font-weight: 600;">info@workhere.ru</p>
        </div>
        <div class="contact-card">
            <div class="icon">📞</div>
            <h4>Телефон</h4>
            <p style="color: #597FFF; font-weight: 600;">8 (800) 123-45-67</p>
        </div>
        <div class="contact-card">
            <div class="icon">✈️</div>
            <h4>Telegram</h4>
            <p style="color: #597FFF; font-weight: 600;">@workhere</p>
        </div>
    </div>
    <div class="cta-button">🚀 Записаться на демо</div>
    <div class="slide-footer">
        <div class="logo-small"><div class="logo-mark">W</div> WorkHere</div>
        <span>14</span>
    </div>
</div>

<!-- SLIDE 15: FINAL -->
<div class="slide bg-dark center">
    <div style="padding-top: 60px;">
        <h2 style="color: white; font-size: 36pt; line-height: 1.4;">
            HRM-систем много,<br>
            но вершину найма покоряет<br>
            <span style="background: linear-gradient(90deg, #597FFF, #FF6B6B, #FFE66D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 48pt;">лишь одна</span>
        </h2>
        <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-top: 50px;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #597FFF, #FF6B6B); border-radius: 20px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 36pt;">W</div>
            <span style="font-size: 48pt; font-weight: 900; color: white;">WorkHere</span>
        </div>
        <p style="color: rgba(255,255,255,0.6); font-size: 18pt; margin-top: 30px;">Ваши кандидаты уже ждут</p>
    </div>
</div>

</body>
</html>
"""

# Генерация PDF
print("Генерация PDF...")
html = HTML(string=SLIDES_HTML)
html.write_pdf('WorkHere_Presentation.pdf')
print(f"✅ PDF создан: WorkHere_Presentation.pdf")

# Проверка
import subprocess
result = subprocess.run(['pdfinfo', 'WorkHere_Presentation.pdf'], capture_output=True, text=True)
for line in result.stdout.split('\n')[:5]:
    print(line)
