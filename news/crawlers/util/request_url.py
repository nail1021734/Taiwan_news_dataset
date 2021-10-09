from typing import Final, Optional

import requests


def get(
    url: Final[str],
    *,
    timeout: Final[Optional[float]] = 20.0,
) -> requests.Response:
    r"""Launch HTTP GET request to specified URL."""
    response = requests.get(
        allow_redirects=True,
        timeout=timeout,
        url=url,
    )
    response.close()
    return response
