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
    url = r'https://www.ntdtv.com/b5/2011/03/29/a511547.html'
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
            台灣海關28日首次發現日本包裝食品遭核輻射污染,台灣衛生署食品藥物管理局最近送驗一批
            日本烏龍麵,在外包裝上驗出碘131、銫134和銫137殘留。不過食品藥物管理局和原能會的
            官員都表示,含量遠低於標準值,民眾不需要恐慌。 日本進口的烏龍麵,外包裝上驗出碘131,
            每公斤14.8貝克、銫134,每公斤16.7貝克和銫137,每公斤18.9貝克的殘留量,這是海關
            加強查驗日本包裝食品以來,台灣首次發現輻射污染。 衛生署食品藥物管理局食品組副組長
            馮潤蘭:「我們的標準是一個碘300貝克每公斤,銫是370貝克每公斤,所以符合我們的規定
            就沒有所謂的風險上面很大的危害。所以民眾也毋需恐慌。」 量出的殘留單位是每公斤10
            幾貝克,泡麵外包裝如果以100公克來計算的話,也只有1點多貝克,原能會官員說,就算
            不小心沾到手上或吃下肚,也不會對人體造成危害。 原能會幅射防護處副處長 劉文熙:
            「其實它已經是背景的變動範圍的上下左右。你如果對外包裝你有疑慮,你可以稍微拆完
            之後擦一下,或是你手洗、洗洗手絕對可以保障你的安全,所以這部分大家的確不用過度
            憂心。」 衛生署表示,外包裝驗出微量幅射物質,至於內容物烏龍麵本身沒有問題,相關
            單位會加強查驗,如果民眾還是擔心,烹煮前可以用清水沖洗一下,就能有效降低污染。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1301328000
    assert parsed_news.reporter == '陳進交,張明筑,台灣臺北'
    assert parsed_news.title == '日輸臺烏龍麵 外包裝發現核污染'
    assert parsed_news.url_pattern == '2011-03-29-511547'
