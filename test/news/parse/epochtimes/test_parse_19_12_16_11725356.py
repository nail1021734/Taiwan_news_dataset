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
    url = r'https://www.epochtimes.com/b5/19/12/16/n11725356.htm'
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
            有俗話說「吃過冬至湯圓長一歲」,然而,現在一般認為吃過年夜飯等於過了年才長一歲,
            為什麼有這個出入呢?「吃過冬至湯圓長一歲」只是沒有根據的傳說嗎?其實關鍵就在於對「
            過年」的認定,歷史上有過改易。 冬至與新年的關係 「冬至」,漢代之前另有稱呼叫「歲初
            」,表示一歲之初的意思,也就是一年的開始,這也是俗話說「吃過冬至湯圓長一歲」的道理
            所在。從周到秦代,把「冬至」當作新年,冬至所在的月份是子月,就是正月。那時代過了冬至
            夜就是過了年了,冬至日就是新年。民俗傳下來「冬至大如年」的說法,其實是反映了這個
            歷史文化。 三千年前的周代曆法,以冬至落在的月份作為「建子之月」——一年的第一個月份
            ,冬至為正月元旦。為何這樣建制呢?周代大司徒設計製作了土圭儀,以「土圭法」測得一年中
            日影最長的日子在冬至日,最短是在夏至日。日影最長的冬至日就是太陽離中國最遠的一日,
            此後,太陽將逐漸北返,陰氣漸弱、陽氣漸漸增長,周代就將冬至日作為新年的開始。這也反映
            了天地陰陽循環「一元復始」開始於冬至的現象。 後來,到了漢武帝太初元年(西元前104年)
            , 改訂曆法,頒行太初曆,以寅月為正月,就是以立春節氣所在的月份作為一年的開始。從此
            新年和冬至分了家,冬至遂成為冬至節,也叫「冬節」或「亞歲」。 歷朝歷代的新年元旦有過
            幾次的變動,然而,冬至日始終是天地間陰陽循環「一元復始」的起點。吃了今年的冬至湯圓,
            可知生命的成熟度又增了一分了!你對自己有何新的期待呢?
            '''
        ),
    )
    assert parsed_news.category == '文化網,文化百科,文化博覽,文化漫談'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576425600
    assert parsed_news.reporter is None
    assert parsed_news.title == '為什麼說「吃過冬至湯圓長一歲」?'
    assert parsed_news.url_pattern == '19-12-16-11725356'
