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
    
    # Use num_recruiters from analysis if not explicitly set
    num_recruiters = config.num_recruiters if config.num_recruiters > 1 else analysis.num_recruiters
    if num_recruiters < 1:
        num_recruiters = 1
    
    # Calculate pricing
    calculations = []
    total = 0
    
    if config.show_standard and config.show_premium:
        # Both tariffs
        std_price = PRICING["standard"]["price_per_license"] * num_recruiters
        prem_price = PRICING["premium"]["price_per_license"] * num_recruiters
        
        calculations.append({
            "name": f"Стандартный тариф ({num_recruiters} × 20 000 ₽)",
            "value": f"{std_price:,} ₽/год".replace(",", " ")
        })
        
        if config.show_ai_option:
            ai_price = PRICING["ai_search"]["price_yearly"]
            calculations.append({
                "name": "ИИ-поиск кандидатов (опционально)",
                "value": f"+{ai_price:,} ₽/год".replace(",", " ")
            })
        
        calculations.append({
            "name": f"Премиум тариф ({num_recruiters} × 42 000 ₽, AI включён)",
            "value": f"{prem_price:,} ₽/год".replace(",", " ")
        })
        
        total = f"от {std_price:,} до {prem_price:,}".replace(",", " ")
        
    elif config.show_premium:
        price = PRICING["premium"]["price_per_license"] * num_recruiters
        calculations.append({
            "name": f"Премиум тариф ({num_recruiters} × 42 000 ₽)",
            "value": f"{price:,} ₽/год".replace(",", " ")
        })
        total = f"{price:,}".replace(",", " ")
        
    else:  # Standard only
        price = PRICING["standard"]["price_per_license"] * num_recruiters
        calculations.append({
            "name": f"Стандартный тариф ({num_recruiters} × 20 000 ₽)",
            "value": f"{price:,} ₽/год".replace(",", " ")
        })
        total = price
        
        if config.show_ai_option:
            ai_price = PRICING["ai_search"]["price_yearly"]
            calculations.append({
                "name": "ИИ-поиск кандидатов (год)",
                "value": f"+{ai_price:,} ₽/год".replace(",", " ")
            })
            total += ai_price
        
        total = f"{total:,}".replace(",", " ")
    
    # Ensure we have good defaults for discussed_features
    discussed = analysis.discussed_features or []
    if len(discussed) < 6:
        defaults = [
            "Единая база кандидатов: все контакты, резюме и история взаимодействий в одном месте",
            "Интеграции с работными сайтами: HH.ru, Авито, SuperJob — автоматический сбор откликов",
            "Настраиваемые воронки и статусы под ваши процессы",
            "Аналитика и отчёты: конверсии, источники, Time-to-Hire",
            "Коммуникации с кандидатами через мессенджеры (WhatsApp, Telegram)",
            "Telegram-бот для уведомлений и напоминаний о собеседованиях"
        ]
        for d in defaults:
            if d not in discussed and len(discussed) < 8:
                discussed.append(d)
    
    pain_points = analysis.current_pain_points or [
        "Работа ведётся в нескольких инструментах, нет единой системы",
        "Много времени уходит на ручной перенос данных и рутину",
        "Отсутствует прозрачная аналитика по процессу подбора"
    ]
    
    # Render HTML
    html_content = template.render(
        logo_path=str(ASSETS_DIR / "logo.png"),
        mascot_path=str(ASSETS_DIR / "mascot.svg"),
        company_name=analysis.company_name or "",
        contact_name=analysis.contact_name or "",
        contact_role=analysis.contact_role or "",
        industry=analysis.industry or "",
        summary=analysis.summary or "",
        hiring_situation=analysis.hiring_situation or "",
        pain_points=pain_points,
        discussed_features=discussed,
        show_standard=config.show_standard,
        show_premium=config.show_premium,
        show_ai_option=config.show_ai_option,
        num_recruiters=num_recruiters,
        calculations=calculations,
        total_price=total,
    )
    
    # Generate PDF
    html = HTML(string=html_content, base_url=str(ASSETS_DIR))
    html.write_pdf(str(output_path))
    
    logger.info(f"Generated PDF: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    
    return output_path
