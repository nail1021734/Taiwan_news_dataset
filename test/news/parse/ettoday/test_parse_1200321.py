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
    url = r'https://star.ettoday.net/news/1200321'
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
            隨著天氣越來越熱,飲料的買氣也隨之增加,但含糖飲料喝多了對身體也不好,正妹主播凱莉
            和小孟便在直播節目中教大家製作天然的蜂蜜檸檬水,酸甜好滋味又有益健康! 凱莉介紹的
            「有機轉型期檸檬乾」是用真的檸檬切片製作,香味非常濃厚,如果喜歡酸的朋友真會愛
            不釋手,光是聞味道就很開心,而且果乾也能直接吃,非常地脆,不過通常是用來泡檸檬水。
            小孟也提到,一般直接去買檸檬,保存期限都很短,切了就要趕快用完,但檸檬果乾可以放
            一整年,想泡的時候就丟一片進去,非常方便。 為了讓檸檬水更有風味,凱莉也拿出在地
            的「台灣鮮採龍眼蜜」,晶瑩剔透的蜂蜜沿著湯匙緩緩滑入杯中,畫面非常漂亮,蜜香也和檸
            檬果香融為一體,小孟也說如果有點感冒、喉嚨不舒服時,可以泡個蜂蜜檸檬水,可以緩解一
            下症狀,平常喝飲料的時候如果可以用蜂蜜代替糖,也會比較健康。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530090000
    assert parsed_news.reporter is None
    assert parsed_news.title == '清香檸檬乾 x 在地龍眼蜜 夏日消暑飲料就靠這一味'
    assert parsed_news.url_pattern == '1200321'
