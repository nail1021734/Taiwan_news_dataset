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
    url = r'https://www.ntdtv.com/b5/2011/12/21/a635020.html'
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
            英國媒體報導,一段「狗狗說人話」的影片擊敗「搞笑版皇室婚禮」、「洗腦貓」等影片,
            榮登今年最受英國民眾歡迎的YouTube影片。 「狗狗說人話」影片中,主人跟小狗說他吃了
            冰箱里的培根,狗狗露出難過神情,哀怨地說:「喔!不!你只是開玩笑吧?!」由於配音得恰到
            好處、狗狗舒展優異「演技」,這段影片大獲好評,至今點閱率已飆破7千3百萬。 YouTube
            趨勢部主管阿洛卡(Kevin Allocca)表示,「2011年點閱率排名前10大的影片證明,儘管
            世界各地的人們使用不同語言,但有些東西總是能夠將所有人的目光吸引至計算機或手機
            屏幕前,例如俏皮可愛的嬰兒、才華洋溢的表演者或是充滿趣味的廣告。」 1. Ultimate
             Dog Tease (klaatu42)。 這份名單中,搞笑版皇家婚禮以2千4百萬餘點閱率名列
            第2。第3名的影片,則是一段用配樂惡搞演員查理辛(Charlie Sheen)受訪畫面的
            片段。 2. The T-Mobile Royal Wedding (lifesforsharing)。 3. Songify
             This – Winning – a Song by Charlie Sheen (schmoyoho)。 4. 最無(有)
            腦、最洗(醒)腦、最沒(有)創意、最讓人哭(笑)不得的Nyan Cat [original]
             (saraj00n)。 最受英國人歡迎的YouTube影片5至10名。 5. Michael
             Collings – Britain’s Got Talent 2011 audition。 6. Masterchef
             Synesthesia (Swede Mason)。 7. Diary of a bad man 5
             (HumzaProductions)。 8. Rebecca Black‘Friday’(Brock’s Dub)。 9.
             Talking Twin Babies (jayrandall22011)。 10. asdfmovie4 (TomSka)。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324396800
    assert parsed_news.reporter is None
    assert parsed_news.title == '英國2011年YouTube十大最熱視頻'
    assert parsed_news.url_pattern == '2011-12-21-635020'
