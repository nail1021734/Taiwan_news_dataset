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
    url = r'https://star.ettoday.net/news/2000210'
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
            撐不住了!疫情海嘯嚴重衝擊國內觀光飯店業,位在台中逢甲的老字號商旅黎客商旅,
            6月1日在臉書上公告,商旅在5月31日熄燈號,也成為此波疫情下首家公布歇業的旅館。
            消息一出震撼不少消費者,黎客商旅自2001年成立,在逢甲商圈還未蓬勃時就已開業,
            受許多商務客愛戴,住房率居高不下,連許多五星級飯店都嘖嘖稱奇。 黎客商旅在臉書上
            公告,「各位親愛的朋友,非常謝謝您長期以來對於黎客商旅的厚愛,近20年來的陪伴,
            讓我們珍惜彼此,也再次對曾經支持指教的朋友們,致上我們最誠摯的感謝,黎客商旅已於
            5月31日結束營業,尚未入住的訂單,會有專案小組協助處理。」 同業透露,儘管逢甲不斷
            有新旅館出現,但黎客商旅不僅有一般散客入住,更有大批商務客捧場,但這波疫情來得
            又急又猛,好一點的飯店勉強靠商務客撐住,還有1成左右住房率,只要開店就是賠錢,
            「天天都在想何時設下停損點!」 網友們看到黎客公告,也紛紛留言
            「震驚,我入住台中的首選」、「真是讓人難過,去台中的首選」、
            「多年來前往台中唯一入住黎客,是非常溫馨舒適的商旅」
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1622945640
    assert parsed_news.reporter == '游瓊華'
    assert parsed_news.title == '台中傳奇商旅首亮熄燈號 逢甲20年老字號「黎客」結束營業'
    assert parsed_news.url_pattern == '2000210'
