from pydantic_settings import BaseSettings


class H4X0RSettings(BaseSettings):
    BOT_NAME: str
    VERSION: str

    SECRET_TELEGRAM_BOT_TOKEN: str

    SECRET_OWNER_CHAT_ID: str
    SECRET_GOOGLE_API: str
    SECRET_DATABASE_FILE: str
    LLM_NAME: str
    MAXIMUM_HISTORY_LENGTH: int

    SECRET_RUACCENT_MODEL_FOLDER: str
    SECRET_TTS_MODEL_FOLDER: str
    REACTIONS: list = [
        "👍",
        "👎",
        "❤",
        "🔥",
        "🥰",
        "👏",
        "😁",
        "🤔",
        "🤯",
        "😱",
        "🤬",
        "😢",
        "🎉",
        "🤩",
        "🤮",
        "💩",
        "🙏",
        "👌",
        "🕊",
        "🤡",
        "🥱",
        "🥴",
        "😍",
        "🐳",
        "❤‍🔥",
        "🌚",
        "🌭",
        "💯",
        "🤣",
        "⚡",
        "🍌",
        "🏆",
        "💔",
        "🤨",
        "😐",
        "🍓",
        "🍾",
        "💋",
        "🖕",
        "😈",
        "😴",
        "😭",
        "🤓",
        "👻",
        "👨‍💻",
        "👀",
        "🎃",
        "🙈",
        "😇",
        "😨",
        "🤝",
        "✍",
        "🤗",
        "🫡",
        "🎅",
        "🎄",
        "☃",
        "💅",
        "🤪",
        "🗿",
        "🆒",
        "💘",
        "🙉",
        "🦄",
        "😘",
        "💊",
        "🙊",
        "😎",
        "👾",
        "🤷‍♂",
        "🤷",
        "🤷‍♀",
        "😡",
    ]

    TTS_MODEL: str

    SECRET_VOICE_MESSAGES_FOLDER: str
    BOT_NAMES: tuple = (
        "гектор",
        "железяка",
        "байтоголовый",
        "битоголовый",
        "бот",
        "долбот",
        "иишнутый",
    )

    class Config:
        env_file = ".env"


h4x0r_settings = H4X0RSettings()
