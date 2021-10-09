import news.crawlers.util.normalize


def test_compress_raw_xml() -> None:
    r"""Must strip and collapse multiple whitespaces."""
    assert (
        news.crawlers.util.normalize.compress_raw_xml(' abc  def ')
        ==
        'abc def'
    )
