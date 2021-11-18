import news.db
import news.parse.db.create
import news.parse.db.read
import news.parse.db.schema
import news.parse.db.util
import news.parse.db.write


def test_read_some_records(db_name: str, cleanup_db_file) -> None:
    # Randomly create two records.
    # Note that SQLite's index start with 1.
    news_list = [
        news.parse.db.schema.ParsedNews(
            idx=1,
            article='abc',
            category='def',
            company_id=123,
            reporter='ghi',
            timestamp=456,
            title='jkl',
            url_pattern='mno',
        ),
        news.parse.db.schema.ParsedNews(
            idx=2,
            article='cba',
            category='fed',
            company_id=321,
            reporter='ihg',
            timestamp=654,
            title='lkj',
            url_pattern='onm',
        ),
        news.parse.db.schema.ParsedNews(
            idx=3,
            article='aaa',
            category=None,
            company_id=111,
            reporter=None,
            timestamp=222,
            title='bbb',
            url_pattern='ccc',
        ),
    ]

    try:
        db_path = news.parse.db.util.get_db_path(db_name=db_name)
        conn = news.db.get_conn(db_path=db_path)
        cur = conn.cursor()
        news.parse.db.create.create_table(cur=cur)
        news.parse.db.write.write_new_records(
            cur=cur,
            news_list=news_list,
        )
        conn.commit()
    finally:
        conn.close()

    # No error is good.
    all_records = news.parse.db.read.read_some_records(
        db_name=db_name,
        limit=2,
        offset=0,
    )
    assert len(all_records) == 2
    for r1, r2 in zip(all_records, news_list[:2]):
        assert r1.idx == r2.idx
        assert r1.article == r2.article
        assert r1.category == r2.category
        assert r1.company_id == r2.company_id
        assert r1.reporter == r2.reporter
        assert r1.timestamp == r2.timestamp
        assert r1.title == r2.title
        assert r1.url_pattern == r2.url_pattern

    # No error is good.
    all_records = news.parse.db.read.read_some_records(
        db_name=db_name,
        limit=2,
        offset=1,
    )
    for r1, r2 in zip(all_records, news_list[1:]):
        assert r1.idx == r2.idx
        assert r1.article == r2.article
        assert r1.category == r2.category
        assert r1.company_id == r2.company_id
        assert r1.reporter == r2.reporter
        assert r1.timestamp == r2.timestamp
        assert r1.title == r2.title
        assert r1.url_pattern == r2.url_pattern

    # No error is good.
    all_records = news.parse.db.read.read_some_records(
        db_name=db_name,
        limit=3,
        offset=1,
    )
    assert len(all_records) == 2
    for r1, r2 in zip(all_records, news_list[1:]):
        assert r1.idx == r2.idx
        assert r1.article == r2.article
        assert r1.category == r2.category
        assert r1.company_id == r2.company_id
        assert r1.reporter == r2.reporter
        assert r1.timestamp == r2.timestamp
        assert r1.title == r2.title
        assert r1.url_pattern == r2.url_pattern
