import importlib


def test_submodule_signature() -> None:
    r"""Ensure submodules' signature."""
    assert importlib.import_module('news.crawlers.chinatimes')
    assert importlib.import_module('news.crawlers.cna')
    assert importlib.import_module('news.crawlers.db')
    assert importlib.import_module('news.crawlers.epochtimes')
    assert importlib.import_module('news.crawlers.ettoday')
    assert importlib.import_module('news.crawlers.ftv')
    assert importlib.import_module('news.crawlers.ltn')
    assert importlib.import_module('news.crawlers.main')
    assert importlib.import_module('news.crawlers.ntdtv')
    assert importlib.import_module('news.crawlers.setn')
    assert importlib.import_module('news.crawlers.storm')
    assert importlib.import_module('news.crawlers.tvbs')
    assert importlib.import_module('news.crawlers.udn')
    assert importlib.import_module('news.crawlers.util')
