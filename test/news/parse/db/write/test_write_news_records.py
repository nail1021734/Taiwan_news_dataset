import news.db
import news.parse.db.create
import news.parse.db.schema
import news.parse.db.util
import news.parse.db.write


def test_write_new_records(
    db_name: str,
    cleanup_db_file,
) -> None:
    idx = 123
    article = 'abc'
    category = 'def'
    company_id = 456
    reporter = 'ghi'
    timestamp = 789
    title = 'jkl'
    url_pattern = 'mno'

    parsed_news = news.parse.db.schema.ParsedNews(
        idx=idx,
        article=article,
        category=category,
        company_id=company_id,
        reporter=reporter,
        timestamp=timestamp,
        title=title,
        url_pattern=url_pattern,
    )

    try:
        db_path = news.parse.db.util.get_db_path(db_name=db_name)
        conn = news.db.get_conn(db_path=db_path)
        cur = conn.cursor()
        news.parse.db.create.create_table(cur=cur)
        # No error is good.
        news.parse.db.write.write_new_records(
            cur=cur,
            news_list=[parsed_news],
        )
        conn.commit()
    finally:
        conn.close()


def test_write_duplicate_records(
    db_name: str,
    cleanup_db_file,
) -> None:
    r"""Writing duplicated records must fail with silence."""
    idx = 123
    article = 'abc'
    category = 'def'
    company_id = 456
    reporter = 'ghi'
    timestamp = 789
    title = 'jkl'
    url_pattern = 'mno'

    parsed_news = news.parse.db.schema.ParsedNews(
        idx=idx,
        article=article,
        category=category,
        company_id=company_id,
        reporter=reporter,
        timestamp=timestamp,
        title=title,
        url_pattern=url_pattern,
    )

    try:
        db_path = news.parse.db.util.get_db_path(db_name=db_name)
        conn = news.db.get_conn(db_path=db_path)
        cur = conn.cursor()
        news.parse.db.create.create_table(cur=cur)
        # No error is good.
        news.parse.db.write.write_new_records(
            cur=cur,
            news_list=[parsed_news, parsed_news],
        )
        conn.commit()
    finally:
        conn.close()
