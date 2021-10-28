import test.news.crawlers.conftest
from datetime import datetime, timezone

import news.crawlers.db.schema
import news.crawlers.util.request_url
from news.crawlers.ftv import (
    CATEGORY_API_LOOKUP_TABLE, COMPANY_ID, get_news_list
)


def test_get_news_list() -> None:
    r"""Crawling news on October 12th, 2021, utc."""
    for category_api in CATEGORY_API_LOOKUP_TABLE.keys():
        news_list = get_news_list(
            category_api=category_api,
            continue_fail_count=2,
            current_datetime=datetime(
                year=2021,
                month=10,
                day=12,
                tzinfo=timezone.utc,
            ),
            debug=False,
        )

        # If news were successfully crawled, then `news_list` is not empty.
        # But this is only true when `category_api == 'W'`.
        if category_api == 'W':
            assert len(news_list) >= 1

        for n in news_list:
            assert isinstance(n, news.crawlers.db.schema.RawNews)
            assert isinstance(n.idx, int)
            assert n.company_id == COMPANY_ID
            assert isinstance(n.raw_xml, str)
            assert isinstance(n.url_pattern, str)


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

    get_news_list(
        category_api=list(CATEGORY_API_LOOKUP_TABLE.keys())[0],
        continue_fail_count=1,
        current_datetime=datetime(
            year=2021,
            month=10,
            day=12,
            tzinfo=timezone.utc,
        ),
        debug=True,
    )
    captured = capsys.readouterr()

    # `tqdm` will output to stderr and thus `captured.err` is not empty.
    assert 'Crawling' in captured.err


def test_show_error_statistics(
    response_410: test.news.crawlers.conftest.MockResponse,
    capsys,
    monkeypatch,
) -> None:
    r"""Must show error statistics when `debug = True`."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_410

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    get_news_list(
        category_api=list(CATEGORY_API_LOOKUP_TABLE.keys())[0],
        continue_fail_count=1,
        current_datetime=datetime(
            year=2021,
            month=10,
            day=12,
            tzinfo=timezone.utc,
        ),
        debug=True,
    )
    captured = capsys.readouterr()

    assert 'URL not found.' in captured.out
