from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENROUTER_API_KEY: str
    WEBHOOK_URL: str
    WEBHOOK_PATH: str = "/webhook"
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    class Config:
        env_file = ".env"


settings = Settings()
