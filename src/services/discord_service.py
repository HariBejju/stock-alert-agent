import requests

from config import Config
from logger import get_logger


logger = get_logger(__name__)


class DiscordService:

    def send(self, message: str) -> None:

        response = requests.post(
            Config.DISCORD_WEBHOOK_URL,
            json={"content": message},
            timeout=10
        )

        response.raise_for_status()

        logger.info(
            "Discord notification sent successfully."
        )