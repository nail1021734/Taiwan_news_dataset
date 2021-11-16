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
    url = r'https://star.ettoday.net/news/2004394'
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
            這是世界大戰發生前1秒的畫面嗎?!奧斯卡高雄林園店這天來了2隻狗狗需要美容,分別是
            哈士奇「Nikuma」和胡麻柴「可樂」,當時寵物美容師宜軒按照慣例將牠們抱到桌上,
            卻沒注意2張桌子靠得很近,後來才發現2隻狗狗正在緩緩接近對方,甚至鼻子貼鼻子開始
            互聞,嚇得她直呼,「你們的社交距離呢?」 畫面中,Nikuma和可樂站在各自的美容桌上,
            伸長脖子慢慢靠近,聞了聞對方的氣味才後退。宜軒接受《ETtoday寵物雲》採訪時表示,
            「我們當時很擔心會不會打架,但是還好2隻狗狗的個性都特別好,沒有打起來,
            後來我想說是不是哈士奇以為那是他們家的柴柴,聞完覺得味道不對就好好讓我們美容了。
            」 宜軒分享,「其實Nikuma是個個性十分溫馴的小女生,不像一般外面看到的二哈那樣活潑,
            洗澡、美容時都很乖;可樂更是隻特別的狗狗,同樣非常乖巧,而且不像一般的柴犬不愛洗澡
            、剪指甲,我們都叫牠天使柴。」即便了解狗狗的個性,宜軒當下還是有點緊張,
            腦海中不斷浮現各種哈士奇跟柴柴吵架的圖片,所幸這2隻狗狗都比較穩定,
            經過幾秒的交流就退回位置,各自乖乖被美容。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1623405240
    assert parsed_news.reporter == '魏筱芸'
    assert parsed_news.title == '哈士奇認錯汪!探頭與柴柴「鼻貼鼻」 美容師驚:社交距離呢?'
    assert parsed_news.url_pattern == '2004394'
