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
    url = r'https://star.ettoday.net/news/1200594'
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
            「香港中環新興景點 大館-是古蹟也是藝術館」 中環是香港最繁榮的金融中
            心,除了大家熟知的蘭芳園、蘭桂坊、太平山山頂纜車、半山手扶梯之外,現在多了「大館
            」這個免費參觀景點。 大館是香港重要的歷史古蹟活化計劃之一,建築群包括三項法定古
            蹟—前中區警署、中央裁判司署和域多利監獄,大館按照文物保育的最高規格,保留歷史建築
            原貌,除了古蹟還有一棟香港賽馬會立方,展出當代藝術,除此之外還有很多相關的藝文活動
            ,是古蹟也是藝術館。 今年5月29日才開放民眾參觀,熱騰騰的景點,建築物很美很殺底片,
            在眾多高樓的中環竟然有這麼一個世外桃源,如果有來中環,不妨把這個點放入行程中,只需
            要上網預約就可以了,暫時逃離快步調的中環市區走進時光隧道一探警署和監獄神秘面紗。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1531054860
    assert parsed_news.reporter == 'J-O'
    assert parsed_news.title == '香港中環新景點「大館」 古蹟藝術並存能窺見監獄原貌'
    assert parsed_news.url_pattern == '1200594'
