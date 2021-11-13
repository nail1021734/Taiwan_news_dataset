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
    url = r'https://star.ettoday.net/news/1200161'
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
            吃過抹茶甜點不稀奇,你喝過加了抹茶的啤酒嗎?台中就有一間超可愛
            的日式風格小店「石燕」,藏在熱鬧的逢甲商圈裡,除了提供鹹食之外,還有賣各種抹茶甜點
            及飲品,絕對會讓抹茶控們失心瘋,小象愛出門就在《旅遊超爽的!》社團中帶領大家去品嚐
            超豐富的抹茶甜點,各位男朋友們請趕快筆記,帶家裡的吃貨去! 石燕共分為兩層樓,店面裝
            潢十分簡單,沒有太多華麗的裝飾,以舒適極簡的日式風格打造而成,石燕主要以抹茶甜點為
            主,主打「日式京都抹茶乳酪鬆餅」,食材全從日本進口,整片鬆餅以京都抹茶製作,口感扎
            實又Q,小象愛出門表示:「吃鬆餅可以搭配附上的抹茶醬以及蜜紅豆,超好吃呢!」而且鬆餅
            不會越吃越膩,還可以吃到一點微微的抹茶苦味,口味非常多層次。 炎炎夏天,當然要喝啤
            酒才過癮啊!石燕近期推出「京都玄米入抹茶茶啤酒」,將現泡的抹茶加入來自北海道的啤
            酒,最下面還有一層桂花蜜,攪拌均勻後,會先感受到啤酒的氣泡衝上來,之後甜甜的花蜜以
            及微微苦澀的抹茶會在嘴裡蔓延,三種不同的滋味碰在一起,絕對讓你的味蕾驚豔! 除了甜點
            之外,石燕也有提供許多擁有日本風味的鹹食,像是馬鈴薯燉牛肉或是豬肉咖哩等等。石燕的
            老闆曾經在京都生活4、5年,回國後因為太想念日本家常料理的味道,於是開始研發餐點,
            希望能把道地的美味帶回台灣分享給大家,其中以「石燕家傳鮮菇嫩雞精緻套餐」最為特別,
            可以吃到軟嫩又入味的雞肉以及滿滿的香菇,非常養生。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530424860
    assert parsed_news.reporter is None
    assert parsed_news.title == '抹茶控會失心瘋!台中日式甜點店有超酷「抹茶啤酒」'
    assert parsed_news.url_pattern == '1200161'
