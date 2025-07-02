
from dataclasses import dataclass
import os


@dataclass
class Config:

    bot_token: str
    api_id: str
    db_path: str = "all.db"


def load_config() -> Config:
    """Load configuration from environment variables.

    Environment variables:
        BOT_API: Telegram bot token.
        DB_PATH: Path to the SQLite database (optional).
    """

    return Config(
        bot_token=os.getenv("BOT_API", ""),
        api_id=os.getenv("OPENAI_API_KEY", ""),
        db_path=os.getenv("DB_PATH", "all.db"),
    )
