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
    url = r'https://star.ettoday.net/news/1200057'
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
            中央氣象局指出,今(27)日天氣依然穩定,中午之前僅東半部及恆春半島偶有不定時局部雨,
            午後西半部地區也有短暫雷雨;在溫度部分,台北盆地、花東縱谷以及高屏近山區容易出現
            36度以上的高溫,其他地區也都會有33度以上。 氣象主播賴忠瑋表示,受到太平洋高壓影響,
            全台各地都相當的晴朗悶熱,中午前各地氣溫都有機會可以達到33至34度,其中台北盆地甚至
            可以突破36度;在水氣方面,中南部因為局部地區有午後熱對流,而有短暫陣雨,北部午後
            雖然有對流雲系生長,但是雨卻好像下不來,感覺較為悶熱。 明(28)日依然會是炎熱天氣,
            不過周五起至周末將比較容易下午後雷陣雨。賴忠瑋提到,鋒面位置也會略往南移,長江以南
            的降雨機率提高,台灣附近的雲量也會增加,不過還不至於直接受到鋒面影響,只是相對這幾天
            來說,不穩定度提高,較有助於午後熱對流的發展,可以稍減悶熱感。 另外,氣象局表示,
            下周日至下周二,南部地區有局部短暫陣雨或雷雨,其他地區午前大多為多雲到晴,午後仍要
            注意降雨問題;而溫度部分,未來一周高溫大約都落在32至35度,外出時要多注意補充水分。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530066900
    assert parsed_news.reporter is None
    assert parsed_news.title == '今台北飆破36度!未來一周各地炎熱 周五至周末午後易降雷雨'
    assert parsed_news.url_pattern == '1200057'
