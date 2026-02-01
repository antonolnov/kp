"""
Bot configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Bot settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8289166080:AAEKdsZJpCH4X6YNhGod3_AUs4oOEFQvWK0")
CURSOR_API_KEY = os.getenv("CURSOR_API_KEY", "")

# Paths
BOT_DIR = Path(__file__).parent
TEMPLATES_DIR = BOT_DIR / "templates"
STORAGE_DIR = BOT_DIR / "storage"
ASSETS_DIR = BOT_DIR.parent / "kp" / "assets"

# Storage settings
HISTORY_RETENTION_DAYS = 3

# Pricing
PRICING = {
    "standard": {
        "name": "Стандартный",
        "price_per_license": 20000,
        "period": "год",
        "ai_included": False,
        "features": [
            "База кандидатов",
            "Интеграции с job-сайтами",
            "Воронка подбора",
            "Коммуникации в одном окне",
            "Календарь и напоминания",
            "Базовая аналитика",
            "Мобильное приложение",
        ]
    },
    "premium": {
        "name": "Премиум",
        "price_per_license": 42000,
        "period": "год",
        "ai_included": True,
        "features": [
            "Всё из Стандартного тарифа",
            "ИИ-поиск кандидатов",
            "Семантический поиск",
            "AI-скоринг резюме",
            "Генерация текстов",
            "Расширенная аналитика",
            "Приоритетная поддержка",
        ]
    },
    "ai_search": {
        "name": "ИИ-поиск кандидатов",
        "price_monthly": 5000,
        "price_yearly": 50000,
        "description": "Умный поиск по базе резюме с семантическим анализом"
    }
}
