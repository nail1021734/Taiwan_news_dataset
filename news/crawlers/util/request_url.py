from typing import Final, Optional
import requests
import cloudscraper


def get(
    url: Final[str],
    *,
    timeout: Final[Optional[float]] = 20.0,
    use_cloudscraper: Final[bool] = False,
) -> requests.Response:
    r"""Launch HTTP GET request to specified URL."""
    if use_cloudscraper and get.scraper is None:
        get.scraper = cloudscraper.create_scraper()
    req = get.scraper if use_cloudscraper else requests

    response = req.get(
        allow_redirects=True,
        timeout=timeout,
        url=url,
    )
    response.close()
    return response


get.scraper = None