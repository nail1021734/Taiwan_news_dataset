import news.crawlers.db.create
import news.crawlers.db.read
import news.crawlers.db.schema
import news.crawlers.db.util
import news.crawlers.db.write
import news.db


def test_read_some_records(db_name: str, cleanup_db_file) -> None:
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
    all_records = news.crawlers.db.read.read_some_records(
        db_name=db_name,
        limit=1,
        offset=0,
    )
    assert len(all_records) == 1
    assert all_records[0].idx == news_list[0].idx
    assert all_records[0].company_id == news_list[0].company_id
    assert all_records[0].raw_xml == news_list[0].raw_xml
    assert all_records[0].url_pattern == news_list[0].url_pattern

    # No error is good.
    all_records = news.crawlers.db.read.read_some_records(
        db_name=db_name,
        limit=1,
        offset=1,
    )
    assert len(all_records) == 1
    assert all_records[0].idx == news_list[1].idx
    assert all_records[0].company_id == news_list[1].company_id
    assert all_records[0].raw_xml == news_list[1].raw_xml
    assert all_records[0].url_pattern == news_list[1].url_pattern

    # No error is good.
    all_records = news.crawlers.db.read.read_some_records(
        db_name=db_name,
        limit=2,
        offset=1,
    )
    assert len(all_records) == 1
    assert all_records[0].idx == news_list[1].idx
    assert all_records[0].company_id == news_list[1].company_id
    assert all_records[0].raw_xml == news_list[1].raw_xml
    assert all_records[0].url_pattern == news_list[1].url_pattern
