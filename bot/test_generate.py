#!/usr/bin/env python3
"""Тестовая генерация PDF для проверки вёрстки"""
import sys
sys.path.insert(0, '/workspace/bot')

from pathlib import Path
from services.pdf_generator import generate_proposal_pdf, ProposalConfig
from services.ai_analyzer import MeetingAnalysis

# Тестовые данные
analysis = MeetingAnalysis(
    company_name="ТестКомпания",
    contact_name="Юлия",
    contact_role="HR-директор",
    num_recruiters=4,
    industry="Общепит / HoReCa",
    current_tools="Битрикс, Excel",
    hiring_situation="Компания из сферы Общепит / HoReCa ищет способы оптимизировать процесс подбора. Команда из 4 рекрутеров работает с несколькими площадками.",
    discussed_features=[
        "Интеграции с работными сайтами: подключение HH.ru, Авито — автоматический сбор откликов",
        "Настраиваемые воронки и статусы: возможность создавать несколько воронок под разные типы подбора",
        "Аналитика и отчёты: конверсии воронки, Time-to-Hire, эффективность источников",
        "IP-телефония: звонки из карточки кандидата, запись разговоров",
        "Коммуникации через мессенджеры: Telegram, WhatsApp — переписка в карточке",
        "Календарь собеседований: интеграция с Яндекс Телемост",
    ],
    current_pain_points=[
        "Работа ведётся в нескольких инструментах",
        "Ручной перенос данных между площадками",
    ],
    needs=["Автоматизация", "Единая система"],
    summary="Решение для автоматизации подбора"
)

config = ProposalConfig(
    show_standard=True,
    show_premium=True,
    show_ai_option=False,
    num_recruiters=4
)

output_path = Path("/workspace/bot/test_output.pdf")
generate_proposal_pdf(analysis, config, output_path)
print(f"PDF создан: {output_path}")
print(f"Размер: {output_path.stat().st_size / 1024:.1f} KB")
