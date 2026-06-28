import feedparser 

from logger import get_logger
from models.articles import Article

logger = get_logger(__name__)

RSS_URL = (
    "https://news.google.com/rss/search?"
    "q=Indian+stock+market&hl=en-IN&gl=IN&ceid=IN:en"
)


class RSSService:

    def __init__(self):
        logger.info("RSS Service initialized.")

    def get_latest_articles(self) -> list[Article]:
        logger.info("Fetching latest articles from RSS feed...")

        feed = feedparser.parse(RSS_URL)

        if feed.bozo:
            logger.error("Failed to parse RSS feed.")
            return []

        articles: list[Article] = []

        for entry in feed.entries:

            article = Article(
                title=entry.get("title", ""),
                summary=entry.get("summary", ""),
                link=entry.get("link", ""),
                source=feed.feed.get("title", "Unknown Source"),
                published_at=None
            )

            articles.append(article)

        logger.info("Fetched %d articles.", len(articles))

        return articles