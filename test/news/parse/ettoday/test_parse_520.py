import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/520'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            勞資談判再度破裂,下季NBA封館在即,馬刺明星後衛Tony Parker決定回老家
            法國職業聯賽ASVEL隊打球。不像其他NBA球員趁機打工賺錢,Parker每月僅領約6萬台幣
            ,幾乎免費效力。 Parker與ASVEL達成協議,以每個月1995美元(約6萬1000台幣)的薪水
            加盟。不像湖人隊球星Kobe對義大利球隊開價40天就要300萬美元(約9150萬台幣)
            ,Parker自己也說,「我幾乎免費為ASVEL效力。」 ASVEL是法國籃球聯賽的強隊,曾於
            2002與2009年奪冠,多年來也都打進聯賽最後4強。Parker也發下豪語表示,「如果我能
            打滿整季的話,冠軍就會是我們的。」 事實上,Parker也是ASVEL事務部副總裁,才願意
            低薪加盟。他在2009年時買下ASVEL的20%股份,目前掛名籃球事務部副總裁,外界普遍
            認為,他會在退休後再買入20%的股份,成為正式的球團領導階層。 帕克今年才幫法國取到
            歐錦賽第2名,將能參加明年的倫敦奧運參賽。另外Parker的合約中也註明,一旦NBA新球季
            開打,他就會返回馬刺隊效力。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1317996300
    assert parsed_news.reporter is None
    assert parsed_news.title == '不搭封館撈錢潮 帕克返法打球月薪6萬台幣'
    assert parsed_news.url_pattern == '520'
