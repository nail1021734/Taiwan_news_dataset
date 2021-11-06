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
    url = r'https://star.ettoday.net/news/1200491'
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
            開幕近兩年的CAPTAIN LOBSTER於新光信義A11館點位租約將於8月底到期,而在A11館店結束
            營業前,CAPTAIN LOBSTER將於6月29日起到林口三井Outlet快閃,開幕前首三日再祭出買一
            送一優惠活動,每日限量50份,每人限購乙份。 另外,在7月2日-9月2日快閃期間,林口三井
            Outlet快閃店也將與新光信義A11館同步舉辦史上最強「買一送二」龍蝦堡優惠活動,點加拿
            大龍蝦堡M或L加價$159薯條+龍蝦濃湯套餐就免費送「加拿大龍蝦堡M」和「龍蝦濃湯」各
            乙份(價值500元),每日限量100份,送完為止。還沒吃過「熱加拿大龍蝦堡」美味的朋友,絕
            對不能錯過這次史上最殺最超值的開幕優惠活動。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530086400
    assert parsed_news.reporter == '黃士原'
    assert parsed_news.title == 'CAPTAIN LOBSTER快閃三井Outlet 開幕再祭出買一送一'
    assert parsed_news.url_pattern == '1200491'
