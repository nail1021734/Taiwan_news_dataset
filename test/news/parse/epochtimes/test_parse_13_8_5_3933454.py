import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/13/8/5/n3933454.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            自法國政府禁售幾款德國奔馳車以來,造成七月奔馳在法國業績下降了6.8%,禁令讓法國經
            銷商不得不面臨裁員困境,而德國奔馳製造商戴姆勒集團則表示將繼續上訴,希望獲得解禁
            。 今年6月19日法國政府指出,德國奔馳A型、B型、CLA型和SL型汽車因排放氣體超標,發出
            銷售禁令。自此德國奔馳製造商——戴姆勒集團(le groupe Daimler)和法國政府間的戰爭不
            斷,為此兩家訴諸司法程序,法國凡爾賽行政法庭7月25日做出決定,暫停該禁令的執行,但法
            國環境部長馬丁(Philippe Martin)隨後則聲明,政府的禁令依然有效。 禁令導致奔馳客戶
            流失從而裁員 自有禁令以來,奔馳在法國的車行面臨的實際情況是:日前有近5000名客戶等
            待新車發貨。此前為了增長業績,奔馳經銷商已採取了各種促銷方式,包括折扣、3年內向客
            戶提供全方位維護服務,出借1200輛奔馳車等,如果政府禁令繼續保持,車行無法向客戶銷售
            汽車,已經準備好購車的客戶將不會一直等待下去,而會選擇競爭對手寶馬(BMW)和奧迪
            (AUDI)的產品,這對奔馳客戶群將會產生重大影響。 業內人士分析,如果禁令繼續保持的話,奔
            馳在法國的經銷商——各大車行將不得不面臨裁員局面,這將涉及1600名在法職員,占奔馳法
            國各大車行總人員的10%到15%。 奔馳反禁令 變相保護法國品牌 被禁的奔馳幾款汽車占法
            國奔馳車行總銷售量的一半以上,奔馳法國地區經銷經理貝爾納(Jean-Claude Bernard)表
            示,某些車行由此受到巨大影響,訂單下降一半,銷售額減少60%,全法20%的奔馳經銷商將受
            到影響。 戴姆勒集團表示,奔馳汽車被禁事宜,目前僅發生在法國,他認為這是法國在變相
            保護法國汽車品牌,並指出在禁令實施之前,奔馳在法國的銷售額增長率達到6%。 據法國《
            回聲報》報導,面對法國環境部長的態度,德國戴姆勒集團將不氣餒,準備向法國最高行政法
            庭——國家委員會上訴獲得解禁,理由是目前在法國本土,被禁的幾款奔馳汽車並沒有因為質
            量造成安全隱患或對環境造成影響,還希望法國政府對禁令造成的損失能做出賠償。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1375632000
    assert parsed_news.reporter == '鄧蘊詞法國,德龍'
    assert parsed_news.title == '幾款奔馳車被禁售 法國經銷商面臨裁員'
    assert parsed_news.url_pattern == '13-8-5-3933454'
