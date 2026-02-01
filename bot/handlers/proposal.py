"""
Proposal generation handlers
"""
import uuid
import logging
from datetime import datetime
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .states import ProposalStates
from services.ai_analyzer import analyze_transcript, MeetingAnalysis
from services.pdf_generator import generate_proposal_pdf, ProposalConfig
from services.document_parser import parse_document
from services.history_storage import history_storage, ProposalRecord
from config import STORAGE_DIR

logger = logging.getLogger(__name__)

router = Router()


# Keyboards
def get_tariff_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for tariff selection"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💼 Стандартный (20 000 ₽/год)", callback_data="tariff_standard")],
        [InlineKeyboardButton(text="⭐ Премиум (42 000 ₽/год)", callback_data="tariff_premium")],
        [InlineKeyboardButton(text="💼+⭐ Оба варианта", callback_data="tariff_both")],
    ])


def get_ai_option_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for AI option selection"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, добавить ИИ-поиск", callback_data="ai_yes")],
        [InlineKeyboardButton(text="❌ Нет, без ИИ", callback_data="ai_no")],
    ])


def get_bonus_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for bonus option selection"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 2 года + 1 лицензия в подарок", callback_data="bonus_free_license")],
        [InlineKeyboardButton(text="🔄 Бесплатный переход с конкурента", callback_data="bonus_competitor")],
        [InlineKeyboardButton(text="📅 2 года + 3 месяца бесплатно", callback_data="bonus_3months")],
        [InlineKeyboardButton(text="➡️ Без бонуса", callback_data="bonus_none")],
    ])


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    await state.clear()
    
    user_name = message.from_user.first_name or "друг"
    
    await message.answer(
        f"👋 Привет, {user_name}!\n\n"
        "Я помогу создать персонализированное КП для клиента на основе записи встречи.\n\n"
        "📎 **Просто отправь мне файл с транскрибацией** (.txt или .docx)\n\n"
        "Я проанализирую диалог и создам красивый PDF с предложением под конкретного клиента ✨",
        parse_mode="Markdown"
    )
    await state.set_state(ProposalStates.waiting_for_transcript)


@router.message(Command("new"))
async def cmd_new(message: Message, state: FSMContext):
    """Start new proposal"""
    await state.clear()
    await message.answer(
        "📎 Отправь файл с транскрибацией встречи\n\n"
        "Поддерживаю .txt и .docx"
    )
    await state.set_state(ProposalStates.waiting_for_transcript)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Show help"""
    await message.answer(
        "📚 **Справка по боту WorkHere КП**\n\n"
        "Бот анализирует транскрибацию встречи с клиентом и создает "
        "персонализированное коммерческое предложение в PDF формате.\n\n"
        "**Что извлекается из встречи:**\n"
        "• Название компании клиента\n"
        "• Количество рекрутеров\n"
        "• Текущие боли и потребности\n"
        "• Обсуждаемые функции\n\n"
        "**Тарифы:**\n"
        "• Стандартный — 20 000 ₽/лицензия/год\n"
        "• Премиум — 42 000 ₽/лицензия/год (с AI)\n"
        "• ИИ-поиск — 5 000 ₽/мес или 50 000 ₽/год\n\n"
        "**Команды:**\n"
        "/new — начать создание КП\n"
        "/history — показать историю\n"
        "/cancel — отменить текущую операцию",
        parse_mode="Markdown"
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Cancel current operation"""
    await state.clear()
    await message.answer("❌ Операция отменена. Используй /new чтобы начать заново.")


@router.message(Command("history"))
async def cmd_history(message: Message):
    """Show proposal history"""
    records = await history_storage.get_user_history(message.from_user.id)
    
    if not records:
        await message.answer("📭 История пуста. Создай первое КП с помощью /new")
        return
    
    text = "📋 **История КП** (последние 10, хранятся 3 дня):\n\n"
    
    keyboard_buttons = []
    for i, record in enumerate(records, 1):
        created = datetime.fromisoformat(record.created_at).strftime("%d.%m.%Y %H:%M")
        company = record.company_name or "Без названия"
        text += f"{i}. **{company}** — {record.tariff}\n"
        text += f"   📅 {created} | 👥 {record.num_recruiters} лиц.\n\n"
        
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"📄 {i}. {company[:20]}",
                callback_data=f"download_{record.id}"
            )
        ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)


