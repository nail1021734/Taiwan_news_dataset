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
    url = r'https://star.ettoday.net/news/2031723'
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
            養狗之後完全沒有隱私!網友Cheryl Tsui日前在發文表示,「養狗之後私人空間是什麼
            ?請問媽麻可以自己上個廁所嘛?」照片中可見,哈士奇和拉布拉多靜靜趴在廁所前,
            一臉憂愁地盯著門前看,似乎已經做好等待奴才「蹲馬桶」的準備,讓人看了瞬間壓力爆棚,
            畫面笑噴千名網友。 「本周我最毛」在周末提供毛毛小品短文,分享寵物、動物日常,
            帶您一秒瀏覽毛孩那些事,不管有沒有養寵物,都期盼能為大家在假日小充電,轉換成上班日
            的大能量。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1626431700
    assert parsed_news.reporter == '呂欣潞'
    assert parsed_news.title == '媽媽要蹲馬桶! 汪姐弟相揪塞廁所前「準備等門」'
    assert parsed_news.url_pattern == '2031723'
