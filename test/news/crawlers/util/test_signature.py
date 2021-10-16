import importlib


def test_submodule_signature() -> None:
    r"""Ensure submodules' signature."""
    assert importlib.import_module('news.crawlers.util.normalize')
    assert importlib.import_module('news.crawlers.util.request_url')
    assert importlib.import_module('news.crawlers.util.status_code')
