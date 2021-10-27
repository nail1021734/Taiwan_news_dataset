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
    url = r'https://www.cna.com.tw/news/aipl/202110200224.aspx'
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
            嘉義市34歲兼任男教師與16歲高二女學生17日同車昏迷,兩人先後不治,有檢舉信指兩人
            師生戀。檢方今天解剖發現女學生一氧化碳中毒,藥毒物方面待釐清;家屬質疑女學生
            遭「加工自殺」。 嘉義地檢署主任檢察官兼發言人蔡英俊今天接受中央社記者訪問
            表示,因無法確認女學生是一氧化碳中毒或藥物等因素致死,今天進行解剖;沒有
            致命性外傷,初步判斷是有一氧化碳中毒跡象,但是否為致死原因,須等待藥毒物
            檢驗結果報告出爐,才能進一步釐清。 蔡英俊指出,有採集女學生陰道棉棒與另一名男教師
            血液棉棒,比對有無發生性行為。另外,男教師遭醫師判定腦死,經家屬同意昨天上午撤除
            維生系統,宣告不治。檢警今天進行相驗,初步判斷男教師有一氧化碳中毒跡象,但須待解剖
            釐清死因。 嘉義縣消防局17日下午獲報指東石漁人碼頭大巴士停車場附近有2人不明原因
            倒臥車內,救護車趕抵,34歲男子及16歲少女已被拖出車外,呈現OHCA(到院前心肺功能
            停止)狀態,隨即送醫急救後,少女當天宣告不治,男子恢復生命跡象,但狀況不穩定,在
            加護病房觀察,男子昨天也宣告不治。 女學生就讀的學校表示,這名男教師在學校
            兼課多年,非正式聘任教師,也在一家補習班任教,在校內及補習班都曾經教過這名
            女學生,至於2人關係,或有人檢舉師生戀,校方則不便說明。另外,女學生家屬懷疑死者是被
            男教師「加工自殺」,希望檢警能調查釐清真相。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1634659200
    assert parsed_news.reporter == '黃國芳嘉義市'
    assert parsed_news.title == '嘉義師生同車2死 女學生解剖、家屬質疑遭加工自殺'
    assert parsed_news.url_pattern == '202110200224'
