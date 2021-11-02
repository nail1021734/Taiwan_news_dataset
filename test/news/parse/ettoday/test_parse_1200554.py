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
    url = r'https://star.ettoday.net/news/1200554'
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
            位於新北市永和區有家人氣排隊店家,店名就叫做「北蘭阿姨商行」,懂的人總是會
            在心底笑笑,餐點很簡單,招牌主食就是嘎拋豬肉飯、蒜味香腸飯、嘎拋炒泡麵,雖然創業的
            三個年輕人沒有餐飲背景,但因為愛吃而研發出的嘎拋豬肉飯卻很受歡迎。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530100800
    assert parsed_news.reporter == '黃士原'
    assert parsed_news.title == '店名「北蘭阿姨」有點惡搞 招牌嘎拋豬肉飯的半熟蛋卻很邪惡'
    assert parsed_news.url_pattern == '1200554'
