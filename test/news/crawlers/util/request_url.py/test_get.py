from time import time

import pytest
import requests

import news.crawlers.util.request_url


def test_timeout() -> None:
    r"""Ensure timeout occur with tolerance time interval."""
    # Choose a private address that is unlikely to exist to prevent failures
    # due to the connect succeeding before the timeout. Use a dotted IP address
    # to avoid including the DNS lookup time with the connect time. This avoids
    # failing the assertion that the timeout occurred fast enough.
    tolerance_secs = 2.0
    timeout_secs = 2.0

    time_start = time()
    with pytest.raises(requests.Timeout):
        news.crawlers.util.request_url.get(
            timeout=timeout_secs,
            url='http://10.0.0.0:12345',
        )
    time_end = time()

    time_diff = abs(time_end - time_start)
    assert abs(timeout_secs - time_diff) <= tolerance_secs, \
        'Timeout occur beyond tolerance.'


def test_response() -> None:
    r"""Ensure GET request work."""
    # Launch request to a server which is almost impossible to shutdown.
    response = news.crawlers.util.request_url.get(url='https://google.com')
    assert isinstance(response, requests.Response)
    assert 'google' in response.text
