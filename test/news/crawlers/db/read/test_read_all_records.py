import news.crawlers.db.create
import news.crawlers.db.read
import news.crawlers.db.schema
import news.crawlers.db.util
import news.crawlers.db.write
import news.db


def test_read_all_records(db_name: str, cleanup_db_file) -> None:
    # Randomly create two records.
    # Note that SQLite's index start with 1.
    news_list = [
        news.crawlers.db.schema.RawNews(
            idx=1,
            company_id=123,
            raw_xml='abc',
            url_pattern='def',
        ),
        news.crawlers.db.schema.RawNews(
            idx=2,
            company_id=456,
            raw_xml='ghi',
            url_pattern='jkl',
        ),
    ]

    try:
        db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
        conn = news.db.get_conn(db_path=db_path)
        cur = conn.cursor()
        news.crawlers.db.create.create_table(cur=cur)
        news.crawlers.db.write.write_new_records(
            cur=cur,
            news_list=news_list,
        )
        conn.commit()
    finally:
        conn.close()

    # No error is good.
    all_records = news.crawlers.db.read.read_all_records(db_name=db_name)
    assert len(all_records) == len(news_list) == 2
    for r1, r2 in zip(all_records, news_list):
        assert r1.idx == r2.idx
        assert r1.company_id == r2.company_id
        assert r1.raw_xml == r2.raw_xml
        assert r1.url_pattern == r2.url_pattern


def test_read_records_unique(db_name: str, cleanup_db_file) -> None:
    r"""Records in database must follow unique constraints."""
    news_list = [
        news.crawlers.db.schema.RawNews(
            idx=1,
            company_id=123,
            raw_xml='aaa',
            url_pattern='url',
        ),
        news.crawlers.db.schema.RawNews(
            idx=1,
            company_id=123,
            raw_xml='bbb',
            url_pattern='url',
        ),
        news.crawlers.db.schema.RawNews(
            idx=1,
            company_id=123,
            raw_xml='ccc',
            url_pattern='url',
        ),
    ]

    try:
        db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
        conn = news.db.get_conn(db_path=db_path)
        cur = conn.cursor()
        news.crawlers.db.create.create_table(cur=cur)
        news.crawlers.db.write.write_new_records(
            cur=cur,
            news_list=news_list,
        )
        conn.commit()
    finally:
        conn.close()

    # No error is good.
    all_records = news.crawlers.db.read.read_all_records(db_name=db_name)
    assert len(all_records) == 1
    assert all_records[0].idx == 1
    assert all_records[0].company_id == 123
    assert all_records[0].raw_xml == 'aaa'
    assert all_records[0].url_pattern == 'url'
