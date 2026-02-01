#!/usr/bin/env python3
"""
WorkHere Commercial Proposal Bot
Generates personalized PDF proposals based on meeting transcripts
"""
import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Add bot directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import TELEGRAM_BOT_TOKEN, STORAGE_DIR
from handlers.proposal import router as proposal_router
from services.history_storage import start_cleanup_task

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point"""
    # Ensure storage directory exists
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register routers
    dp.include_router(proposal_router)
    
    # Start cleanup task
    cleanup_task = asyncio.create_task(start_cleanup_task())
    
    logger.info("Starting WorkHere КП Bot...")
    
    try:
        # Delete webhook and start polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        cleanup_task.cancel()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
