import hashlib
import json
from pathlib import Path

from logger import get_logger
from models.article import Article

logger = get_logger(__name__)

DATA_FILE = Path("data/processed_articles.json")


class DeduplicationService:

    def load_processed_articles(self) -> set[str]:
        """
        Load processed article IDs from the JSON file.
        """

        if not DATA_FILE.exists():
            logger.warning("Processed articles file not found. Creating a new one.")
            return set()

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            logger.info("Loaded %d processed article IDs.", len(data))
            return set(data)

        except Exception:
            logger.exception("Failed to load processed articles.")
            return set()

    def save_processed_articles(self, article_ids: set[str]) -> None:
        """
        Save processed article IDs to the JSON file.
        """

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(sorted(article_ids), file, indent=4)

            logger.info("Saved %d processed article IDs.", len(article_ids))

        except Exception:
            logger.exception("Failed to save processed articles.")
            raise

    def _generate_article_id(self, article: Article) -> str:
        """
        Generate a unique ID for an article using title + link.
        """

        unique_string = f"{article.title}|{article.link}"

        return hashlib.sha256(unique_string.encode("utf-8")).hexdigest()

    def filter_new_articles(self, articles: list[Article]) -> list[Article]:
        """
        Return only articles that haven't been processed before.
        """

        processed_ids = self.load_processed_articles()

        new_articles = []

        for article in articles:

            article_id = self._generate_article_id(article)

            if article_id in processed_ids:
                logger.info("Skipping duplicate article: %s", article.title)
                continue

            processed_ids.add(article_id)
            new_articles.append(article)

        self.save_processed_articles(processed_ids)

        logger.info(
            "New Articles: %d | Duplicates Skipped: %d",
            len(new_articles),
            len(articles) - len(new_articles),
        )

        return new_articles