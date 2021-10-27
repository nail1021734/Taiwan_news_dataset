import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201609300395.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            從「每個人的私人司機」到「讓交通運輸工具如流水般可靠,無處不在」標語,Uber號稱
            「共享經濟」,也迫使不少城市改革計程車特許壟斷現況,但學者質疑它其實沒有共享,反而是
            跨國資本主義新服務態樣的經濟,而且Uber汽車服務想終結的可能不只是計程車,還有
            全球汽車經銷商。
            '''
        ),
    )
    assert parsed_news.category == '產經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1475164800
    assert parsed_news.reporter == '蔡素蓉台北'
    assert parsed_news.title == 'Uber 沒共享的跨國資本主義新經濟'
    assert parsed_news.url_pattern == '201609300395'
