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
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640292.html'
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
            英國倫敦以優越的地理位置和獨特的地標建築,每年的跨年焰火表演一向是別具一格獨領
            風騷;而芬蘭首都赫爾辛基則在新年展現了2012年「世界設計之都」的稱號;南半球的巴西
            裏約熱內盧上演了2百萬人狂歡迎新年的盛大場面,百聞不如一見,現在就讓記者們帶大家到
            現場看看。 泰晤士河畔焰火輝煌喜迎奧運年 今年的倫敦泰晤士河畔新年焰火表演不止是
            為了辭舊迎新,也是為了迎接2012倫敦奧運會,還有女王登基60週年。 當新年鐘聲敲響
            的時刻,絢麗奪目的焰火從135米高的倫敦眼四周以及泰晤士河面上射出,伴隨著靈動跳躍
            的音符,整個天空變成了五彩繽紛的動態畫卷。 「2012世界設計之都」迎新年 芬蘭首都
            赫爾辛基迎來了作為「世界設計之都」的2012年。 除了著名藝人到場表演,赫爾辛基市
            政府還為現場的數萬觀眾上演了芬蘭史上最大規模的3D投影表演,芬蘭地標建築「赫爾辛基
            大教堂」霎時變得鮮活起來。 隨著新年倒計時的歡呼聲,教堂廣場上騰起了一簇簇
            煙花,人們互祝「新年快樂」,迎接新年的到來。 加拿大卡爾加里市的上萬民眾聚集在
            市中心的奧林匹克廣場,等待新年的到來, 伴隨著觀眾們的吶喊,當電子時鐘歸零的
            時候,全場歡呼,大型煙火表演開始,慶祝2012年的到來。 巴西裏約熱內盧2百萬人狂歡迎
            新年 在狂歡之都巴西里約熱內盧,大約200萬人共同歡慶2012年元旦的到來。從十多只木筏
            上燃放了24噸煙花,照亮了旅遊勝地科帕卡巴納海灘的上空,上百萬人在這裡觀賞世界上最
            大規模的煙花之一,現場載歌載舞,熱鬧非凡。
            '''
        ),
    )
    assert parsed_news.category == '法輪功,各界恭賀李洪志先生新年好'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1325347200
    assert parsed_news.reporter == '王晨光,榮舒,冠齊'
    assert parsed_news.title == '西半球創意狂歡派對 燦爛迎新年'
    assert parsed_news.url_pattern == '2012-01-01-640292'
