from typing import Final

import news.crawlers.db.create
import news.crawlers.db.schema
import news.crawlers.db.util
import news.crawlers.db.write
import news.db


def test_write_new_records(
    db_name: Final[str],
    cleanup_db_file: Final,
) -> None:
    idx = 123
    company_id = 456
    raw_xml = 'abc'
    url_pattern = 'def'

    raw_news = news.crawlers.db.schema.RawNews(
        idx=idx,
        company_id=company_id,
        raw_xml=raw_xml,
        url_pattern=url_pattern,
    )

    try:
        db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
        conn = news.db.get_conn(db_path=db_path)
        cur = conn.cursor()
        news.crawlers.db.create.create_table(cur=cur)
        # No error is good.
        news.crawlers.db.write.write_new_records(
            cur=cur,
            news_list=[raw_news],
        )
        conn.commit()
    finally:
        conn.close()