import news.crawlers.util.normalize


def test_get_company_id() -> None:
    r"""Must reserve company id mapping."""
    assert news.crawlers.util.normalize.get_company_id(company='中時') == 0
    assert news.crawlers.util.normalize.get_company_id(company='中央社') == 1
    assert news.crawlers.util.normalize.get_company_id(company='大紀元') == 2
    assert news.crawlers.util.normalize.get_company_id(company='東森') == 3
    assert news.crawlers.util.normalize.get_company_id(company='民視') == 4
    assert news.crawlers.util.normalize.get_company_id(company='自由') == 5
    assert news.crawlers.util.normalize.get_company_id(company='新唐人') == 6
    assert news.crawlers.util.normalize.get_company_id(company='三立') == 7
    assert news.crawlers.util.normalize.get_company_id(company='風傳媒') == 8
    assert news.crawlers.util.normalize.get_company_id(company='tvbs') == 9
    assert news.crawlers.util.normalize.get_company_id(company='聯合報') == 10
