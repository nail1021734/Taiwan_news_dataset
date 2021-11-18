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
    url = r'https://star.ettoday.net/news/1200152'
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
            越南因迷信仍有吃貓狗肉的文化,當地動物救援人員Quyen偷偷帶著攝相機,潛入越南胡志明
            市平新郡(Quan Binh Tan)的貓肉市場,揭露貓咪被殘殺的恐怖畫面,影片引起軒然
            大波。 從畫面中可以看到,冰冷的鐵籠裡塞滿了好多隻貓咪,牠們頻頻害怕地對著陌生人
            喊叫。根據《每日郵報》報導指出,貓咪在當地被稱為「小老虎」,吃一次貓肉要價新台幣
            1750元到2300元,而當地人吃貓肉竟是相信可以增加體力、提高性慾、驅除厄運,甚至有人
            認為能因此繼承貓的敏捷性。 救援機構Fight Dog Meat的執行長蜜雪兒伯朗
            (Michele Brown)將這段影片PO上網並表示,「最近狗肉引起了許多人的關注,但貓幾乎
            沒有,這使我感到沮喪。」她還透露,影片中的貓咪最大來源其實是從大陸進口的,不過也有
            許多是從當地偷來的家貓,或是身上帶有細菌的流浪貓,「儘管已經不斷地宣導,但仍有許多
            觀光客來到越南,會想嘗試貓肉。」 越南在1997年發生鼠疫時,政府就鼓勵人民飼養貓隻,
            並且禁止餐館內販賣貓肉,但還是有許多人遊走於法律之外,像是河內市就有數十家餐館販賣
            貓肉。大部分的飼主會把貓咪關在家,擔心寵物會被偷並出售給餐館。另外,不僅僅是貓肉,
            連狗肉都是一些越南人的餐桌「佳餚」。 網友們對於越南食用貓肉的評論兩極,許多人紛紛
            留言說,「貓咪很可愛不應該吃牠們」、「非常殘忍!」、「因為貓有人在飼養,所以大家會
            心疼吧」、「牛豬雞表示:沒人同情我」、「吃貓能變敏捷,那吃魚就可以潛水了?」不過也有
            不少人認為,要尊重各國的當地文化。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530085380
    assert parsed_news.reporter is None
    assert parsed_news.title == '直擊越南「貓肉市場」 當地迷信能提升性慾、變敏捷'
    assert parsed_news.url_pattern == '1200152'
