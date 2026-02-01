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


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    await state.clear()
    
    await message.answer(
        "👋 Привет! Я помогу создать персонализированное коммерческое предложение WorkHere.\n\n"
        "📝 **Как это работает:**\n"
        "1. Отправь мне транскрибацию встречи (текст, .txt или .docx файл)\n"
        "2. Выбери тариф для КП\n"
        "3. Получи готовый PDF\n\n"
        "📋 **Команды:**\n"
        "/new — создать новое КП\n"
        "/history — история КП (хранится 3 дня)\n"
        "/help — справка\n\n"
        "Отправь транскрибацию, чтобы начать!",
        parse_mode="Markdown"
    )
    await state.set_state(ProposalStates.waiting_for_transcript)


@router.message(Command("new"))
async def cmd_new(message: Message, state: FSMContext):
    """Start new proposal"""
    await state.clear()
    await message.answer(
        "📝 Отправь транскрибацию встречи.\n\n"
        "Можно отправить:\n"
        "• Текст сообщением\n"
        "• Файл .txt\n"
        "• Файл .docx"
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


# Handle transcript - text message
@router.message(StateFilter(ProposalStates.waiting_for_transcript), F.text)
async def handle_transcript_text(message: Message, state: FSMContext):
    """Handle transcript as text message"""
    if message.text.startswith("/"):
        return
    
    transcript = message.text
    
    if len(transcript) < 50:
        await message.answer("⚠️ Текст слишком короткий. Отправь полную транскрибацию встречи.")
        return
    
    await state.update_data(transcript=transcript)
    
    await message.answer(
        "📊 Выбери тариф для коммерческого предложения:",
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
        await message.answer("⚠️ Поддерживаются только файлы .txt и .docx")
        return
    
    # Check file size (max 10MB)
    if doc.file_size > 10 * 1024 * 1024:
        await message.answer("⚠️ Файл слишком большой. Максимум 10 МБ.")
        return
    
    status_msg = await message.answer("⏳ Читаю файл...")
    
    try:
        # Download file
        file = await message.bot.get_file(doc.file_id)
        file_content = await message.bot.download_file(file.file_path)
        content_bytes = file_content.read()
        
        # Parse document
        transcript = await parse_document(content_bytes, filename)
        
        if len(transcript) < 50:
            await status_msg.edit_text("⚠️ Файл пустой или содержит слишком мало текста.")
            return
        
        await state.update_data(transcript=transcript)
        
        await status_msg.edit_text(
            f"✅ Файл прочитан ({len(transcript)} символов)\n\n"
            "📊 Выбери тариф для коммерческого предложения:",
            reply_markup=get_tariff_keyboard()
        )
        await state.set_state(ProposalStates.waiting_for_tariff)
        
    except Exception as e:
        logger.error(f"Failed to parse file: {e}")
        await status_msg.edit_text(f"❌ Ошибка чтения файла: {e}")


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
        # Premium or both - proceed to generation
        await state.update_data(ai_option=False)
        await generate_proposal(callback.message, state)


# Handle AI option
@router.callback_query(StateFilter(ProposalStates.waiting_for_ai_option), F.data.startswith("ai_"))
async def handle_ai_option(callback: CallbackQuery, state: FSMContext):
    """Handle AI option selection"""
    ai_option = callback.data == "ai_yes"
    await callback.answer()
    
    await state.update_data(ai_option=ai_option)
    await generate_proposal(callback.message, state)


async def generate_proposal(message: Message, state: FSMContext):
    """Generate the proposal PDF - GPT-4o acts as designer"""
    from services.html_generator import generate_html_proposal
    from services.page_reviewer import full_review, format_review_report
    from config import OPENAI_API_KEY
    
    data = await state.get_data()
    transcript = data.get("transcript", "")
    tariff = data.get("tariff", "standard")
    ai_option = data.get("ai_option", False)
    
    status_msg = await message.edit_text("🎨 GPT-4o создаёт КП как дизайнер...")
    
    try:
        # 1. GPT-4o generates full HTML (acts as designer)
        proposal_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        pdf_filename = f"КП_{timestamp}.pdf"
        pdf_path = STORAGE_DIR / pdf_filename
        
        # Определяем количество рекрутеров из транскрибации (простой поиск)
        num_recruiters = 3  # default
        for word in ["4 рекрутер", "четыре рекрутер", "5 рекрутер", "пять рекрутер"]:
            if word in transcript.lower():
                num_recruiters = int(word[0]) if word[0].isdigit() else 5
                break
        
        await generate_html_proposal(
            transcript=transcript,
            tariff=tariff,
            num_recruiters=num_recruiters,
            output_path=pdf_path
        )
        
        # 2. Review PDF with GPT-4o vision
        review_info = ""
        if OPENAI_API_KEY:
            await status_msg.edit_text("🔍 Проверяю качество...")
            
            review = await full_review(pdf_path, OPENAI_API_KEY)
            report = format_review_report(review)
            logger.info(report)
            
            if not review.is_ok:
                all_issues = []
                for pr in review.page_reviews:
                    if pr.issues:
                        all_issues.extend([f"Стр.{pr.page_num}: {i}" for i in pr.issues])
                all_issues.extend(review.final_issues)
                
                if all_issues:
                    review_info = "\n\n⚠️ Замечания:\n" + "\n".join(f"• {i}" for i in all_issues[:3])
        
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
            company_name="",  # GPT extracts it inside HTML
            tariff=tariff_label,
            num_recruiters=num_recruiters,
            created_at=datetime.now().isoformat(),
            pdf_path=str(pdf_path),
            summary=""
        )
        await history_storage.add_record(record)
        
        # Send PDF
        await status_msg.delete()
        
        caption = f"✅ **КП готово!**\n\n"
        caption += f"👥 Рекрутеров: {num_recruiters}\n"
        caption += f"💼 Тариф: {tariff_label}"
        caption += review_info
        
        await message.answer_document(
            FSInputFile(pdf_path, filename=pdf_filename),
            caption=caption,
            parse_mode="Markdown"
        )
        
        await message.answer(
            "💡 Используй /new чтобы создать ещё одно КП\n"
            "📋 /history — посмотреть историю"
        )
        
    except Exception as e:
        logger.exception(f"Failed to generate proposal: {e}")
        await status_msg.edit_text(f"❌ Ошибка генерации: {e}\n\nПопробуй ещё раз: /new")
    
    finally:
        await state.clear()


# Handle unexpected messages
@router.message(StateFilter(ProposalStates.waiting_for_tariff))
async def handle_waiting_tariff(message: Message):
    """Handle message when waiting for tariff"""
    await message.answer(
        "👆 Выбери тариф, нажав на одну из кнопок выше.",
        reply_markup=get_tariff_keyboard()
    )


@router.message(StateFilter(ProposalStates.waiting_for_ai_option))
async def handle_waiting_ai(message: Message):
    """Handle message when waiting for AI option"""
    await message.answer(
        "👆 Выбери, нужен ли ИИ-поиск:",
        reply_markup=get_ai_option_keyboard()
    )
