import pytest

import news.crawlers.db.schema


def test_init() -> None:
    r"""Instance of `RawNews` must be iterable.

    Iterator will generate following attributes in order:
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

    attrs_gen = iter(raw_news)

    assert next(attrs_gen) == idx
    assert next(attrs_gen) == company_id
    assert next(attrs_gen) == raw_xml
    assert next(attrs_gen) == url_pattern

    with pytest.raises(StopIteration):
        next(attrs_gen)
