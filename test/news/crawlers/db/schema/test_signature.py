import inspect
from inspect import Parameter, Signature

import news.crawlers.db.schema


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.db.schema, 'RawNews')
    assert inspect.isclass(news.crawlers.db.schema.RawNews)


def test_class_attribute() -> None:
    r"""Ensure class attributes' signature."""
    assert hasattr(news.crawlers.db.schema.RawNews, 'idx')
    assert isinstance(news.crawlers.db.schema.RawNews.idx, int)
    assert news.crawlers.db.schema.RawNews.idx == 0
    assert hasattr(news.crawlers.db.schema.RawNews, 'company_id')
    assert isinstance(news.crawlers.db.schema.RawNews.company_id, int)
    assert news.crawlers.db.schema.RawNews.company_id == 0
    assert hasattr(news.crawlers.db.schema.RawNews, 'raw_xml')
    assert isinstance(news.crawlers.db.schema.RawNews.raw_xml, str)
    assert news.crawlers.db.schema.RawNews.raw_xml == ''
    assert hasattr(news.crawlers.db.schema.RawNews, 'url_pattern')
    assert isinstance(news.crawlers.db.schema.RawNews.url_pattern, str)
    assert news.crawlers.db.schema.RawNews.url_pattern == ''


def test_instance_method() -> None:
    r"""Ensure instance methods' signature."""
    assert hasattr(news.crawlers.db.schema.RawNews, '__iter__')
    assert inspect.isfunction(news.crawlers.db.schema.RawNews.__iter__)
    assert inspect.signature(news.crawlers.db.schema.RawNews.__iter__) \
        == Signature(
            parameters=[
                Parameter(
                    name='self',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Parameter.empty,
                ),
            ],
            return_annotation=Signature.empty,
        )
