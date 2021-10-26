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
    url = r'https://www.ntdtv.com/b5/2011/12/26/a637451.html'
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
            新加坡明年又將出現新地標,「濱海灣花園」預計半年後開放,其中最具話題性的是打造近20
            個人工擎天「大樹」(Super Tree),最高達50公尺,真面目終於曝光。 新加坡地標在
            魚尾獅獨霸多年後,去年濱海灣區出現金沙綜合娛樂城,是觀光客最新熱門拍照景點,但就
            在金沙對面的「濱海灣花園」明年將完工開放;這個占地約100公頃,有東南亞最大室內
            「涼」室、以及高聳的擎天大樹,早已讓許多人想一窺究竟。 新加坡國家公園局安排媒體
            近期前往預覽,記者們坐在公車上遠遠望去時,嘰嘰喳喳的說大樹很高、形狀很特別,還
            拿來與台灣神木相較一番,等到達時,才發現站在樹下,每個人除了脖子要伸長到極點,還要
            努力往後仰才可完整看到大樹。 不過,這些不是真正的樹木,而是人工水泥樹,由於還在
            施工期間,看起來有點怪異;但導覽人員表示再過一段時間,所培植的植物會爬滿這些
            大樹幹,綠意盎然,再搭配上介於25公尺及50公尺等不同高度,相當於9層樓至16層樓高,
            遊客未來登上樹頂時可盡覽新加坡風景。 除了人工擎天大樹外,濱海灣花園中最醒目的
            建築物就是花穹(Flower Dome),這個以鋼鐵及玻璃打造的室內植物園,匯集來自全球
            多洲的植物,為配合生長在不同氣候型態需求,因此設計出這個大型「涼」室,從小型仙人掌
            到龐然大樹都安然在此生長,訴求的是讓人跨越地理限制,在同一地方就可看到各洲不同的
            代表性植物。 濱海灣花園工程總監陳偉杰表示,濱海灣花園除向新加坡人展示世界上不同的
            植物,同時也能把新加坡展示給世界。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324828800
    assert parsed_news.reporter is None
    assert parsed_news.title == '星地標 50公尺高樹曝光'
    assert parsed_news.url_pattern == '2011-12-26-637451'
