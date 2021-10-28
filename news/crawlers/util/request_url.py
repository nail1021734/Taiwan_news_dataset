from typing import Optional

import requests


def get(
    url: str,
    *,
    timeout: Optional[float] = 20.0,
) -> requests.Response:
    r"""Launch HTTP GET request to specified URL."""
    response = requests.get(
        allow_redirects=True,
        timeout=timeout,
        url=url,
    )
    response.close()
    return response
