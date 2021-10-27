import inspect
from datetime import datetime
from inspect import Parameter, Signature

import news.parse.db.schema


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.parse.db.schema, 'ParsedNews')
    assert inspect.isclass(news.parse.db.schema.ParsedNews)


def test_class_attribute() -> None:
    r"""Ensure class attributes' signature."""
    assert hasattr(news.parse.db.schema.ParsedNews, 'idx')
    assert news.parse.db.schema.ParsedNews.idx == 0
    assert hasattr(news.parse.db.schema.ParsedNews, 'article')
    assert news.parse.db.schema.ParsedNews.article == ''
    assert hasattr(news.parse.db.schema.ParsedNews, 'category')
    assert news.parse.db.schema.ParsedNews.category is None
    assert hasattr(news.parse.db.schema.ParsedNews, 'company_id')
    assert news.parse.db.schema.ParsedNews.company_id == 0
    assert hasattr(news.parse.db.schema.ParsedNews, 'reporter')
    assert news.parse.db.schema.ParsedNews.reporter is None
    assert hasattr(news.parse.db.schema.ParsedNews, 'timestamp')
    assert news.parse.db.schema.ParsedNews.timestamp == 0
    assert hasattr(news.parse.db.schema.ParsedNews, 'title')
    assert news.parse.db.schema.ParsedNews.title == ''
    assert hasattr(news.parse.db.schema.ParsedNews, 'url_pattern')
    assert news.parse.db.schema.ParsedNews.url_pattern == ''


def test_instance_method() -> None:
    r"""Ensure instance methods' signature."""
    assert hasattr(news.parse.db.schema.ParsedNews, '__iter__')
    assert inspect.isfunction(news.parse.db.schema.ParsedNews.__iter__)
    assert inspect.signature(
        news.parse.db.schema.ParsedNews.__iter__,
    ) == Signature(
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
    assert hasattr(news.parse.db.schema.ParsedNews, 'get_datetime')
    assert inspect.isfunction(news.parse.db.schema.ParsedNews.get_datetime)
    assert inspect.signature(
        news.parse.db.schema.ParsedNews.get_datetime,
    ) == Signature(
        parameters=[
            Parameter(
                name='self',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Parameter.empty,
            ),
        ],
        return_annotation=datetime,
    )
    assert hasattr(news.parse.db.schema.ParsedNews, 'get_datetime_str')
    assert inspect.isfunction(news.parse.db.schema.ParsedNews.get_datetime_str)
    assert inspect.signature(
        news.parse.db.schema.ParsedNews.get_datetime_str,
    ) == Signature(
        parameters=[
            Parameter(
                name='self',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Parameter.empty,
            ),
        ],
        return_annotation=str,
    )
    assert hasattr(news.parse.db.schema.ParsedNews, 'pretify')
    assert inspect.isfunction(news.parse.db.schema.ParsedNews.pretify)
    assert inspect.signature(
        news.parse.db.schema.ParsedNews.pretify,
    ) == Signature(
        parameters=[
            Parameter(
                name='self',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Parameter.empty,
            ),
        ],
        return_annotation=str,
    )
