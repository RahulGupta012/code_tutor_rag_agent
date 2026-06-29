# from duckduckgo_search import DDGS
from ddgs import DDGS
import trafilatura

from app.utils.logger import logger


def search_web(
    query: str,
    max_results: int = 3
):

    logger.info(
        f"Searching Web: {query}"
    )

    documents = []

    with DDGS() as ddgs:

        results = list(
            ddgs.text(
                query,
                max_results=max_results
            )
        )

    for result in results:

        try:

            downloaded = trafilatura.fetch_url(
                result["href"]
            )

            if not downloaded:
                continue

            content = trafilatura.extract(
                downloaded
            )

            if not content:
                continue

            documents.append(
                {
                    "content": content,
                    "url": result["href"],
                    "title": result["title"]
                }
            )

        except Exception as e:

            logger.error(e)

    return documents 


# results = search_web(
#     "Difference between append and extend in python"
# )

# print(results[0]["title"])
# print(results[0]["url"])
# print(results[0]["content"][:1000])