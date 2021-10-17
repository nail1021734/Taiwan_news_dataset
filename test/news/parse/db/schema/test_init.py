import news.parse.db.schema


def test_init() -> None:
    r"""Instance of `ParsedNews` must include correct attributes.

    Correct attributes includes:
    - `idx`
    - `article`
    - `category`
    - `company_id`
    - `datetime`
    - `reporter`
    - `title`
    - `url_pattern`
    """
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

    assert parsed_news.idx == idx
    assert parsed_news.article == article
    assert parsed_news.category == category
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == datetime
    assert parsed_news.reporter == reporter
    assert parsed_news.title == title
    assert parsed_news.url_pattern == url_pattern
