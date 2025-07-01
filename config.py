"""Configuration utilities for the Telegram bot.

Usage:
    from config import load_config
    cfg = load_config()
    print(cfg.bot_token)
"""
from dataclasses import dataclass
import os


@dataclass
class Config:
    """Basic application settings."""

    bot_token: str
    db_path: str = "all.db"


def load_config() -> Config:
    """Load configuration from environment variables.

    Environment variables:
        BOT_API: Telegram bot token.
        DB_PATH: Path to the SQLite database (optional).
    """

    return Config(
        bot_token=os.getenv("BOT_API", ""),
        db_path=os.getenv("DB_PATH", "all.db"),
    )
