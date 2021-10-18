from typing import Final

import news.db
import news.parse.db.create
import news.parse.db.schema
import news.parse.db.util
import news.parse.db.write


def test_write_new_records(
    db_name: Final[str],
    cleanup_db_file: Final,
) -> None:
    idx = 123
    article = 'abc'
    category = 'def'
    company_id = 456
    datetime = 789
    reporter = 'ghi'
    title = 'jkl'
    url_pattern = 'mno'

    parsed_news = news.parse.db.schema.ParsedNews(
        idx=idx,
        article=article,
        category=category,
        company_id=company_id,
        datetime=datetime,
        reporter=reporter,
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