@router.callback_query(F.data.startswith("download_"))
async def handle_download(callback: CallbackQuery):
    """Handle PDF download from history"""
    record_id = callback.data.replace("download_", "")
    record = await history_storage.get_record_by_id(record_id)
    
    if not record:
        await callback.answer("❌ Файл не найден", show_alert=True)
        return
    
    pdf_path = Path(record.pdf_path)
    if not pdf_path.exists():
        await callback.answer("❌ Файл был удален", show_alert=True)
        return
    
    await callback.answer()
    
    company = record.company_name or "WorkHere"
    filename = f"КП_{company}_{record.tariff}.pdf"
    
    await callback.message.answer_document(
        FSInputFile(pdf_path, filename=filename),
        caption=f"📄 КП для {company}\n{record.tariff} | {record.num_recruiters} лиц."
    )


# Валидация что это встреча
def validate_transcript(text: str) -> tuple[bool, str]:
    """Проверяет что текст — это транскрибация встречи про рекрутинг/HR"""
    text_lower = text.lower()
    
    # Ключевые слова встречи
    meeting_keywords = ["здравствуйте", "добрый день", "привет", "давайте", "расскажите", 
                       "встреча", "созвон", "обсудить", "вопрос", "спасибо", "до свидания"]
    
    # Ключевые слова HR/рекрутинга
    hr_keywords = ["рекрутер", "подбор", "кандидат", "вакансия", "резюме", "hr", "найм", 
                   "hh", "headhunter", "авито", "отклик", "собеседование", "персонал",
                   "ats", "crm", "система", "workhere", "интеграция", "воронка"]
    
    has_meeting = any(kw in text_lower for kw in meeting_keywords)
    has_hr = any(kw in text_lower for kw in hr_keywords)
    
    if len(text) < 200:
        return False, "Текст слишком короткий. Нужна полная транскрибация встречи 😊"
    
    if not has_meeting:
        return False, "Похоже, это не транскрибация встречи. Отправь, пожалуйста, запись диалога с клиентом 🎙"
    
    if not has_hr:
        return False, "Не нашла обсуждения рекрутинга или HR-системы. Отправь транскрибацию встречи про WorkHere 💼"
    
    return True, ""


# Handle transcript - text message
@router.message(StateFilter(ProposalStates.waiting_for_transcript), F.text)
async def handle_transcript_text(message: Message, state: FSMContext):
    """Handle transcript as text message"""
    if message.text.startswith("/"):
        return
    
    transcript = message.text
    
    # Валидация
    is_valid, error_msg = validate_transcript(transcript)
    if not is_valid:
        await message.answer(error_msg)
        return
    
    await state.update_data(transcript=transcript)
    
    await message.answer(
        "✨ Отлично! Теперь выбери тариф:",
        reply_markup=get_tariff_keyboard()
    )
    await state.set_state(ProposalStates.waiting_for_tariff)


# Handle transcript - file
@router.message(StateFilter(ProposalStates.waiting_for_transcript), F.document)
async def handle_transcript_file(message: Message, state: FSMContext):
    """Handle transcript as file"""
    doc = message.document
    
    # Check file extension
    filename = doc.file_name or "file.txt"
    suffix = Path(filename).suffix.lower()
    
    if suffix not in [".txt", ".docx"]:
        await message.answer("📎 Поддерживаю только .txt и .docx файлы. Попробуй в другом формате!")
        return
    
    # Check file size (max 10MB)
    if doc.file_size > 10 * 1024 * 1024:
        await message.answer("📦 Файл великоват! Максимум 10 МБ, пожалуйста.")
        return
    
    status_msg = await message.answer("📖 Читаю файл...")
    
    try:
        # Download file
        file = await message.bot.get_file(doc.file_id)
        file_content = await message.bot.download_file(file.file_path)
        content_bytes = file_content.read()
        
        # Parse document
        transcript = await parse_document(content_bytes, filename)
        
        # Валидация содержимого
        is_valid, error_msg = validate_transcript(transcript)
        if not is_valid:
            await status_msg.edit_text(error_msg)
            return
        
        await state.update_data(transcript=transcript)
        
        await status_msg.edit_text(
            f"✅ Готово! Прочитала {len(transcript)} символов\n\n"
            "✨ Теперь выбери тариф:",
            reply_markup=get_tariff_keyboard()
        )
        await state.set_state(ProposalStates.waiting_for_tariff)
        
    except Exception as e:
        logger.error(f"Failed to parse file: {e}")
        await status_msg.edit_text(f"😔 Не получилось прочитать файл. Попробуй другой?")


