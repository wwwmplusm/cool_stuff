"""Entry point for the Telegram bot.

Example:
    python main.py
"""

from __future__ import annotations

import logging


from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from config import load_config
from db import Database
from states import Onboarding
from typing import List

from keyboards import (
    get_yes_no_keyboard,
    get_life_areas_keyboard,
    add_rem_keyboard,
    get_goals_keyboard,
    get_back_keyboard,
    get_daily_rules_keyboard,
    example_keyboard
)

logging.basicConfig(level=logging.INFO)

cfg = load_config()
DB = Database(cfg.db_path)

bot = Bot(cfg.bot_token)
dp = Dispatcher()




@dp.message(CommandStart())
async def cmd_start(message: Message, state: Onboarding) -> None:
    await message.answer(
        "Большинство трекеров отнимают твоё время. Я – чтобы вернуть "
        "его и помочь сделать дела. \u23F3"
    )
    await message.answer(
        "У тебя уже есть цели/планы на сегодня?",
        reply_markup=get_yes_no_keyboard(),
    )
    await state.set_state(Onboarding.ask_goals_today)


@dp.message(Onboarding.ask_goals_today, Text("Да"))
async def process_has_goals(message: Message, state: Onboarding) -> None:
    await message.answer(
        "Отлично! Напиши списком или пришли голосовое – я всё сохраню."
    )
    await state.set_state(Onboarding.input_goals)


@dp.message(Onboarding.ask_goals_today, Text("Нет"))
async def process_no_goals(message: Message, state: Onboarding) -> None:
    await message.answer(
        "Понимаю. В какой сфере хочешь улучшиться сегодня?",
        reply_markup=get_life_areas_keyboard(),
    )
    await state.set_state(Onboarding.select_life_area)


@dp.message(Onboarding.input_goals)
async def input_goals(message: Message, state: Onboarding) -> None:
    goals_text = message.text or ""
    goals = [g.strip() for g in goals_text.split("\n") if g.strip()]
    data = await state.get_data()
    stored_goals: List[str] = data.get("goals", [])
    stored_goals.extend(goals)
    await state.update_data(goals=stored_goals)
    await summary_goals(message, state)


@dp.message(Onboarding.select_life_area)
async def select_area(message: Message, state: Onboarding) -> None:
    area = message.text
    await state.update_data(area=area)
    await message.answer(
        f"Пример действия для «{area}»: …  Напиши свою конкретику "
        "или нажми «Назад».",
        reply_markup=get_back_keyboard(),
    )
    await state.set_state(Onboarding.suggest_example_goal)


@dp.message(Onboarding.suggest_example_goal, Text("Назад"))
async def example_back(message: Message, state: Onboarding) -> None:
    await process_no_goals(message, state)


@dp.message(Onboarding.suggest_example_goal)
async def example_input(message: Message, state: Onboarding) -> None:
    await state.update_data(goals=[message.text])
    await summary_goals(message, state)


async def summary_goals(message: Message, state: Onboarding) -> None:
    data = await state.get_data()
    goals = data.get("goals", [])
    goals_list = "\n".join(f"- {hbold(g)}" for g in goals)
    await message.answer(
        f"Твой план на сегодня:\n{goals_list}\nВсё верно?",
        reply_markup=add_rem_keyboard()
    )
    await state.set_state(Onboarding.summary_goals)


@dp.message(Onboarding.summary_goals, Text("➕ Добавить"))
async def summary_add(message: Message, state: Onboarding) -> None:
    await message.answer("Напиши дополнительную цель")
    await state.set_state(Onboarding.input_goals)


@dp.message(Onboarding.summary_goals, Text("✂️ Убрать"))
async def summary_remove(message: Message, state: Onboarding) -> None:
    data = await state.get_data()
    goals = data.get("goals", [])
    await message.answer(
        "Отметь, что убрать:",
        reply_markup=get_goals_keyboard(goals),
    )
    await state.set_state(Onboarding.remove_goals)


@dp.message(Onboarding.summary_goals, Text("✅ Всё ок"))
async def summary_ok(message: Message, state: Onboarding) -> None:
    await message.answer(
        "Отличный план! Помни: цель без действия — мечта. В течение дня "
        "присылай мне голосом/текстом, как всё идёт. ✔️",
        reply_markup=get_daily_rules_keyboard(),
    )
    await state.set_state(Onboarding.daily_rules)


@dp.message(Onboarding.remove_goals)
async def remove_goals_state(message: Message, state: Onboarding) -> None:
    data = await state.get_data()
    goals = data.get("goals", [])
    if message.text in goals:
        goals.remove(message.text)
    await state.update_data(goals=goals)
    await summary_goals(message, state)


@dp.message(Onboarding.daily_rules, Text("Это как?"))
async def ask_example(message: Message, state: Onboarding) -> None:
    await message.answer(
        "Смотри: днём ты шлёшь заметки. Вечером нажимаешь «Подвести итог» "
        "— я дам полный отчёт. Хочешь пример?",
        reply_markup=example_keyboard(),
    )
    await state.set_state(Onboarding.explain_logging)


@dp.message(Onboarding.daily_rules)
async def skip_example(message: Message, state: Onboarding) -> None:
    await set_report_time(message, state)


@dp.message(Onboarding.explain_logging, Text("Давай!"))
async def send_example(message: Message, state: Onboarding) -> None:
    await message.answer("Пример отчёта: ...")
    await set_report_time(message, state)


@dp.message(Onboarding.explain_logging, Text("Уже хочу начинать!"))
async def skip_send_example(message: Message, state: Onboarding) -> None:
    await set_report_time(message, state)


async def set_report_time(message: Message, state: Onboarding) -> None:
    await message.answer("Во сколько напомнить подвести итоги?")
    await state.set_state(Onboarding.set_report_time)


@dp.message(Onboarding.set_report_time)
async def save_report_time(message: Message, state: Onboarding) -> None:
    report_time = message.text
    data = await state.get_data()
    goals = data.get("goals", [])
    DB.save_user(
        user_id=message.from_user.id,
        data={
            "area": data.get("area"),
            "goals": goals,
            "report_time": report_time,
        },
    )
    await message.answer("Супер! Жду твоих апдейтов. Успехов! 🚀")
    await state.clear()


def main() -> None:
    """Start polling."""

    dp.run_polling(bot)


if __name__ == "__main__":
    main()
