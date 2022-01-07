import news.crawlers.db.schema


def test_init() -> None:
    r"""Instance of `RawNews` must include correct attributes.

    Correct attributes includes:
    - `idx`
    - `company_id`
    - `raw_xml`
    - `url_pattern`
    """
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

    assert raw_news.idx == idx
    assert raw_news.company_id == company_id
    assert raw_news.raw_xml == raw_xml
    assert raw_news.url_pattern == url_pattern
