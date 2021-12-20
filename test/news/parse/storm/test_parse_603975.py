import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/603975?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            兩年之內,中國每七個人,就有兩台監視錄像頭伺候,若扣掉嬰兒和老人,每五人就有
            兩台。你知道嗎? 2017年,中國已經成功完成人類頭部移植,將A的人頭移植到B的身體上,
            你知道嗎? 人類倫理,正受到科技的根本挑戰,而中國已經成為地球上最大的倫理試驗場,
            請看本集。 世界已經意識到,「中共模式」若不制止,將威脅到地球。那麼,什麼是
            「中共模式」?本集提供一個不同的視角:中共模式就是「上面一群拿破崙,
            下面一群義和團」。請看分析。 范疇 Kenneth C. Fan 簡介: 跨界思考者。
            終身創業者。小政府信奉者。平民精神推行者。「無印良國」倡議者。
            '''
        ),
    )
    assert parsed_news.category == '國際,政治,中港澳,國內,影音,歷史,文化,人物,科技'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541533800
    assert parsed_news.reporter == '腦力犯中'
    assert parsed_news.title == '史上最大倫理實驗場?拿破崙+義和團=中共現況?'
    assert parsed_news.url_pattern == '603975'
