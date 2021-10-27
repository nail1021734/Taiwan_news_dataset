import test.news.crawlers.conftest
from datetime import datetime, timedelta, timezone

import news.crawlers.db.schema
import news.crawlers.epochtimes
import news.crawlers.util.request_url
from news.crawlers.epochtimes import CATEGORY_API_LOOKUP_TABLE, get_news_list


def test_get_news_list() -> None:
    r"""Must return list of `RawNews`."""

    for category_api in CATEGORY_API_LOOKUP_TABLE.values():
        news_list = get_news_list(
            category_api=category_api,
            continue_fail_count=1,
            current_datetime=datetime.now(tz=timezone.utc),
            debug=False,
            first_page=2,
            last_page=3,
            past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=30),
        )

        # If news were successfully crawled, then `news_list` is not empty.
        assert len(news_list) >= 1

        for n in news_list:
            assert isinstance(n, news.crawlers.db.schema.RawNews)
            assert isinstance(n.idx, int)
            assert n.company_id == news.crawlers.epochtimes.COMPANY_ID
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
        category_api=list(CATEGORY_API_LOOKUP_TABLE.values())[0],
        continue_fail_count=1,
        current_datetime=datetime.now(tz=timezone.utc),
        debug=True,
        first_page=2,
        last_page=3,
        past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
    )
    captured = capsys.readouterr()

    # `tqdm` will output to stderr and thus `captured.err` is not empty.
    assert 'Crawling' in captured.err


def test_show_error_statistics(
    response_404: test.news.crawlers.conftest.MockResponse,
    capsys,
    monkeypatch,
) -> None:
    r"""Must show error statistics when `debug = True`."""

    def mock_get(**kwargs) -> test.news.crawlers.conftest.MockResponse:
        return response_404

    monkeypatch.setattr(
        news.crawlers.util.request_url,
        'get',
        mock_get,
    )

    get_news_list(
        category_api=list(CATEGORY_API_LOOKUP_TABLE.values())[0],
        continue_fail_count=1,
        current_datetime=datetime.now(tz=timezone.utc),
        debug=True,
        first_page=2,
        last_page=3,
        past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
    )
    captured = capsys.readouterr()

    assert 'URL not found.' in captured.out
