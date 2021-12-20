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
    url = r'https://star.ettoday.net/news/261'
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
            南韓知名人氣男團體「BigBang」近日負面消息接二連三,繼主唱大聲疑酒駕發生交通事故
            撞死人後,隊長G-Dragon又傳出吸食大麻遭到調查,但經過調查後念他是初犯,並且
            非經常性吸食,又是學生身分,將他以緩起訴處分。 G-Dragon聲稱:「5月赴日舉辦演唱會時
            ,去某夜店從一位看似像粉絲的日本人那得到一根菸,當時吸了之後覺得味道和一般菸不同
            ,有懷疑是大麻,吸了一點後便丟了。」據南韓檢方表示,在七月中對G-Dragon進行毛髮
            檢驗,呈現陽性結果,但吸食量極少,並未達到法律量刑處理的基準,念在是初犯,又考量到
            G-Dragon還在就學,因此給予緩起訴處分。 才發生成員大聲酒駕疑雲,又爆出G-Dragon
            吸食大麻,可說是屋漏偏逢連夜雨,幸好大聲獲判無罪,G-Dragon也得以緩起訴。另外,日本
            方面表示,近日即將發行的GD&TOP日本專輯如常推出,希望能掃去近日的陰霾從新出發。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1317886560
    assert parsed_news.reporter is None
    assert parsed_news.title == 'BigBang隊長樣本檢測陽性 獲緩起訴處分'
    assert parsed_news.url_pattern == '261'
