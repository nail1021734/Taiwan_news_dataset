import pytest

import news.parse.db.schema


def test_init() -> None:
    r"""Instance of `ParsedNews` must be iterable.

    Iterator will generate following attributes in order:
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

    attrs_gen = iter(parsed_news)

    assert next(attrs_gen) == idx
    assert next(attrs_gen) == article
    assert next(attrs_gen) == category
    assert next(attrs_gen) == company_id
    assert next(attrs_gen) == datetime
    assert next(attrs_gen) == reporter
    assert next(attrs_gen) == title
    assert next(attrs_gen) == url_pattern

    with pytest.raises(StopIteration):
        next(attrs_gen)
