import test.news.crawlers.conftest
from datetime import datetime, timedelta, timezone

import news.crawlers.db.schema
import news.crawlers.udn
import news.crawlers.util.request_url
import news.crawlers.util.status_code


def test_get_news_list() -> None:
    news_list = news.crawlers.udn.get_news_list(
        current_datetime=datetime.now(tz=timezone.utc) + timedelta(hours=8),
        first_page=1,
        last_page=2,
        past_datetime=datetime.now(tz=timezone.utc)
        - timedelta(days=1, hours=16),
        continue_fail_count=5,
        debug=False,
    )

    # If news were successfully crawled, then `news_list` is not empty.
    assert len(news_list) >= 1

    for n in news_list:
        assert isinstance(n, news.crawlers.db.schema.RawNews)
        assert isinstance(n.idx, int)
        assert n.company_id == news.crawlers.udn.COMPANY_ID
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

    news.crawlers.udn.get_news_list(
        current_datetime=datetime.now(tz=timezone.utc),
        first_page=1,
        last_page=1,
        past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
        continue_fail_count=1,
        debug=True,
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

    news.crawlers.udn.get_news_list(
        current_datetime=datetime.now(tz=timezone.utc),
        first_page=1,
        last_page=2,
        past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
        continue_fail_count=1,
        debug=True,
    )
    captured = capsys.readouterr()

    assert 'URL not found.' in captured.out
