import os


class Config:

    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

    @classmethod
    def validate(cls) -> None:

        missing = []

        if not cls.DISCORD_WEBHOOK_URL:
            missing.append("DISCORD_WEBHOOK_URL")

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )