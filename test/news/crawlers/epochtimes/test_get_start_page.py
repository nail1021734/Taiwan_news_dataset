import test.news.crawlers.conftest
from datetime import datetime, timedelta, timezone
from typing import Final

import news.crawlers.util
from news.crawlers.epochtimes import CATEGORY_API_LOOKUP_TABLE, get_start_page


def test_get_start_page() -> None:
    r"""Start page must be larger than 2."""
    current_datetime = datetime(
        year=2021,
        month=10,
        day=12,
        tzinfo=timezone.utc,
    )
    for category_api in CATEGORY_API_LOOKUP_TABLE.values():
        start_page = get_start_page(
            category_api=category_api,
            continue_fail_count=5,
            current_datetime=current_datetime - timedelta(days=90),
            debug=False,
            first_page=2,
            max_page=10,
            past_datetime=current_datetime - timedelta(days=91),
        )
        assert start_page > 2


def test_show_progress_bar(
    response_200: Final[test.news.crawlers.conftest.MockResponse],
    capsys: Final,
    monkeypatch: Final,
) -> None:
    r"""Must show progress bar when `debug = True`."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_200

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    get_start_page(
        category_api=list(CATEGORY_API_LOOKUP_TABLE.values())[0],
        continue_fail_count=1,
        current_datetime=datetime.now(tz=timezone.utc),
        debug=True,
        first_page=2,
        max_page=10,
        past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
    )
    captured = capsys.readouterr()

    # `tqdm` will output to stderr and thus `captured.err` is not empty.
    assert 'Find start page' in captured.err


def test_show_error_statistics(
    response_404: Final[test.news.crawlers.conftest.MockResponse],
    capsys: Final,
    monkeypatch: Final,
) -> None:
    r"""Must show error statistics when `debug = True`."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_404

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    get_start_page(
        category_api=list(CATEGORY_API_LOOKUP_TABLE.values())[0],
        continue_fail_count=1,
        current_datetime=datetime.now(tz=timezone.utc),
        debug=True,
        first_page=2,
        max_page=10,
        past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
    )
    captured = capsys.readouterr()

    assert 'URL not found.' in captured.out
