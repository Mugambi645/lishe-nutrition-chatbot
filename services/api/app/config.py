from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://lishe:lishe@localhost:4322/lishe"
    )
    redis_url: str ="redis://localhost:6079/0"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    huggingface_api_token: str = ""

    model_config = {"env_prefix": "LISHE_"}


settings = Settings()