import inspect
from inspect import Parameter, Signature

import news.crawlers.db.util


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.db.util, 'get_db_path')
    assert inspect.isfunction(news.crawlers.db.util.get_db_path)
    assert inspect.signature(news.crawlers.db.util.get_db_path) == Signature(
        parameters=[
            Parameter(
                name='db_name',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=str,
            ),
        ],
        return_annotation=str,
    )
