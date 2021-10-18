import importlib


def test_submodule_signature() -> None:
    r"""Ensure submodules' signature."""
    assert importlib.import_module('news.parse.db.create')
    assert importlib.import_module('news.parse.db.read')
    assert importlib.import_module('news.parse.db.schema')
    assert importlib.import_module('news.parse.db.util')
    assert importlib.import_module('news.parse.db.write')
