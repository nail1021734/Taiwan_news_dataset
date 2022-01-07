import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/21336?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            台北榮民總醫研究指出,憂鬱症族群罹患肢體震顫、肌肉僵直的巴金森氏症的比例,比非
            憂鬱症患者高出3倍。研究人員並建議,高齡族群可將憂鬱症視為進一步檢查神經系統問題
            的警訊。 北榮精神部成人精神科主治醫師楊智傑10月2日於《美國神經學研究院期刊》
            發表的論文,研究透過「全民健康保險研究資料庫」(NHIRD)挑選23,180名成年人,做為
            研究觀察樣本,其中4634名有憂鬱症病史,18544名沒有憂鬱症,持續觀察這些人後來是否
            罹患巴金森氏症。 最長10年的追蹤期間,共有66名(1.42%)憂鬱症患者出現巴金森氏症
            病徵,對照組則有97名(0.52%)出現症狀,調整年齡與性別因素後發現,憂鬱症患者出現
            巴金森氏症症狀的機率,比非憂鬱症患者群體高出3.24倍。 若排除憂鬱症確診後2到5年內
            診斷出巴金森氏症的病例,憂鬱症患者罹患巴金森氏症的機率,仍然比非憂鬱症患者要高,
            且數據分析顯示,年齡、以及較難治療的憂鬱症,都可能增加罹患巴金森氏症的風險。 楊智傑
            表示,過去研究已經確認,憂鬱症與中風、癌症等疾病確有關連,他們的最新研究則揭示,
            憂鬱症還可能提高罹患巴金森氏症的風險。但他也強調:「不是所有的憂鬱問題,都會導致
            巴金森氏症。」 美國巴金森氏症基金會則稱,近六成巴金森氏症患者,會經歷輕微到中度的
            憂鬱症狀,另有研究認為,憂鬱症狀可能與巴金森氏症患者腦部化學物質的變化有關。而同時
            罹患兩種疾病的患者,發病後行動困難的程度與焦慮問題也比較嚴重。
            '''
        ),
    )
    assert parsed_news.category == '風生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1380763860
    assert parsed_news.reporter == '楊芬瑩'
    assert parsed_news.title == '高齡憂鬱 巴金森氏症機率高3倍'
    assert parsed_news.url_pattern == '21336'
