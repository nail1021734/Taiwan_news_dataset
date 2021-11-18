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
    url = r'https://star.ettoday.net/news/2085854'
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
            台灣啤酒英熊職業籃球隊日前宣布球隊總經理職務將由前台啤球員「哈孝遠」出任,2012年
            哈孝遠宣佈引退並,將事業重心轉移到演藝圈,但因為脫離運動員的身分,在「年久失修」的
            狀況下,體重一度失守,最顛峰的時候飆到157公斤!這次宣布回歸籃球圈之前,哈孝遠特別
            「打理門面」45天內狂甩12公斤,神清氣爽的接下這次的新職位。 退役運動員體重
            失守 狂飆157公斤 哈孝遠表示,2012轉換跑道進入演藝圈,因為疏於練習,加上自己的
            易胖體質,體重一度失控、十分驚人,甚至有人看到自己的體型,完全不相信自己是
            前籃球國手,讓他十分沮喪;但哈孝遠熱愛籃球的心始終未滅,這次為了扛起總經理的角色,
            給球隊一個好的形象,真的用心的減重了12公斤;因為成效太好,還被網友懷疑疑似
            「抽脂」,讓他哭笑不得。
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1632456000
    assert parsed_news.reporter is None
    assert parsed_news.title == '哈孝遠接台啤球隊總經理 為打理門面、狠甩12kg'
    assert parsed_news.url_pattern == '2085854'
