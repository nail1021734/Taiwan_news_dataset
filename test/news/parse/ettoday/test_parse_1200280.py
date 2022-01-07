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
    url = r'https://star.ettoday.net/news/1200280'
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
            當口渴難耐的時候,來一顆冰涼的梨子,消暑氣又解渴,是每年夏天不可或缺的重要角色。
            國泰綜合醫院營養組營養師賴秀怡指出,梨子和其他的水果一樣,含有豐富的維生素群和礦
            物質,在中醫的角度中,是個能止咳化痰的好食材。 一項由南韓多個大學合作研究指出,針
            對長期的空氣汙染中,常吃梨子的人的尿液中所含的致癌物,有降低的現象;另一個小型試驗
            發現,以計程車司機為主角,若有吃梨的習慣,在24小時之內排出致癌物的速度會特別快,減
            少癌症的危險因子發生。 賴秀怡營養師補充,在中醫說法裡,煮過的梨子比直接吃更具營養
            價值,在動物試驗中也發現,攝取煮過的梨子可以從尿中排出較多的1-羥基芘毒素。以下這
            道雪梨銀耳,運用了天然的食材所做出的養生湯品,很適合在夏天食用喔! 雪梨銀耳 材料:
            梨子3個、白木耳1個、枸杞10公克、冰糖40至50公克、水1500CC 步驟: 1.梨去皮去核切塊
            。 2.白木耳泡開撕成小片狀。 3.食材加入電鍋中,外鍋加2杯水燉煮。 4.加入冰糖與枸杞
            再放到瓦斯爐上把糖煮化即可。 營養師有話說..梨子中的黃酮類植化素,能幫助對肺部的調養。
            '''
        ),
    )
    assert parsed_news.category == '健康'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530138420
    assert parsed_news.reporter == '林玫妮'
    assert parsed_news.title == '雪梨銀耳降火補水分!煮過的梨子比直接吃更具營養價值'
    assert parsed_news.url_pattern == '1200280'
