from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from typing import List


def get_goals_keyboard(goals: List[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=g)] for g in goals],
        resize_keyboard=True,
    )

def get_yes_no_keyboard() -> ReplyKeyboardMarkup:
    """Returns a simple Yes/No keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
        resize_keyboard=True,
    )

def get_life_areas_keyboard() -> ReplyKeyboardMarkup:
    """Returns the keyboard for selecting a life area."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Здоровье"),
                KeyboardButton(text="Карьера"),
                KeyboardButton(text="Деньги"),
            ],
            [
                KeyboardButton(text="Отношения"),
                KeyboardButton(text="Ум"),
                KeyboardButton(text="Дом/пространство"),
            ],
            [KeyboardButton(text="Другое")],
        ],
        resize_keyboard=True,
    )

def add_rem_keyboard() -> ReplyKeyboardMarkup:
    """Returns the keyboard for the summary screen."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Добавить"),
                KeyboardButton(text="✂️ Убрать"),
            ],
            [KeyboardButton(text="✅ Всё ок")],
        ],
        resize_keyboard=True,
    )

def get_back_keyboard() -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру с одной кнопкой 'Назад'."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад")]],
        resize_keyboard=True,
    )

def get_daily_rules_keyboard() -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру с кнопкой 'Это как?'."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Это как?")]],
        resize_keyboard=True,
    )

def example_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Давай пример!")], [KeyboardButton(text="Я уже хочу начинать!")]],
        resize_keyboard=True,
    )