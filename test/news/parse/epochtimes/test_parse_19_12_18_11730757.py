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
    url = r'https://www.epochtimes.com/b5/19/12/18/n11730757.htm'
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
            公元196年對於漢獻帝,對於曹操都是非常重要的一年。這一年,曹操親自到洛陽迎接漢獻帝
            回到許昌,漢朝的首都正式遷到許昌。同樣就在這一年,漢朝更改年號,新的年號叫「建安」
            。 年號是中國古代用來紀年所起的一種名號。漢獻帝一共六個年號,第一個年號叫「永漢」,
            就是漢朝長長久久,永永遠遠的意思,非常有意思,漢朝最後就是終結在漢獻帝手裏,沒有永漢
            。 漢獻帝即位頭七年用了四個年號,而建安這個年號一用就用了二十五年。建安是什麽意思
            啊?建安建安,就是建立安寧,天下太平的意思。漢獻帝這一年只有十六歲,但是前十六年過得
            太慘了,喪父喪母,哥哥被害,然後四處顛沛流離,被人追殺,被人綁架,有的時候吃不好,睡不
            好,住不好。更改新年號為建安就是希望天下太平,咱們以後別折騰了。 大家經常聽到一句話
            「挾天子以令諸侯」,但是很少有人把奉迎天子給曹操帶來了什麽說清楚。那麽奉迎天子到底
            給曹操帶來了什麽機遇和風險呢?
            '''
        ),
    )
    assert parsed_news.category == '文化網,史海鉤沉,中國歷代名人,傳奇人物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576598400
    assert parsed_news.reporter is None
    assert parsed_news.title == '奉迎天子給曹操帶來機遇還是風險?'
    assert parsed_news.url_pattern == '19-12-18-11730757'
