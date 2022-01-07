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
    url = r'https://star.ettoday.net/news/2100142'
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
            台灣基進立委陳柏惟罷免案將於10月23日正式投票,民進黨喊出「反惡罷」
            力挺陳柏惟。對此,國民黨青年部副主任詹為元質疑,民進黨真的力挺要肇事逃逸的行為
            ? 詹為元表示,以陳柏惟為首的民進黨們,不斷強調這是場惡質的罷免,並且喊出
            「反惡罷」,但難道跟民進黨立場不一樣就叫惡質?就叫惡霸? 詹為元指出,民進黨
            罷免韓國瑜時,就說罷免制度是民主價值的體現,韓國瑜被罷掉之後就說為台灣的民主
            寫下里程碑,然後現在罷免陳柏惟時,就說千萬不要讓罷免成為民主的倒退。 詹為元說,
            民進黨現在定調叫做惡質罷免,但但很不幸的,包含肇事逃逸、支持娛樂性大麻分階段
            合法化、打賭博性電玩等,這些事情都做過了;更嚴重的是,陳柏惟敢做卻不敢當,肇事逃逸
            說自己馬上投案但其實是被警方循線到案,明明去電子遊藝場卻硬要說自己去打快打旋風
            。 他更抨擊,陳柏惟身為台中市的立委,面對中火問題不聞不問,沒有與台中人站在一起抵抗
            空氣汙染,這樣難道不是愧對台中市民嗎?難道不是愧對中二選區的選民嗎?面對說謊與
            避重就輕,又一再辜負在地選民,我們要做的是「罷免惡質」。
            '''
        ),
    )
    assert parsed_news.category == '政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634099460
    assert parsed_news.reporter == '徐政璿'
    assert parsed_news.title == '綠營喊「反惡霸」護陳柏惟 他質疑:民進黨挺肇事逃逸?'
    assert parsed_news.url_pattern == '2100142'
