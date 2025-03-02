from pydantic_settings import BaseSettings


class H4X0RSettings(BaseSettings):

    CLOUD_URL: str
    CLOUD_PORT: int

    TELEGRAM_BOT_TOKEN: str
    PHONE_NUMBER: str
    OWNER_USERNAME: str
    GOOGLE_API: str
    IS_ENABLED: bool = False
    DUMP_FILES_PATH: str
    LLM_NAME: str
    DUMP_FILE_MAXIMUM_ITEMS_COUNT: int
    MUSIC_FOLDER: str
    BOT_NAMES: tuple = (
        "hector",
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
