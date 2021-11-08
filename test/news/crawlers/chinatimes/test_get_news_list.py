import test.news.crawlers.conftest
from datetime import datetime, timedelta, timezone

import news.crawlers.chinatimes
import news.crawlers.db.schema
import news.crawlers.util.request_url


def test_get_news_list() -> None:
    r"""Crawling news on October 12th, 2021, utc."""
    continue_fail_count = 2

    news_list = news.crawlers.chinatimes.get_news_list(
        continue_fail_count=continue_fail_count,
        current_datetime=datetime(
            year=2021,
            month=10,
            day=12,
            tzinfo=timezone.utc,
        ),
        debug=False,
        max_news_per_day=10,
    )

    # If news were successfully crawled, then `news_list` is not empty.
    assert len(news_list) >= 1

    for n in news_list:
        assert isinstance(n, news.crawlers.db.schema.RawNews)
        assert isinstance(n.idx, int)
        assert n.company_id == news.crawlers.chinatimes.COMPANY_ID
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

    news.crawlers.chinatimes.get_news_list(
        continue_fail_count=1,
        current_datetime=datetime.now(tz=timezone.utc) - timedelta(days=1),
        debug=True,
        max_news_per_day=1,
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

    news.crawlers.chinatimes.get_news_list(
        continue_fail_count=1,
        current_datetime=datetime.now(tz=timezone.utc) - timedelta(days=1),
        debug=True,
        max_news_per_day=1,
    )
    captured = capsys.readouterr()

    # It will output 'URL not found'.
    assert 'URL not found.' in captured.out
