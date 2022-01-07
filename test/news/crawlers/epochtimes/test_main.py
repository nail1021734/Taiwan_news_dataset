import test.news.crawlers.conftest
from datetime import datetime, timedelta, timezone
from typing import List

import pytest

import news.crawlers.db.read
import news.crawlers.db.schema
import news.crawlers.epochtimes


def test_utc_timezone(
    db_name: str,
    cleanup_db_file,
) -> None:
    r"""`current_datetime` and `past_datetime` must in utc timezone."""
    taiwan_current_datetime = datetime.now(
        tz=timezone(offset=timedelta(hours=8)),
    )
    with pytest.raises(ValueError) as excinfo:
        news.crawlers.epochtimes.main(
            current_datetime=taiwan_current_datetime,
            db_name=db_name,
            past_datetime=datetime.now(tz=timezone.utc),
        )

    assert '`current_datetime` must in utc timezone.' in str(excinfo.value)
    taiwan_current_datetime = datetime.now(
        tz=timezone(offset=timedelta(hours=8)),
    )

    with pytest.raises(ValueError) as excinfo:
        news.crawlers.epochtimes.main(
            current_datetime=datetime.now(tz=timezone.utc),
            db_name=db_name,
            past_datetime=taiwan_current_datetime,
        )

    assert '`past_datetime` must in utc timezone.' in str(excinfo.value)


def test_datetime_order(
    db_name: str,
    cleanup_db_file,
) -> None:
    r"""Must have `past_datetime <= current_datetime`."""
    with pytest.raises(ValueError) as excinfo:
        news.crawlers.epochtimes.main(
            current_datetime=datetime.now(tz=timezone.utc),
            db_name=db_name,
            past_datetime=datetime.now(tz=timezone.utc) + timedelta(days=2),
        )

    assert (
        'Must have `past_datetime <= current_datetime`.' in str(excinfo.value)
    )


def test_save_news_to_db(
    db_name: str,
    response_200: test.news.crawlers.conftest.MockResponse,
    cleanup_db_file,
    monkeypatch,
) -> None:
    r"""Save crawling news to database with correct format."""

    def mock_get_max_page(**kwargs) -> int:
        return 2

    def mock_get_start_page(**kwargs) -> int:
        return 2

    def mock_get_news_list(**kwargs) -> List[news.crawlers.db.schema.RawNews]:
        return [
            news.crawlers.db.schema.RawNews(
                idx=0,
                company_id=news.crawlers.epochtimes.COMPANY_ID,
                raw_xml='abc',
                url_pattern='123',
            ),
            news.crawlers.db.schema.RawNews(
                idx=0,
                company_id=news.crawlers.epochtimes.COMPANY_ID,
                raw_xml='def',
                url_pattern='456',
            ),
        ]

    monkeypatch.setattr(
        news.crawlers.epochtimes,
        'get_max_page',
        mock_get_max_page,
    )
    monkeypatch.setattr(
        news.crawlers.epochtimes,
        'get_start_page',
        mock_get_start_page,
    )
    monkeypatch.setattr(
        news.crawlers.epochtimes,
        'get_news_list',
        mock_get_news_list,
    )

    news.crawlers.epochtimes.main(
        continue_fail_count=1,
        current_datetime=datetime.now(tz=timezone.utc),
        db_name=db_name,
        debug=False,
        past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
    )

    all_records = news.crawlers.db.read.read_all_records(db_name=db_name)
    assert len(all_records)

    for record in all_records:
        assert isinstance(record, news.crawlers.db.schema.RawNews)
        assert isinstance(record.idx, int)
        assert record.company_id == news.crawlers.epochtimes.COMPANY_ID
        assert isinstance(record.raw_xml, str)
        assert isinstance(record.url_pattern, str)
