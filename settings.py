from pydantic_settings import BaseSettings


class H4X0RSettings(BaseSettings):

    TELEGRAM_BOT_TOKEN: str
    APP_ID: int
    API_HASH: str
    PHONE_NUMBER: str
    OWNER_USERNAME: str
    GOOGLE_API: str
    IS_ENABLED: bool = False

    class Config:
        env_file = ".env"


h4x0r_settings = H4X0RSettings()
