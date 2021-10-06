import inspect
import sqlite3
from inspect import Parameter, Signature

import news.db


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.db, 'get_conn')
    assert inspect.isfunction(news.db.get_conn)
    assert inspect.signature(news.db.get_conn) == Signature(
        parameters=[
            Parameter(
                name='db_path',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=str
            ),
        ],
        return_annotation=sqlite3.Connection,
    )
