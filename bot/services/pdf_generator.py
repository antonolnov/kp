"""
PDF Generator for personalized commercial proposals
"""
import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from config import TEMPLATES_DIR, ASSETS_DIR, PRICING
from .ai_analyzer import MeetingAnalysis

logger = logging.getLogger(__name__)


# Feature icons mapping
FEATURE_ICONS = {
    "База кандидатов": "📁",
    "Интеграции": "🔗",
    "Интеграции с job-сайтами": "🔗",
    "HH.ru": "🔗",
    "Коммуникации": "💬",
    "Коммуникации в одном окне": "💬",
    "Воронка": "📊",
    "Воронка подбора": "📊",
    "Автоматизация": "⚡",
    "Аналитика": "📈",
    "Дашборды": "📈",
    "AI": "🤖",
    "ИИ": "🤖",
    "AI-поиск": "🤖",
    "Семантический поиск": "🔍",
    "Календарь": "📅",
    "Мобильное": "📱",
    "Документы": "📄",
    "КЭДО": "📄",
    "Офферы": "📄",
    "Talent pool": "👥",
    "Кадровый резерв": "👥",
    "Скоринг": "🎯",
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
    """
    Generate personalized PDF proposal
    
    Args:
        analysis: Meeting analysis data
        config: Proposal configuration
        output_path: Where to save the PDF
        
    Returns:
        Path to generated PDF
    """
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("proposal.html")
    
    # Prepare highlighted features
    highlighted_features = set()
    for feature in analysis.discussed_features:
        for key in FEATURE_ICONS.keys():
            if key.lower() in feature.lower() or feature.lower() in key.lower():
                highlighted_features.add(key)
    
    highlighted_features_str = " ".join(analysis.discussed_features).lower()
    
    # Calculate pricing
    calculations = []
    total = 0
    
    if config.show_premium:
        price = PRICING["premium"]["price_per_license"] * config.num_recruiters
        calculations.append({
            "name": f"Премиум тариф × {config.num_recruiters} лиц.",
            "value": f"{price:,} ₽".replace(",", " ")
        })
        total = price
    elif config.show_standard:
        price = PRICING["standard"]["price_per_license"] * config.num_recruiters
        calculations.append({
            "name": f"Стандартный тариф × {config.num_recruiters} лиц.",
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
    
    # If both tariffs shown, show both calculations
    if config.show_standard and config.show_premium:
        calculations = []
        std_price = PRICING["standard"]["price_per_license"] * config.num_recruiters
        prem_price = PRICING["premium"]["price_per_license"] * config.num_recruiters
        
        calculations.append({
            "name": f"Стандартный: {config.num_recruiters} лиц. × 20 000 ₽",
            "value": f"{std_price:,} ₽".replace(",", " ")
        })
        
        if config.show_ai_option:
            ai_price = PRICING["ai_search"]["price_yearly"]
            calculations.append({
                "name": "+ ИИ-поиск (опционально)",
                "value": f"+{ai_price:,} ₽/год".replace(",", " ")
            })
        
        calculations.append({
            "name": f"Премиум: {config.num_recruiters} лиц. × 42 000 ₽",
            "value": f"{prem_price:,} ₽".replace(",", " ")
        })
        
        # Show range
        total = f"от {std_price:,} до {prem_price:,}".replace(",", " ")
    else:
        total = f"{total:,}".replace(",", " ")
    
    # Ensure we have default pain points and needs if empty
    pain_points = analysis.current_pain_points or [
        "Долгий процесс закрытия вакансий",
        "Разрозненные источники кандидатов",
        "Отсутствие единой базы"
    ]
    
    needs = analysis.needs or [
        "Автоматизация рутинных задач",
        "Централизованное управление наймом",
        "Прозрачная аналитика"
    ]
    
    discussed = analysis.discussed_features or [
        "Интеграции с job-сайтами",
        "Воронка подбора",
        "Аналитика"
    ]
    
    # Render HTML
    html_content = template.render(
        logo_path=str(ASSETS_DIR / "logo.png"),
        company_name=analysis.company_name,
        contact_name=analysis.contact_name,
        summary=analysis.summary,
        hiring_situation=analysis.hiring_situation,
        pain_points=pain_points,
        needs=needs,
        discussed_features=discussed,
        specific_request=analysis.specific_request,
        feature_icons=FEATURE_ICONS,
        highlighted_features=highlighted_features,
        highlighted_features_str=highlighted_features_str,
        show_standard=config.show_standard,
        show_premium=config.show_premium,
        show_ai_option=config.show_ai_option,
        show_ai=config.show_premium or config.show_ai_option,
        num_recruiters=config.num_recruiters,
        calculations=calculations,
        total_price=total,
    )
    
    # Generate PDF
    html = HTML(string=html_content, base_url=str(ASSETS_DIR))
    html.write_pdf(str(output_path))
    
    logger.info(f"Generated PDF: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    
    return output_path
