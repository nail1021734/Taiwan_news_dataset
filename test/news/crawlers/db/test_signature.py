import importlib


def test_submodule_signature():
    r"""Ensure submodules' signature."""
    assert importlib.import_module('news.crawlers.db.create')
    assert importlib.import_module('news.crawlers.db.read')
    assert importlib.import_module('news.crawlers.db.schema')
    assert importlib.import_module('news.crawlers.db.util')
    assert importlib.import_module('news.crawlers.db.write')
