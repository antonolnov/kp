"""
PDF Generator for personalized commercial proposals
"""
import logging
from pathlib import Path
from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from config import TEMPLATES_DIR, ASSETS_DIR, PRICING
from .ai_analyzer import MeetingAnalysis

logger = logging.getLogger(__name__)


# Feature icons mapping
FEATURE_ICONS = {
    # Интеграции
    "Интеграции с job-сайтами": "🔗",
    "Интеграции с job-сайтами (HH, Авито)": "🔗",
    "Интеграции": "🔗",
    "HH.ru": "🔗",
    "Авито": "🔗",
    
    # Коммуникации
    "Коммуникации": "💬",
    "Коммуникации в одном окне": "💬",
    "Мессенджеры": "💬",
    "Мессенджеры (WhatsApp, Telegram)": "💬",
    "WhatsApp": "💬",
    
    # Воронка
    "Воронка подбора": "📊",
    "Воронка": "📊",
    
    # Телефония
    "Телефония": "📞",
    "IP-телефония": "📞",
    "IP-телефония с записью звонков": "📞",
    
    # Аналитика
    "Аналитика": "📈",
    "Аналитика и отчёты": "📈",
    "Отчёты": "📈",
    
    # Календарь
    "Календарь": "📅",
    "Календарь собеседований": "📅",
    "Календарь с интеграцией Телемост": "📅",
    "Телемост": "📅",
    
    # Заказчики
    "Заказчики": "👥",
    "Работа с заказчиками": "👥",
    "Работа с внутренними заказчиками": "👥",
    
    # ФЗ-152
    "ФЗ-152": "🛡️",
    "Соответствие ФЗ-152": "🛡️",
    "Персональные данные": "🛡️",
    
    # AI
    "AI": "🤖",
    "ИИ-поиск": "🤖",
    "AI-поиск": "🤖",
    
    # Уведомления
    "Уведомления": "🔔",
    "Telegram-бот": "🔔",
    "Telegram-бот для уведомлений": "🔔",
    "Напоминания": "🔔",
    
    # База
    "База кандидатов": "📁",
    "Единая база": "📁",
    
    # Автоматизация
    "Автоматизация": "⚡",
    
    # Мобильное
    "Мобильное приложение": "📱",
}


@dataclass
class ProposalConfig:
    """Configuration for proposal generation"""
    show_standard: bool = True
    show_premium: bool = False
    show_ai_option: bool = False
    num_recruiters: int = 1


def generate_proposal_pdf(
    analysis: MeetingAnalysis,
    config: ProposalConfig,
    output_path: Path
) -> Path:
    """Generate personalized PDF proposal"""
    
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("proposal.html")
    
    # Create highlighted features string for template matching
    highlighted_str = " ".join(analysis.discussed_features)
    
    # Calculate pricing
    calculations = []
    total = 0
    
    if config.show_standard and config.show_premium:
        # Both tariffs
        std_price = PRICING["standard"]["price_per_license"] * config.num_recruiters
        prem_price = PRICING["premium"]["price_per_license"] * config.num_recruiters
        
        calculations.append({
            "name": f"Стандартный: {config.num_recruiters} × 20 000 ₽",
            "value": f"{std_price:,} ₽".replace(",", " ")
        })
        
        if config.show_ai_option:
            ai_price = PRICING["ai_search"]["price_yearly"]
            calculations.append({
                "name": "+ ИИ-поиск (опционально)",
                "value": f"+{ai_price:,} ₽/год".replace(",", " ")
            })
        
        calculations.append({
            "name": f"Премиум: {config.num_recruiters} × 42 000 ₽",
            "value": f"{prem_price:,} ₽".replace(",", " ")
        })
        
        total = f"от {std_price:,} до {prem_price:,}".replace(",", " ")
        
    elif config.show_premium:
        price = PRICING["premium"]["price_per_license"] * config.num_recruiters
        calculations.append({
            "name": f"Премиум тариф × {config.num_recruiters}",
            "value": f"{price:,} ₽".replace(",", " ")
        })
        total = f"{price:,}".replace(",", " ")
        
    else:  # Standard only
        price = PRICING["standard"]["price_per_license"] * config.num_recruiters
        calculations.append({
            "name": f"Стандартный тариф × {config.num_recruiters}",
            "value": f"{price:,} ₽".replace(",", " ")
        })
        total = price
        
        if config.show_ai_option:
            ai_price = PRICING["ai_search"]["price_yearly"]
            calculations.append({
                "name": "ИИ-поиск кандидатов (год)",
                "value": f"{ai_price:,} ₽".replace(",", " ")
            })
            total += ai_price
        
        total = f"{total:,}".replace(",", " ")
    
    # Ensure we have defaults
    pain_points = analysis.current_pain_points or [
        "Работа ведётся в нескольких системах",
        "Много времени уходит на рутинные операции",
        "Нет единой картины по подбору"
    ]
    
    needs = analysis.needs or [
        "Объединить все инструменты в одной системе",
        "Автоматизировать рутинные задачи",
        "Получить прозрачную аналитику"
    ]
    
    discussed = analysis.discussed_features or [
        "Интеграции с job-сайтами",
        "Воронка подбора",
        "Аналитика и отчёты"
    ]
    
    # Render HTML
    html_content = template.render(
        logo_path=str(ASSETS_DIR / "logo.png"),
        company_name=analysis.company_name,
        contact_name=analysis.contact_name,
        contact_role=getattr(analysis, 'contact_role', ''),
        industry=getattr(analysis, 'industry', ''),
        summary=analysis.summary,
        hiring_situation=analysis.hiring_situation,
        pain_points=pain_points,
        needs=needs,
        discussed_features=discussed,
        feature_icons=FEATURE_ICONS,
        highlighted_str=highlighted_str,
        show_standard=config.show_standard,
        show_premium=config.show_premium,
        show_ai_option=config.show_ai_option,
        num_recruiters=config.num_recruiters,
        calculations=calculations,
        total_price=total,
    )
    
    # Generate PDF
    html = HTML(string=html_content, base_url=str(ASSETS_DIR))
    html.write_pdf(str(output_path))
    
    logger.info(f"Generated PDF: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    
    return output_path
