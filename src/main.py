from config import Config
from logger import get_logger
from notifier import DiscordNotifier


logger = get_logger(__name__)


def run() -> None:

    logger.info("Stock Agent starting...")

    Config.validate()

    notifier = DiscordNotifier()

    notifier.send(
        "🚀 Stock Agent connected successfully."
    )

    logger.info("Stock Agent completed successfully.")


if __name__ == "__main__":
    try:
        run()

    except Exception as exc:

        logger.exception(
            "Fatal application error: %s",
            exc
        )

        raise