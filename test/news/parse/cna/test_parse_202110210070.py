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
    url = r'https://www.cna.com.tw/news/aipl/202110210070.aspx'
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
            中國官方5月起密集頒布政策,限制加密數位貨幣交易。中國國家發改委今天公布修改
            「產業結構調整指導目錄(2019年本)」草案,將「虛擬貨幣挖礦」納入淘汰類
            「落後生產工藝裝備」中。 據澎湃新聞,實際上,中國國家發展和改革委員會2019年4月8日
            發布的目錄草案中,就曾將「虛擬貨幣挖礦」活動列入淘汰類產業。不過,當年11月6日
            發布的正式版本中,原列入淘汰類產業的「虛擬貨幣挖礦活動」被刪除。 中國國家發改委
            等11部門今年9月24日發布「關於整治虛擬貨幣『挖礦』活動的通知」,當時便預告,將
            虛擬貨幣挖礦活動增補列入「產業結構調整指導目錄(2019年本)」淘汰類。在增補
            列入前,將虛擬貨幣挖礦活動視同淘汰類產業處理,並按照有關規定禁止投資。 中國國家
            發展改革委10月8日發布的「市場准入負面清單(2021年版)」草案,也提到對「產業結構
            調整指導目錄」有關措施的修訂,擬將虛擬貨幣挖礦活動納入淘汰類產業。 中國國務院
            金融穩定發展委員會5月21日提出要嚴打比特幣挖礦和交易行為,防範金融風險。 之後,中國
            人民銀行(央行)7月初也發布風險提示,「鄭重警告」轄內金融機構,不得直接或間接為客戶提供
            虛擬貨幣相關服務。 新疆、雲南、內蒙古、青海、四川等「比特幣礦業大省」今年也先後
            推出禁令,清理關停虛擬貨幣「挖礦」,要求完成重點對象甄別關停、開展發電
            企業自查自糾。 綜合英國廣播公司(BBC)中文網、紐約時報等外媒分析,中國之前
            頒布的規劃已將虛擬貨幣挖礦列為高耗能行業,隨著「碳中和」的推進,關停這些礦機,將
            減輕其他行業節能減排的壓力,同時也加強金融風險控管,以確保經濟保持平穩。 據外電
            報導,受監管措施影響,不少中國挖礦企業決定將設備轉往中亞的哈薩克或美國德州等地
            另起爐灶;也有企業決定拋售設備退出產業,但挖礦機的市價已大不如前。 路透社6月引述
            加密貨幣交易平台OKEx Insights資深編輯詹姆士(Adam James)分析,北京的禁令
            可能終止中國90%的挖礦活動。
            '''
        ),
    )
    assert parsed_news.category == '兩岸'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1634745600
    assert parsed_news.reporter == '台北'
    assert parsed_news.title == '中國修產業結構調整指導目錄 淘汰虛擬貨幣挖礦'
    assert parsed_news.url_pattern == '202110210070'
