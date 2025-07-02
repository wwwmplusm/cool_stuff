"""Finite state machine for the onboarding flow."""

from aiogram.fsm.state import State, StatesGroup


class Onboarding(StatesGroup):
    """Conversation states for new users."""

    first_step = State()
    ask_goals_today = State()
    input_goals = State()
    select_life_area = State()
    suggest_example_goal = State()
    summary_goals = State()
    remove_goals = State()
    daily_rules = State()
    explain_logging = State()
    set_report_time = State()
