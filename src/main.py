from config import Config
from logger import get_logger

from services.discord_service import DiscordService
from services.rss_service import RSSService

logger = get_logger(__name__)


def run() -> None:

    logger.info("Stock Agent starting...")

    Config.validate()

    rss_service = RSSService()
    discord_service = DiscordService()

    articles = rss_service.get_latest_articles()

    if not articles:
        logger.warning("No articles found from RSS feed.")
        return

    first_article = articles[0]

    message = (
        "📰 Latest Market News\n\n"
        f"Title : {first_article.title}\n\n"
        f"Source : {first_article.source}\n\n"
        f"Link : {first_article.link}"
    )

    discord_service.send(message)

    logger.info("Stock Agent completed successfully.")


if __name__ == "__main__":
    try:
        run()

    except Exception:
        logger.exception("Unhandled exception occurred.")
        raise