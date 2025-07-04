"""Speech-to-text via OpenAI Whisper.

Usage:
    from src.services.voice_service import transcribe_audio
    text = await transcribe_audio("path/to/file.ogg")
"""

from __future__ import annotations

import openai

from config import load_config


async def transcribe_audio(path: str) -> str:
    """Return text transcript for given audio file using Whisper API.

    Parameters
    ----------
    path: str
        Local path to audio file in a format supported by OpenAI.

    Returns
    -------
    str
        Recognized text or empty string on failure.
    """
    cfg = load_config()
    client = openai.OpenAI(api_key=cfg.api_id)
    with open(path, "rb") as file:
        response = await client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            response_format="text",
        )
    return str(response).strip()
