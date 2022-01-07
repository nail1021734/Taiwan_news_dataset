import test.news.crawlers.conftest

import news.crawlers.util.request_url
import news.crawlers.util.status_code
from news.crawlers.tvbs import (
    CATEGORY_API_LOOKUP_TABLE, get_latest_available_news_idx
)


def test_get_latest_available_news_idx() -> None:
    for category in CATEGORY_API_LOOKUP_TABLE.keys():
        latest_ava_news_idx = get_latest_available_news_idx(
            category=category,
            continue_fail_count=1,
            debug=False,
            first_idx=1590000,
            latest_idx=1600000,
        )

        assert 1590000 <= latest_ava_news_idx <= 1600000


def test_show_progress_bar(
    response_200: test.news.crawlers.conftest.MockResponse,
    capsys,
    monkeypatch,
) -> None:
    r"""Must show progress bar when `debug = True`."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_200

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    get_latest_available_news_idx(
        category=list(CATEGORY_API_LOOKUP_TABLE.keys())[0],
        continue_fail_count=1,
        debug=True,
        first_idx=1590000,
        latest_idx=1600000,
    )
    captured = capsys.readouterr()

    # `tqdm` will output to stderr and thus `captured.err` is not empty.
    assert 'Find latest idx' in captured.err


def test_show_error_statistics(
    response_404: test.news.crawlers.conftest.MockResponse,
    capsys,
    monkeypatch,
) -> None:
    r"""Must show error statistics when `debug = True`."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_404

    def mock_check_status_code(**kwargs) -> None:
        raise Exception('URL not found.')

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    monkeypatch.setattr(
        news.crawlers.util.status_code,
        'check_status_code',
        mock_check_status_code,
    )

    get_latest_available_news_idx(
        category=list(CATEGORY_API_LOOKUP_TABLE.keys())[0],
        continue_fail_count=1,
        debug=True,
        first_idx=1590000,
        latest_idx=1600000,
    )
    captured = capsys.readouterr()

    assert 'URL not found.' in captured.out
