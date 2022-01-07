from typing import List

import pytest

import news.crawlers.db.read
import news.crawlers.db.schema
import news.crawlers.tvbs
import news.crawlers.util.request_url


def test_first_idx(
    db_name: str,
    cleanup_db_file,
) -> None:
    r"""Must have `first_idx > 0`."""
    with pytest.raises(ValueError) as excinfo:
        news.crawlers.tvbs.main(
            db_name=db_name,
            first_idx=0,
            latest_idx=1,
        )

    assert 'Must have `first_idx > 0`.' in str(excinfo.value)


def test_latest_idx(
    db_name: str,
    cleanup_db_file,
    monkeypatch,
) -> None:
    r"""Must have `latest_idx > 0`"""
    with pytest.raises(ValueError) as excinfo:
        news.crawlers.tvbs.main(
            db_name=db_name,
            first_idx=1,
            latest_idx=0,
        )

    assert 'Must have `latest_idx > 0`.' in str(excinfo.value)


def test_idx_order(
    db_name: str,
    cleanup_db_file,
) -> None:
    r"""Must have `first_idx <= latest_idx`."""
    with pytest.raises(ValueError) as excinfo:
        news.crawlers.tvbs.main(
            db_name=db_name,
            first_idx=2,
            latest_idx=1,
        )

    assert 'Must have `first_idx <= latest_idx`.' in str(excinfo.value)


def test_save_news_to_db(
    db_name: str,
    cleanup_db_file,
    monkeypatch,
) -> None:
    r"""Save crawling news to database with correct format."""

    def mock_get_latest_available_news_idx(**kwargs) -> int:
        return 1

    def mock_get_all_available_news_idx(**kwargs) -> List[int]:
        return [1, 2, 3]

    def mock_get_news_list(**kwargs) -> List[news.crawlers.db.schema.RawNews]:
        return [
            news.crawlers.db.schema.RawNews(
                idx=0,
                company_id=news.crawlers.tvbs.COMPANY_ID,
                raw_xml='abc',
                url_pattern='123',
            ),
            news.crawlers.db.schema.RawNews(
                idx=0,
                company_id=news.crawlers.tvbs.COMPANY_ID,
                raw_xml='def',
                url_pattern='456',
            ),
        ]

    monkeypatch.setattr(
        news.crawlers.tvbs,
        'get_latest_available_news_idx',
        mock_get_latest_available_news_idx,
    )

    monkeypatch.setattr(
        news.crawlers.tvbs,
        'get_all_available_news_idx',
        mock_get_all_available_news_idx,
    )

    monkeypatch.setattr(
        news.crawlers.tvbs,
        'get_news_list',
        mock_get_news_list,
    )

    news.crawlers.tvbs.main(
        db_name=db_name,
        first_idx=1,
        latest_idx=3,
    )

    all_records = news.crawlers.db.read.read_all_records(db_name=db_name)
    assert len(all_records)

    for record in all_records:
        assert isinstance(record, news.crawlers.db.schema.RawNews)
        assert isinstance(record.idx, int)
        assert record.company_id == news.crawlers.tvbs.COMPANY_ID
        assert isinstance(record.raw_xml, str)
        assert isinstance(record.url_pattern, str)
