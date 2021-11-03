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
    url = r'https://star.ettoday.net/news/1200501'
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
            台灣星巴克夏季聯名新品來了,去年聯名L.A.生活潮牌BAN.DO系列商品,繽紛甜美的加州風
            格,當時引爆搶購狂潮。今年業者再度推出11款合作單品,預計7月3日(二)上市,以夏日花園
            元素設計筆記本、不鏽鋼杯與水果提袋等,展現青春活潑的氣息。 星巴克近年大玩聯名合
            作,今年夏季攜手BAN.DO品牌,主打花園、水果與彩虹三個意象,運用經典淡粉色結合熱帶花
            卉,設計11款限量生活小物,包含:水果不鏽鋼杯、TOGO杯、提袋、多功能包、手拿包、筆記
            本組與便條紙,明亮絢麗的用色搶眼,給人帶來夏日好心情,每款售價450元~1200元。 星巴
            克本次聯名商品5款杯款將於7月3日全台上市,每次結帳每款商品各限購1個。另外,BAN.DO
            提袋水果、BAN.DO多功能包、BAN.DO手拿包、BAN.DO便條紙組、BAN.DO夏日筆記本組、
            BAN.DO筆袋夏日花園等6款聯名商品則於部分門市販賣。
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530088020
    assert parsed_news.reporter == '徐恩樂'
    assert parsed_news.title == '星巴克聯名BAN.DO!熱帶花卉11款單品7/3限量搶購'
    assert parsed_news.url_pattern == '1200501'
