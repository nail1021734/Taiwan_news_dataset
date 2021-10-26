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
    url = r'https://www.ntdtv.com/b5/2011/04/04/a514182.html'
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
            雅加達時間2011年4月4日凌晨3時06分39秒,6.7級地震震撼印尼首府雅加達。有關部門
            隨後發出海嘯預警,但目前尚無人員傷亡或財產損失的報導。 據美國地質調查局數據,地震
            規模6.7级,震中在北緯位置9.865°,東經107.612°,爪哇島南部區域,震源深度為10
            公里。 美國地質勘探局的記錄顯示,震中離雅加達426公里,離萬隆324公里,離西爪哇打橫
            291公里,以及離澳洲聖誕島224英里。 來自震區的消息說,地震發生后當地許多居民逃出
            戶外躲避。印尼首都雅加達、西爪哇和日惹等地也有較強震感。 美國太平洋海嘯警報中心
            (Pacific TsunamiWarning Center)說,此一地震沒有引發廣泛毀滅性海嘯的危險,但
            可能會有「非常小規模的局部海嘯」。 據點滴網站的報導,把強震修正為7.1級,離
            芝拉扎西南293公里,或北緯10.01°東經107.69°,地震潛伏海嘯可能性,強震也波及到
            中爪哇甚至峇厘島。 印尼地處太平洋地震帶,每年發生數千次地震。2004年12月,印尼亞齊
            地區發生里氏7.9級地震並引發印度洋海嘯,造成20多萬人死亡,50多萬人無家可歸。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1301846400
    assert parsed_news.reporter is None
    assert parsed_news.title == '印尼发生强震 首都雅加达有震感'
    assert parsed_news.url_pattern == '2011-04-04-514182'
