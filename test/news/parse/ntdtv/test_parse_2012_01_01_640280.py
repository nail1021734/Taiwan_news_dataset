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
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640280.html'
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
            東京迪士尼度假區今天起到5日為止,舉行賀新年花車遊行活動,米奇和米妮等吉祥物穿著日本
            和服裝扮,向遊客賀年,吸引許多遊客進場,充滿喜氣。 迪士尼度假區分迪士尼樂園和迪士尼
            海洋,今天上午11點(台北時間10點)開始的賀新年花車遊行,在開始前1、2個小時,就有許多
            民眾在寒風中等待,心情興奮。 活動一開始,在鼓樂手引導下,穿著和服的米奇、米妮與今年
            的東京迪士尼度假世界親善大使,站在日本新年裝飾的花車上,熱情的向兩旁遊客揮手
            致意。 米奇、米妮的好友們搭在另一輛車上,隊伍中還有舞獅的人高喊「新年快樂」。 花車
            遊行活動將從1至5日每天舉辦2次,每次約25分鐘。只有第1次賀年踩街活動,度假區親善
            大使會登場。 今年的親善大使是經營迪士尼的東方樂園公司一位25歲女職員。她是從110位
            應徵者當中雀屏中選,今年將到日本各地與民眾分享迪士尼度假區的夢想。 今天園區可看到
            很多親子、情侶盛裝打扮,還有小女孩穿得跟平時米妮的紅底白點洋裝一樣,為了與吉祥物
            美美地合照,在寒風刺骨當中還脫掉外套。 有些大人布包裝飾著滿滿的吉祥物,尤其是龍年版
            米奇與米妮或和服造型款式。這些遊客說希望明年新年也在此度過。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325347200
    assert parsed_news.reporter is None
    assert parsed_news.title == '東京迪士尼迎新 花車遊行熱鬧'
    assert parsed_news.url_pattern == '2012-01-01-640280'
