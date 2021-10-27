import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/13/a631155.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            第一條連接俄羅斯首都莫斯科到法國首都巴黎的直達火車在週一早晨開通。這條全長3177
            公里的鐵路線是歐洲第二長線路,由俄羅斯鐵路局提供服務。 這列火車時速每小時200公里,
            全程旅行時間38小時,途徑德國,波蘭,白俄羅斯等五個國家。對於想乘火車遊覽歐洲的旅客
            很有吸引力。 旅客娜塔莉亞:「我覺得這趟旅途主要是有意思,因為可以沿途看到很多城市,
            不僅是巴黎,還有柏林啊,法蘭克福啊,華沙啊和其他城市。對於那些想乘火車體驗歐洲的
            有人非常有趣,不僅僅是坐火車,而是一趟遠足旅行。」 車上有酒吧,餐車和像旅館一樣的
            豪華套間。 旅遊業旅客耶夫蓋尼:「我們大多數的客人是乘火車遊覽歐洲,很多從倫敦出發,
            乘火車穿越歐洲一路到達中國。需要轉車,如果有了這趟火車我們就更有優勢了。」 這趟
            火車在新年前的車票已經售罄。俄羅斯鐵路局的官員在開幕式上表示,他們期望著這條線路
            能給俄羅斯和歐洲的鐵路運輸合作帶來成功。 星期一早晨出發的列車預計在週二早晨到
            達柏林,同天傍晚抵達終點站巴黎。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1323705600
    assert parsed_news.reporter == '施萍'
    assert parsed_news.title == '首條從莫斯科直達巴黎鐵路線開通'
    assert parsed_news.url_pattern == '2011-12-13-631155'
