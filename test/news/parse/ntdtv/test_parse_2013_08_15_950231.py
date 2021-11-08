import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2013/08/15/a950276.html'
    response = news.crawlers.util.request_url.get(url=url)

    raw_news = news.crawlers.db.schema.RawNews(
        company_id=company_id,
        raw_xml=news.crawlers.util.normalize.compress_raw_xml(
            raw_xml=response.text,
        ),
        url_pattern=news.crawlers.util.normalize.compress_url(
            company_id=company_id,
            url=url,
        )
    )

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            由於幫派暴力加劇,南非當局發言人凱西(Bronagh Casey)說,由於教師對自身安危表示
            憂心,西開普敦省(Western Cape)教育廳「昨天決定,15日和16日將關閉曼恩伯格鎮
            (Manenberg)的學校」。共關閉開普敦郊區學校16所,大約1萬2000名學童只能留在家中而
            無法上學。 據中央社報導,開普敦低收入的曼恩伯格郊區近幾週來,已有至少50人因幫派
            暴力而喪命。這個郊區涵蓋惡名昭彰的開普平原區(Cape Flats)在內。 許多遇害者據報
            只是旁觀。凱西告訴記者:「教師及學童的安全,是我們主要的考量」。 這個地區有1所學校
            兩週前因槍擊案,而關閉1天。
            '''
        ),
    )
    assert parsed_news.category == '國際,社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1376496000
    assert parsed_news.reporter is None
    assert parsed_news.title == '幫派暴力 開普敦十多校關閉'
    assert parsed_news.url_pattern == '2013-08-15-950276'
