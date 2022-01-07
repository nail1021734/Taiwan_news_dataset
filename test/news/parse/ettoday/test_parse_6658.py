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
    url = r'https://star.ettoday.net/news/6658'
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
            駐堪薩斯辦事處長劉姍姍遭美國FBI逮捕,前外交部長程建人12日表示,美方處理粗糙、不當
            ,不尊重台灣,美方應立刻釋放劉姍姍,「人權沒有週末」,政府也應聘請律師協助劉姍姍
            。 劉姍姍11日清晨因被控「外籍勞工契約詐欺」罪嫌,遭美國聯邦調查局逮捕拘留,外交部
            表達嚴正抗議,要求立即無條件釋放劉姍姍。外交部長楊進添表示,他已致電美國在台協會
            台北辦事處(AIT)處長司徒文表達抗議,並將繼續交涉。劉珊珊目前遭拘留在詹森郡
            (Johnson County)監獄,預計16日出庭應訊。 程建人表示,台灣因與美國無正式外交關係
            ,於1980年簽訂台美特權、免稅暨豁免協定,其中第5條規定雙方派駐外事人員,在執行
            被授權的公務行為時,得享司法豁免。不過,第5條只是原則性規定,沒有清楚界定,也因此造成
            大家對公務行為的解釋不一,爭議就在此。 程建人認為,若劉姍姍虐待幫傭,不僅不應該
            ,也必須處理,但美國的作法不當;雖然台美特權、免稅暨豁免協定只是原則性的規範,有討論
            空間,但也不能忽略雙方簽有這個協定。他說,過去曾發生美國司法單位向駐外人員發傳票
            ,但為避免豁免協定受衝擊,堅持不簽收。 程建人說,問題關鍵在於美國為什麼不事先告知
            ,完全不尊重台灣,既然兩國是友好國家,應該相互尊重,美國的處理方式粗糙,讓人情何以堪
            。他主張,美國應該立即、無條件釋放劉姍姍,不能等到週一上班日再處理
            ,「人權沒有週末」。
            '''
        ),
    )
    assert parsed_news.category == '政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1321097700
    assert parsed_news.reporter is None
    assert parsed_news.title == '劉姍姍案 程建人:美方處理粗糙不當'
    assert parsed_news.url_pattern == '6658'
