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
    url = r'https://www.epochtimes.com/b5/19/12/19/n11733577.htm'
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
            2020台灣大選,進入倒數最後三個星期,各方勢力,激烈交鋒。北京威脅,與紅色勢力滲透,
            仍舊是媒體關注的焦點。新唐人《新聞大破解》節目將為讀者解析紛亂的時局。 從港台連動
            來看,有香港央視之稱的TVB電視台,裁員一成,高層異動,「殼王」陳國強與宏達電董事長
            王雪紅,都從TVB撤退,這是否意味著香港媒體與輿論,將徹底由中國共產黨直接控制? 另外,
            美中貿易戰纏鬥多時,日前美中兩國先後宣布第一階段經貿協議達成共識,美方也因此取消12
            月15日原定加稅行動。美中貿易戰是否只是暫時休兵?2020全球大局,在美國經濟持續強勁,
            中國經濟持續下行放緩的格局下,台灣的角色與位置? 再有,中共面對內外交迫的困境,已經是
            走投無路。因此最近有中國問題專家,建議美國國務卿蓬佩奧和他的團隊,應該考慮準備如何
            應對中共垮台和多方勢力投誠問題。如果接下來,強烈要求北京進行結構性改革的全球大局
            大致已經底定,應該為中共垮台做哪些準備?
            '''
        ),
    )
    assert parsed_news.category == '台灣'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576684800
    assert parsed_news.reporter is None
    assert parsed_news.title == '新聞大破解:決戰2020!台灣抗紅關鍵交鋒'
    assert parsed_news.url_pattern == '19-12-19-11733577'
