import test.news.crawlers.conftest
from typing import Final

import news.crawlers.db.schema
import news.crawlers.util.request_url
import news.crawlers.util.status_code
from news.crawlers.setn import (
    CATEGORY_API_LOOKUP_TABLE, COMPANY_ID, get_news_list
)


def test_get_news_list() -> None:
    r"""Crawling newest news."""
    for category_api in CATEGORY_API_LOOKUP_TABLE.values():
        news_list = get_news_list(
            category_api=category_api,
            continue_fail_count=1,
            debug=False,
            first_page=1,
            max_page=1,
        )

        # If news were successfully crawled, then `news_list` is not empty.
        assert len(news_list) >= 1

        for n in news_list:
            assert isinstance(n, news.crawlers.db.schema.RawNews)
            assert isinstance(n.idx, int)
            assert n.company_id == COMPANY_ID
            assert isinstance(n.raw_xml, str)
            assert isinstance(n.url_pattern, str)


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

    get_news_list(
        category_api=list(CATEGORY_API_LOOKUP_TABLE.values())[0],
        continue_fail_count=1,
        debug=True,
        first_page=1,
        max_page=1,
    )
    captured = capsys.readouterr()

    # `tqdm` will output to stderr and thus `captured.err` is not empty.
    assert 'Crawling' in captured.err


def test_show_error_statistics(
    response_404: Final[test.news.crawlers.conftest.MockResponse],
    capsys: Final,
    monkeypatch: Final,
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

    get_news_list(
        category_api=list(CATEGORY_API_LOOKUP_TABLE.values())[0],
        continue_fail_count=1,
        debug=True,
        first_page=1,
        max_page=1,
    )
    captured = capsys.readouterr()

    assert 'URL not found.' in captured.out
