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
    url = r'https://star.ettoday.net/news/2026279'
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
            唐鳳版疫苗意願登記與預約系統6日上線,先行以離島金馬澎第9類、第10類接種對象試辦,
            至於本島該兩類對象則於13日開放登記,不過,中央流行疫情指揮中心今(8)日宣布提前,即日
            起開放全國第9類、第10類對象登記,目標7月16日開放接種。 近期陸續有美日捐贈與自購
            疫苗抵台,國內取得疫苗已經超過700萬劑,目前接種已經接近290萬人次,疫苗覆蓋率超過
            12%,不過距離蔡英文總統喊出的月底覆蓋率達25%還有一段距離。 指揮中心6日10時開放
            「COVID-19疫苗施打意願登記與預約系統」,首波針對金馬澎離島試辦,開放第9類(18歲
            至64歲,患有高風險疾病、罕見疾病或重大傷病者)及第10類(50-64歲成人)對象進行疫苗
            施打意願登記,7日下午5時收單,總計有162.7萬人完成登錄,當中符合試辦對象的離島身份
            者共5,178人,8日起預約。 原本預計看試辦情況,於13日再開放全國第9類、第10類對象
            登記,不過指揮中心今日晚間宣布,即開放全國第9類及第10類對象意願登記。 發言人莊人祥
            說明,登記從即起到7/12日下午5時止,目標7/16開放兩類對象接種,而在此之前,會希望65
            歲以上長者儘速完成施打,等擴大開放施打之後,65歲以上長者也必須使用該系統進行登記
            預約。 指揮中心提醒,「COVID-19疫苗施打意願登記與預約系統」須先完成意願登記後,才
            能在接到通知後進行預約。系統平臺會按疫苗分配情形參照民眾所登記之意願,通知符合預約
            資格的民眾,收到簡訊通知者即可進行下一步預約接種。 尚未收到簡訊之民眾,會於後續符合
            預約資格後,收到簡訊通知,所有資料皆會完整保存,請民眾放心。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1625747400
    assert parsed_news.reporter == '洪巧藍'
    assert parsed_news.title == '第二波疫苗登記即起開放!全國第9類、第10類對象目標7/16接種'
    assert parsed_news.url_pattern == '2026279'
