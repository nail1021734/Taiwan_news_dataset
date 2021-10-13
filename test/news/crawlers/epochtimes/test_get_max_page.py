from news.crawlers.epochtimes import CATEGORY_API_LOOKUP_TABLE, get_max_page


def test_get_max_page() -> None:
    r"""Each category must have at least 100 pages.

    100 is choose by observation.  If any error occured, `get_max_page` must
    return `1`.
    """
    for category_api in CATEGORY_API_LOOKUP_TABLE.values():
        max_page = get_max_page(category_api=category_api)
        assert max_page >= 100 or max_page == 1
