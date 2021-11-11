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
    url = r'https://star.ettoday.net/news/5452'
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
            波士頓紅襪今年有許多球員投入自由市場,其中備受關注的除了「微笑老爹」歐提茲
            (David Ortiz)之外,還有救援投手派柏本(Jonathan Papelbon),這兩名球員都被
            剛出爐的Elias Ranking列為A級自由球員,而紅襪也尚未與他們續約,進而成為各隊
            競相爭取的熱門球員。 派柏本在紅襪隊負責扮演終結者的角色,並且是紅襪隊史上最多
            救援成功的選手,在2002年選秀上,第40輪被奧克蘭運動家選中,但是他拒絕加盟簽約
            ,隔年(2003年),派柏本在第4輪就被紅襪挑走,2005年升上大聯盟原本被設定成先發投手
            ,但是因為當時紅襪的救援投手表現不佳,派柏本就在2006年轉型成終結者角色,2009年
            派柏本奪下生涯中的第133次救援成功,成為紅襪隊史上的救援王。 今年是在紅襪大聯盟
            效力的第7個球季,今年繳出4勝1敗,防禦率2.94,雖然今年救援成功次數是生涯最低的31次
            ,但是創造了生涯最多次的87次三振的成績,生涯累積的表現上則繳出,23勝19敗,防禦率
            2.33,219次救援成功與509次三振。 紅襪今年季賽結束後被爆出喝酒、吃速食的醜聞,遲遲
            不與歐提茲、派柏本等自由球員續約,派柏本或許可以在球場上承擔救援工作,但是在紅襪
            內部要誰來救援?自由市場上最搶手的球員都離自己最近何時才續約?這要繼續等紅襪放出
            消息。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1320578520
    assert parsed_news.reporter == "陶本和"
    assert parsed_news.title == '紅襪紛擾不斷 續約救援王派柏本來救援?'
    assert parsed_news.url_pattern == '5452'
