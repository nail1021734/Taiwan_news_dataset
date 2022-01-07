import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/14/1/1/n4048455.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            最新消息,捷克警方發言人說,巴勒斯坦駐捷克大使因公寓發生爆炸受重傷,已不治身亡。
            布拉格警方女發言人Andrea Zoulová證實的此消息。今天中午,捷克首都布拉格,巴勒斯坦
            駐捷克大使的公寓發生爆炸,大使賈馬爾(Džamál Muhammad Džamál)於自家公寓被炸傷
            後送往醫院急救。 《捷克新聞》(NOVINKY.cz)1月1日報導,今天(週三)中午巴勒斯坦
            駐布捷克大使賈馬爾(Džamál Muhammad Džamál)在Suchdol(捷克)的住宅公寓發生
            爆炸,當時大使身受重傷。 據知情人士調查,沒有跡象表明這是一起恐怖行為。這可能是粗心
            操作危險的煙火或爆炸物所致。巴勒斯坦駐布拉格大使館新聞辦公室的代表
            Nabil El Fahel確認,巴勒斯坦大使受了重傷,家庭成員安全無事。這位大使已被送往中央
            軍事醫院,並處在人工睡眠狀態。 警方發言人Andrea Zoulová說:「週三中午在
            Internacionální街確實發生了爆炸。」據她介紹,這不是勒斯坦大使館的所在地,是
            巴勒斯坦大使的公寓。在現場的鄰居說,大使的家庭剛剛搬進公寓,到處都是箱子和包裹的
            傢俱。 布拉格救援隊發言人Jiřina Ernestová告訴《捷通社》(ČTK)記者,炸傷一人,
            還有一個女人吸入煙霧,也已被送到Motol醫院。她說,「目前我們必須等待」,警方還沒有
            做更多的詳細說明。 這個地方交通很便利,除了警察,消防隊員,醫護人員之外,警察總部的
            直升機也飛到了。 巴勒斯坦大使賈馬爾(Džamál Muhammad Džamál)已不治身亡的消息,
            是捷克警方發言人Andrea Zoulová證實的。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter == '李天韻,田佳貴'
    assert parsed_news.title == '巴勒斯坦駐捷克大使在公寓被炸身亡'
    assert parsed_news.url_pattern == '14-1-1-4048455'