# Handle tariff selection
@router.callback_query(StateFilter(ProposalStates.waiting_for_tariff), F.data.startswith("tariff_"))
async def handle_tariff_selection(callback: CallbackQuery, state: FSMContext):
    """Handle tariff selection"""
    tariff = callback.data.replace("tariff_", "")
    await callback.answer()
    
    await state.update_data(tariff=tariff)
    
    # If standard tariff, ask about AI option
    if tariff == "standard":
        await callback.message.edit_text(
            "🤖 Добавить **ИИ-поиск кандидатов** к стандартному тарифу?\n\n"
            "• 5 000 ₽/месяц\n"
            "• 50 000 ₽/год (экономия 17%)",
            parse_mode="Markdown",
            reply_markup=get_ai_option_keyboard()
        )
        await state.set_state(ProposalStates.waiting_for_ai_option)
    else:
        # Premium or both - ask about bonus
        await state.update_data(ai_option=False)
        await ask_bonus(callback.message, state)


# Handle AI option
@router.callback_query(StateFilter(ProposalStates.waiting_for_ai_option), F.data.startswith("ai_"))
async def handle_ai_option(callback: CallbackQuery, state: FSMContext):
    """Handle AI option selection"""
    ai_option = callback.data == "ai_yes"
    await callback.answer()
    
    await state.update_data(ai_option=ai_option)
    await ask_bonus(callback.message, state)


async def ask_bonus(message: Message, state: FSMContext):
    """Ask about bonus option for 2-year payment"""
    await message.edit_text(
        "🎁 **Добавить специальное предложение при оплате на 2 года?**\n\n"
        "Выбери бонус для клиента:",
        parse_mode="Markdown",
        reply_markup=get_bonus_keyboard()
    )
    await state.set_state(ProposalStates.waiting_for_bonus)


# Handle bonus option
@router.callback_query(StateFilter(ProposalStates.waiting_for_bonus), F.data.startswith("bonus_"))
async def handle_bonus_option(callback: CallbackQuery, state: FSMContext):
    """Handle bonus option selection"""
    bonus = callback.data.replace("bonus_", "")
    await callback.answer()
    
    # Map bonus codes to readable text
    bonus_texts = {
        "free_license": "При оплате на 2 года — 1 лицензия в подарок",
        "competitor": "Бесплатный период использования = остаток срока у текущего провайдера",
        "3months": "При оплате на 2 года — 3 месяца использования бесплатно",
        "none": None
    }
    
    await state.update_data(bonus=bonus_texts.get(bonus))
    await generate_proposal(callback.message, state)


