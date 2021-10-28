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
    url = r'https://www.epochtimes.com/b5/14/1/1/n4048382.htm'
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
            英國首相卡麥隆(David Cameron)表示,在歷經金融危機後,2014年將是「英國開始成長」
            的1年。 卡麥隆今天在「泰晤士報」(Times)撰文指出,英國政府推動復甦的計畫分為
            5個部分,且將聚焦在削減赤字和所得稅、支持小型企業來創造工作機會、設立福利津貼上限
            和限制移民。他也承諾教育為首要任務。 卡麥隆寫道:「我們的復甦是真的,但也很脆弱,
            未來有更多困難的決定。」這個保守黨黨魁提到前1個由工黨領導的政府政策時表示:「重回
            非理性的經濟狀況將會重創這個國家。」 英國經濟在2012年最後兩季萎縮後,於去年第1
            季恢復成長。去年第3季經濟擴張0.8%。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter is None
    assert parsed_news.title == '英首相:5管齊下推動成長'
    assert parsed_news.url_pattern == '14-1-1-4048382'
