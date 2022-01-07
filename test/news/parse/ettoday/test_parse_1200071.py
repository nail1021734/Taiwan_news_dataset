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
    url = r'https://star.ettoday.net/news/1200071'
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
            大陸近年來經濟起飛,不少企業紛紛祭出高薪搶才,手機大廠華為的招聘資訊近年來引起日本
            當地關注,單是應屆畢業生開出月薪40萬日圓(約新台幣11萬元),相當於一般日企行情的
            2倍,如此高薪也讓當地人大吃一驚,意外打開在日本的知名度。 日本厚生勞動省調查指出,
            2017年日本大學畢業生起薪20.61萬日圓(約新台幣5.7萬元),碩士畢業生起薪則為23.34
            萬日圓(約新台幣6.5萬元)。華為一口氣就開出40萬日圓,讓當地人驚呼,「日本人的工資
            比其他國家還低」。 另從2017年世界平均年收入排行發現,瑞士以超過9.5萬美元
            (約新台幣289萬元)的年薪奪冠,全年平均勞動工時僅1590小時,而日本則排名第18名,
            年薪不到3.8萬美元(約新台幣115萬元),勞動工時高達1713小時,若與瑞士相較,平均
            年收入差距達2.5倍以上。 《日經中文網》專欄作家青樹明子表示,日本以低於其他國家的
            工資,成為世界第3大經濟體,背後最大推手正是當地獨有的「終身雇用制度」。日本大學
            新鮮人一旦被錄取後,在公司待到退休不成問題,就算營運虧損、效率不佳也不太會被解雇,
            工資還會隨著年齡與資歷提升,甚至也不用煩惱退休生活,福利待遇相當充沛。 即使薪資
            較低,不過工作相對穩定有保障,讓工薪族欣然接受,同時他們反而認為,「工資低是因為
            公司沒有太好的收益,必須為公司拼命工作才行」。日本獨特的思考方式很可能是造成工資
            難以提高的重要原因。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530137580
    assert parsed_news.reporter is None
    assert parsed_news.title == '華為赴日搶才!新鮮人月領11萬 日本人驚「差1倍」嘆:工資好低'
    assert parsed_news.url_pattern == '1200071'