async def generate_proposal(message: Message, state: FSMContext):
    """Generate the proposal PDF"""
    import asyncio
    from services.html_generator import generate_html_proposal
    from services.page_reviewer import full_review, format_review_report
    from config import OPENAI_API_KEY
    
    data = await state.get_data()
    transcript = data.get("transcript", "")
    tariff = data.get("tariff", "standard")
    ai_option = data.get("ai_option", False)
    bonus = data.get("bonus")  # Бонус при оплате на 2 года
    
    # Статусные сообщения с анимацией
    status_messages = [
        "✨ Анализирую встречу...\n\n⏳ Это займёт 30-60 секунд.\nМожешь пока отдохнуть ☕ или отправить другой файл — обработаю параллельно!",
        "🎨 Создаю дизайн КП...",
        "📝 Пишу персонализированный текст...",
        "🔧 Собираю документ...",
    ]
    
    status_msg = await message.edit_text(status_messages[0])
    
    try:
        proposal_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        pdf_filename = f"КП_{timestamp}.pdf"
        pdf_path = STORAGE_DIR / pdf_filename
        
        # Определяем количество рекрутеров
        num_recruiters = 3
        for word in ["4 рекрутер", "четыре рекрутер", "5 рекрутер", "пять рекрутер"]:
            if word in transcript.lower():
                num_recruiters = int(word[0]) if word[0].isdigit() else 5
                break
        
        # Обновляем статус пока генерируется
        async def update_status():
            for i, msg in enumerate(status_messages[1:], 1):
                await asyncio.sleep(8)
                try:
                    await status_msg.edit_text(msg)
                except:
                    pass
        
        # Запускаем обновление статуса параллельно
        status_task = asyncio.create_task(update_status())
        
        try:
            await generate_html_proposal(
                transcript=transcript,
                tariff=tariff,
                num_recruiters=num_recruiters,
                output_path=pdf_path,
                bonus=bonus
            )
        finally:
            status_task.cancel()
        
        # Финальная проверка
        await status_msg.edit_text("✅ Почти готово! Проверяю результат...")
        
        review_info = ""
        if OPENAI_API_KEY:
            try:
                review = await full_review(pdf_path, OPENAI_API_KEY)
                report = format_review_report(review)
                logger.info(report)
            except Exception as e:
                logger.warning(f"Review failed: {e}")
        
        # Determine tariff label
        if tariff == "both":
            tariff_label = "Стандартный + Премиум"
        elif tariff == "premium":
            tariff_label = "Премиум"
        else:
            tariff_label = "Стандартный" + (" + ИИ" if ai_option else "")
        
        # Save to history
        record = ProposalRecord(
            id=proposal_id,
            user_id=message.chat.id,
            username=None,
            company_name="",
            tariff=tariff_label,
            num_recruiters=num_recruiters,
            created_at=datetime.now().isoformat(),
            pdf_path=str(pdf_path),
            summary=""
        )
        await history_storage.add_record(record)
        
        # Send PDF
        await status_msg.delete()
        
        caption = f"🎉 **Готово!**\n\n"
        caption += f"👥 Рекрутеров: {num_recruiters}\n"
        caption += f"💼 Тариф: {tariff_label}"
        
        await message.answer_document(
            FSInputFile(pdf_path, filename=pdf_filename),
            caption=caption,
            parse_mode="Markdown"
        )
        
        await message.answer(
            "Хочешь создать ещё одно КП? Жми /new 🚀\n"
            "Посмотреть историю: /history"
        )
        
    except Exception as e:
        logger.exception(f"Failed to generate proposal: {e}")
        await status_msg.edit_text(
            "😔 Что-то пошло не так...\n\n"
            "Попробуй ещё раз: /new\n"
            "Если проблема повторится — напиши в поддержку."
        )
    
    finally:
        await state.clear()


# Handle unexpected messages
@router.message(StateFilter(ProposalStates.waiting_for_tariff))
async def handle_waiting_tariff(message: Message):
    """Handle message when waiting for tariff"""
    await message.answer(
        "☝️ Нажми на одну из кнопок выше, чтобы выбрать тариф",
        reply_markup=get_tariff_keyboard()
    )


@router.message(StateFilter(ProposalStates.waiting_for_ai_option))
async def handle_waiting_ai(message: Message):
    """Handle message when waiting for AI option"""
    await message.answer(
        "☝️ Выбери вариант кнопкой выше",
        reply_markup=get_ai_option_keyboard()
    )


@router.message(StateFilter(ProposalStates.waiting_for_bonus))
async def handle_waiting_bonus(message: Message):
    """Handle message when waiting for bonus option"""
    await message.answer(
        "☝️ Выбери бонус кнопкой выше",
        reply_markup=get_bonus_keyboard()
    )


# Handle any other message outside of expected flow
@router.message(StateFilter(ProposalStates.waiting_for_transcript))
async def handle_unexpected_in_transcript(message: Message):
    """Handle non-file message when waiting for transcript"""
    await message.answer(
        "📎 Жду файл с транскрибацией встречи (.txt или .docx)\n\n"
        "Если хочешь начать заново — /new"
    )


@router.message()
async def handle_any_message(message: Message, state: FSMContext):
    """Handle any message outside of flow"""
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer(
            "👋 Привет! Я создаю КП на основе транскрибаций встреч.\n\n"
            "Отправь /new чтобы начать"
        )
