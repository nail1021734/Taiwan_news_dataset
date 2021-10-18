import inspect
import sqlite3
from inspect import Parameter, Signature
from typing import Final, List, Sequence

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
                annotation=Final[str],
            ),
        ],
        return_annotation=sqlite3.Connection,
    )
    assert hasattr(news.db, 'is_sqlite3_file')
    assert inspect.isfunction(news.db.is_sqlite3_file)
    assert inspect.signature(news.db.is_sqlite3_file) == Signature(
        parameters=[
            Parameter(
                name='file_path',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
        ],
        return_annotation=bool,
    )
    assert hasattr(news.db, 'get_db_paths')
    assert inspect.isfunction(news.db.get_db_paths)
    assert inspect.signature(news.db.get_db_paths) == Signature(
        parameters=[
            Parameter(
                name='file_paths',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[Sequence[str]],
            ),
        ],
        return_annotation=List[str],
    )
