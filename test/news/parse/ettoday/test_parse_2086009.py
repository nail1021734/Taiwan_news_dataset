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
    url = r'https://star.ettoday.net/news/2086009'
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
            美國製藥廠莫德納(Moderna Inc)執行長班塞爾(Stephane Bancel)表示,隨著疫苗
            產量增加,確保全球供應,COVID-19(2019冠狀病毒疾病)疫情大流行可望在1年內結束
            。 班塞爾告訴新蘇黎世日報(Neue Zuercher Zeitung):「如果你檢視過去6個月來整個
            產業的產能擴張,明年中以前可望有足夠的劑量,如此一來,世上所有人將可以接種疫苗。
            加強劑也可能符合需求的程度。」 班塞爾還說,甚至嬰孩可能很快也有疫苗可以打
            。 「那些還沒接種疫苗的人將會自然免疫,因為Delta變異株感染力高。這樣的話,我們
            將會出現類似流感的情況。你可以接種疫苗,平安度過冬天。或者不接種,冒著生病的風險,
            甚至可能住院。」 在被問到,這是否意味著明年下半年可以恢復到正常生活。他說:「
            我猜想,從今天起,一年吧。」 班塞爾說,他預期政府會批准已接種疫苗者注射加強劑,因為
            去年秋天接種疫苗的有風險患者「無疑」需要再補打。 莫德納加強劑的劑量只有原始疫苗
            劑量的一半,這樣可以有更多的加強劑。 「疫苗的數量是最大的限制因素,而在只要一半的
            劑量下,來年我們將可以供應全球30億劑,而不是只有20億劑。」 由於莫德納來不及進行
            調整,今年加強劑的成份仍然和原始疫苗一樣。 「我們目前正針對優化的Delta變異株進行
            臨床試驗。這將會成為2022年加強劑的基礎。我們也測試了科學家認為最有可能的下一個
            變異株,Delta加上Beta。」 班塞爾說,莫德納可利用現有生產COVID-19疫苗的生產線來
            生產對付新變異株的疫苗。疫苗的價格應該會一樣。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1632403320
    assert parsed_news.reporter is None
    assert parsed_news.title == '莫德納執行長:疫情可望1年內結束'
    assert parsed_news.url_pattern == '2086009'
