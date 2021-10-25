import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201801190132.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            法國乳製品廠拉克塔利斯(Lactalis)公司生產的嬰兒奶粉預防性下架擴大,食藥署
            今天宣布,台灣共計29個品項需全面下架,目前業者已回收9萬罐。 拉克塔利斯疑因奶粉遭
            沙門氏菌汙染,造成26名孩童生病,去年已下令全球大規模召回。日前又有外電訊息,
            該集團基於最大限度的預防性原則,全面回收所有Craon工廠產品。 衛生福利部食品藥物
            管理署簡任技正鄭維智今天表示,法國Lactalis集團1月15日通知台灣輸入商有關該集團
            基於最大限度的預防性原則,全面回收所有Craon工廠產品。食藥署已在16日要求所有由
            Craon工廠生產並輸入販售的產品,應配合原廠政策停止販售並將產品預防性下架。 鄭維智
            表示,經查有端強、友華、佳格3家業者輸入法國Lactalis集團Craon工廠生產的奶粉產品
            共計29品項,不論生產日期及批號,業者應將產品全數下架。 鄭維智說,食藥署要求業者
            要在17日凌晨0時前完成下架,目前統計業者共回收9萬罐。食藥署也已啟動販售端稽查,
            目前市面上應已無相關產品。若查到業者繼續販售且沒下架,將依法開罰
            新台幣3萬到300萬元。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1516291200
    assert parsed_news.reporter == '陳偉婷台北'
    assert parsed_news.title == '法國問題奶粉再擴大 台灣29品項全下架'
    assert parsed_news.url_pattern == '201801190132'
