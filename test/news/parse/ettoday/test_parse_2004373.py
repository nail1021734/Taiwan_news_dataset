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
    url = r'https://star.ettoday.net/news/2004373'
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
            新冠病毒在紙幣、手機螢幕和無銹鋼等材質上,殘留時間能夠長達28天,因此讓消毒業
            生意大增,不過有員工抱怨,最近常出入確診者家中,身處高染疫風險,身分卻列為一般民眾,
            無法先獲得打疫苗的資格,讓原PO怕爆直呼,「真正最危險的是我們耶!」 一名男網友在
            臉書《爆怨2公社》表示,本身從事消毒業,自從疫情大爆發後,電話跟案件接到手軟,
            「從安全性低的預防性殺菌,到危險性極高的確診者住家我們都要去」,明明身處染疫高
            風險區,卻不能列為打優先疫苗的名單,讓原PO相當氣憤。 原PO更痛批,「真正最危險的是
            我們耶」,我們要去的環境是曾經有病毒的地方,結果我們分類卻被分到跟一般民眾一樣,
            「政府只會做戲給民眾看嗎,在室外噴有比我們在室內噴危險嗎,只是想好好打個疫苗安個心
            ,繼續努力把疫情降下來卻換來不平等的待遇。」 抱怨文曝光後,底下網友也搖頭回應,
            「因為沒疫苗,結案」、「放心啦!我一天要接觸沒戴口罩且近距離的客人也有外籍,我也是
            排的很後面,習慣就好了」、「是政府發包嗎?還是私人的?」「自求多福了」、「很快就有
            國產疫苗了」。 事後,原PO在留言串補充後續,表示打給1922詢問後,得到「你們的屬於
            一般民眾,一樣的類別」,讓原PO再度崩潰。 繼莫德納正式開打後,日本捐贈的124萬劑
            AZ疫苗,分配狀況也備受關切。副指揮官陳宗彥表示,有特別提醒各縣市政府,一定要依照
            指揮中心訂定的類別順序施打,其中1到6類人數約267萬,因此這次疫苗124萬劑全部施打
            完畢,也還無法滿足,點有請各縣市政府特別注意,規劃上要審慎處理。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1623386280
    assert parsed_news.reporter is None
    assert parsed_news.title == '消毒噴到手軟「狂去確診家中」 他打1922心涼了:危險的是我們'
    assert parsed_news.url_pattern == '2004373'
