"""
FSM States for bot conversation flow
"""
from aiogram.fsm.state import State, StatesGroup


class ProposalStates(StatesGroup):
    """States for proposal generation flow"""
    waiting_for_transcript = State()
    waiting_for_tariff = State()
    waiting_for_ai_option = State()
    processing = State()
