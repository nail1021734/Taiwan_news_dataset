import news.crawlers.storm


def test_page_found() -> None:
    r"""Must return `False` when page is found."""
    assert not news.crawlers.storm.page_not_found(
        raw_xml='<h1 id="article_title"></h1>',
    )


def test_page_not_found() -> None:
    r"""Must return `True` when page not found."""
    assert news.crawlers.storm.page_not_found(raw_xml='')
