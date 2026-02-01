"""
PDF Generator for personalized commercial proposals
"""
import logging
import random
from pathlib import Path
from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from config import TEMPLATES_DIR, ASSETS_DIR, PRICING
from .ai_analyzer import MeetingAnalysis

logger = logging.getLogger(__name__)


# Фразы для маскота (без эмодзи — WeasyPrint не поддерживает)
MASCOT_PHRASES = [
    "Разберёмся с рутиной — будет время на важное!",
    "Все отклики в одном месте — красота!",
    "Автоматизация — это про нас!",
    "Меньше рутины, больше результата!",
    "Ваша команда скажет спасибо!",
    "Наконец-то порядок в подборе!",
    "Рекрутинг может быть простым!",
    "Будем рады видеть вас в WorkHere!",
    "Подбор без хаоса — это реально!",
    "Время на кандидатов, а не на рутину!",
]


@dataclass
class ProposalConfig:
    """Configuration for proposal generation"""
    show_standard: bool = True
    show_premium: bool = False
    show_ai_option: bool = False
    num_recruiters: int = 1


def get_mascot_paths() -> list[Path]:
    """Get all available mascot images"""
    mascots_dir = ASSETS_DIR / "mascots"
    if mascots_dir.exists():
        mascots = list(mascots_dir.glob("*.svg")) + list(mascots_dir.glob("*.png"))
        if mascots:
            return mascots
    
    # Fallback to single mascot
    single = ASSETS_DIR / "mascot.svg"
    if single.exists():
        return [single]
    
    return []


def get_random_mascots(count: int = 3) -> list[str]:
    """Get random mascot paths for the document"""
    mascots = get_mascot_paths()
    if not mascots:
        return [""] * count
    
    # If we have fewer mascots than needed, repeat them
    result = []
    for i in range(count):
        mascot = random.choice(mascots)
        result.append(str(mascot))
    
    return result


def get_random_phrases(count: int = 3) -> list[str]:
    """Get random phrases for mascots"""
    phrases = random.sample(MASCOT_PHRASES, min(count, len(MASCOT_PHRASES)))
    # Ensure we have enough phrases
    while len(phrases) < count:
        phrases.append(random.choice(MASCOT_PHRASES))
    return phrases


def calculate_mascot_sizes(
    discussed_features: list[str],
    hiring_situation: str,
    show_both_tariffs: bool,
    show_ai: bool
) -> dict:
    """
    Рассчитать размеры маскотов на основе количества контента.
    
    Правило: чем меньше контента, тем больше маскоты (заполняют пустоту).
    
    Returns:
        dict с ключами: size_1, size_2, size_3 (в пикселях)
    """
    # Базовая оценка "плотности" контента (0-100)
    content_score = 0
    
    # Количество пунктов обсуждения (основной фактор)
    features_count = len(discussed_features)
    if features_count <= 3:
        content_score += 10
    elif features_count <= 5:
        content_score += 30
    elif features_count <= 7:
        content_score += 50
    else:
        content_score += 70
    
    # Длина ситуации
    situation_len = len(hiring_situation) if hiring_situation else 0
    if situation_len > 150:
        content_score += 15
    elif situation_len > 80:
        content_score += 10
    
    # Два тарифа = больше контента в таблице
    if show_both_tariffs:
        content_score += 10
    
    # AI-модуль = дополнительный раздел
    if show_ai:
        content_score += 10
    
    # Определяем размеры на основе score
    # Чем МЕНЬШЕ score, тем БОЛЬШЕ маскоты
    
    if content_score <= 30:
        # Мало контента — большие маскоты
        return {
            'size_1': 160,  # После раздела 1
            'size_2': 180,  # После раздела 2
            'size_3': 220,  # Финальный (самый большой)
        }
    elif content_score <= 50:
        # Средний контент — средние маскоты
        return {
            'size_1': 130,
            'size_2': 150,
            'size_3': 180,
        }
    elif content_score <= 70:
        # Много контента — маленькие маскоты
        return {
            'size_1': 100,
            'size_2': 110,
            'size_3': 140,
        }
    else:
        # Очень много контента — минимальные маскоты
        return {
            'size_1': 80,
            'size_2': 90,
            'size_3': 120,
        }


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
            "Единая база кандидатов: все контакты, резюме и история в одном месте",
            "Интеграции с работными сайтами: HH.ru, Авито — автоматический сбор откликов",
            "Настраиваемые воронки и статусы под ваши процессы",
            "Аналитика и отчёты: конверсии, источники, Time-to-Hire",
            "Коммуникации с кандидатами через мессенджеры",
            "Telegram-бот для уведомлений и напоминаний"
        ]
        for d in defaults:
            if d not in discussed and len(discussed) < 8:
                discussed.append(d)
    
    # Get mascots and phrases
    mascot_paths = get_random_mascots(3)
    mascot_phrases = get_random_phrases(3)
    
    # Calculate mascot sizes based on content density
    mascot_sizes = calculate_mascot_sizes(
        discussed_features=discussed,
        hiring_situation=analysis.hiring_situation or "",
        show_both_tariffs=config.show_standard and config.show_premium,
        show_ai=config.show_ai_option or config.show_premium
    )
    
    logger.info(f"Content density -> mascot sizes: {mascot_sizes}")
    
    # Render HTML
    html_content = template.render(
        logo_path=str(ASSETS_DIR / "logo.png"),
        mascot_path_1=mascot_paths[0],
        mascot_path_2=mascot_paths[1],
        mascot_path_3=mascot_paths[2],
        mascot_phrase_1=mascot_phrases[0],
        mascot_phrase_2=mascot_phrases[1],
        mascot_phrase_3=mascot_phrases[2],
        mascot_size_1=mascot_sizes['size_1'],
        mascot_size_2=mascot_sizes['size_2'],
        mascot_size_3=mascot_sizes['size_3'],
        company_name=analysis.company_name or "",
        contact_name=analysis.contact_name or "",
        contact_role=analysis.contact_role or "",
        industry=analysis.industry or "",
        summary=analysis.summary or "",
        hiring_situation=analysis.hiring_situation or "",
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
