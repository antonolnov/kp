"""
PDF Generator for personalized commercial proposals
Принцип: думай как Артемий Лебедев — каждый элемент должен быть на своём месте,
пустота должна быть заполнена, баланс визуала и контента.
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


# Фразы для маскота (без эмодзи)
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
    
    single = ASSETS_DIR / "mascot.svg"
    if single.exists():
        return [single]
    
    return []


def get_random_mascots(count: int = 4) -> list[str]:
    """Get random mascot paths for the document"""
    mascots = get_mascot_paths()
    if not mascots:
        return [""] * count
    
    result = []
    for i in range(count):
        mascot = random.choice(mascots)
        result.append(str(mascot))
    
    return result


def get_random_phrases(count: int = 4) -> list[str]:
    """Get random phrases for mascots"""
    phrases = random.sample(MASCOT_PHRASES, min(count, len(MASCOT_PHRASES)))
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
    ПРАВИЛО ДИЗАЙНЕРА:
    Маскоты должны ЗАПОЛНЯТЬ пустое пространство.
    Чем меньше контента — тем БОЛЬШЕ маскоты.
    
    4 маскота в документе:
    1. После раздела "Что обсуждали"
    2. После раздела "Решение WorkHere"  
    3. После раздела "Внедрение"
    4. В конце перед футером
    """
    # Оценка контента
    features_count = len(discussed_features) if discussed_features else 0
    situation_len = len(hiring_situation) if hiring_situation else 0
    
    # Базовый размер — БОЛЬШОЙ
    # Уменьшаем только если много контента
    
    base_size = 180  # Большой по умолчанию
    
    # Корректировка на контент
    if features_count >= 7:
        base_size -= 40
    elif features_count >= 5:
        base_size -= 20
    
    if situation_len > 200:
        base_size -= 20
    elif situation_len > 100:
        base_size -= 10
    
    if show_both_tariffs:
        base_size -= 10
    
    if show_ai:
        base_size -= 10
    
    # Минимум 120px
    base_size = max(base_size, 120)
    
    # Разные размеры для разных позиций
    # Финальный маскот всегда самый большой
    return {
        'size_1': base_size,
        'size_2': base_size + 10,
        'size_3': base_size + 20,
        'size_4': base_size + 40,  # Финальный — самый большой
    }


def generate_proposal_pdf(
    analysis: MeetingAnalysis,
    config: ProposalConfig,
    output_path: Path
) -> Path:
    """
    Генерация PDF как ДИЗАЙНЕР:
    - Баланс контента и визуала
    - Маскоты заполняют пустоты
    - Чистая типографика
    - Никакого визуального мусора
    """
    
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("proposal.html")
    
    num_recruiters = config.num_recruiters if config.num_recruiters > 1 else analysis.num_recruiters
    if num_recruiters < 1:
        num_recruiters = 1
    
    # Расчёт цен
    calculations = []
    total = 0
    
    if config.show_standard and config.show_premium:
        std_price = PRICING["standard"]["price_per_license"] * num_recruiters
        prem_price = PRICING["premium"]["price_per_license"] * num_recruiters
        
        calculations.append({
            "name": f"Стандартный тариф ({num_recruiters} × 20 000 ₽)",
            "value": f"{std_price:,} ₽/год".replace(",", " ")
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
        
    else:
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
    
    # Для расчёта размеров маскотов используем копию списка (не мутируем оригинал!)
    discussed = list(analysis.diagnosis_pains or [])
    
    # 4 маскота с ПРАВИЛЬНЫМИ размерами
    mascot_paths = get_random_mascots(4)
    mascot_phrases = get_random_phrases(4)
    
    mascot_sizes = calculate_mascot_sizes(
        discussed_features=discussed,
        hiring_situation=analysis.hiring_situation or "",
        show_both_tariffs=config.show_standard and config.show_premium,
        show_ai=config.show_ai_option or config.show_premium
    )
    
    logger.info(f"Mascot sizes calculated: {mascot_sizes}")
    
    # Используем контент от AI напрямую — никаких дефолтов!
    # AI должен генерировать всё сам
    diagnosis_pains = analysis.diagnosis_pains or []
    solution_base = analysis.solution_base or []
    solution_integrations = analysis.solution_integrations or []
    solution_automation = analysis.solution_automation or []
    solution_ai = analysis.solution_ai or []
    why_recruiters = analysis.why_recruiters or []
    why_managers = analysis.why_managers or []
    diagnosis_situation = analysis.diagnosis_situation or ""
    key_message = analysis.key_message or ""
    
    logger.info(f"Content from AI: pains={len(diagnosis_pains)}, base={len(solution_base)}, situation={len(diagnosis_situation)} chars")
    
    # Рендер
    html_content = template.render(
        logo_path=str(ASSETS_DIR / "logo.png"),
        mascot_path_1=mascot_paths[0],
        mascot_path_2=mascot_paths[1],
        mascot_path_3=mascot_paths[2],
        mascot_path_4=mascot_paths[3],
        mascot_phrase_1=mascot_phrases[0],
        mascot_phrase_2=mascot_phrases[1],
        mascot_phrase_3=mascot_phrases[2],
        mascot_phrase_4=mascot_phrases[3],
        mascot_size_1=mascot_sizes['size_1'],
        mascot_size_2=mascot_sizes['size_2'],
        mascot_size_3=mascot_sizes['size_3'],
        mascot_size_4=mascot_sizes['size_4'],
        company_name=analysis.company_name or "",
        contact_name=analysis.contact_name or "",
        contact_role=analysis.contact_role or "",
        # Раздел 1: Диагноз
        diagnosis_situation=diagnosis_situation,
        diagnosis_pains=diagnosis_pains,
        # Раздел 2: Решение (персонализированное)
        solution_base=solution_base,
        solution_integrations=solution_integrations,
        solution_automation=solution_automation,
        solution_ai=solution_ai,
        # Раздел 5: Почему WorkHere (персонализированное)
        why_recruiters=why_recruiters,
        why_managers=why_managers,
        # Ключевой посыл
        key_message=key_message,
        # Цены
        show_standard=config.show_standard,
        show_premium=config.show_premium,
        show_ai_option=config.show_ai_option,
        num_recruiters=num_recruiters,
        calculations=calculations,
        total_price=total,
    )
    
    html = HTML(string=html_content, base_url=str(ASSETS_DIR))
    html.write_pdf(str(output_path))
    
    logger.info(f"Generated PDF: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    
    return output_path
