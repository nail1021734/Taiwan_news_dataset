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
    url = r'https://www.cna.com.tw/news/aipl/202110200353.aspx'
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
            中經院副院長王健全今天建議,可在房地合一稅上附加「世代正義稅」用於興建社會
            住宅,財政部回應,房地合一2.0版7月才剛上路,盼先拉長時間觀察成效,將持續搜集外界
            意見關注房市發展。 中經院副院長王健全今天出席中經院記者會受訪時表示,房價愈來
            愈高,將導致年輕人失落感更大,甚至不婚不生,外部成本沉重,建議應課「世代
            正義稅」,並將稅金用於興建只租不售的社會住宅。 王健全建議,政府應對持有5戶以上的
            多屋族,檢視資金來源,看看有無超貸、出租的情況,並課徵「世代正義稅」,作法可從房地
            合一稅上附加2至3%的稅。 對此,財政部賦稅署副署長樓美鐘受訪表示,為鼓勵興辦社會
            住宅者或公益出租人,財政部已提供相關租稅減免,包含所得稅及房屋稅都有,對學者
            建議,她認為應先再觀察看看房地合一2.0的實施成效,目前才上路幾個月,效果仍有待
            觀察,畢竟房屋不像一般商品這麼容易買賣,政策影響要拉長來看,會持續注意相關狀況
            並搜集各界意見。 樓美鐘也強調,稅制不是房市唯一的影響因素,也不是萬能的工具,會
            持續觀察其他影響市場的政策因素,思考應如何配套運用租稅工具。
            '''
        ),
    )
    assert parsed_news.category == '產經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634659200
    assert parsed_news.reporter == '吳佳蓉台北'
    assert parsed_news.title == '學者籲課世代正義稅 財政部:先看房地合一2.0成效'
    assert parsed_news.url_pattern == '202110200353'
