import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2021/06/28/a103153088.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            進入6月以來,印度尼西亞的中共肺炎(COVID-19)疫情持續飆升,日前單日新增確診人數
            已突破2萬,醫護人員的確診和死亡人數也不斷攀升。印尼官方日前證實,僅6月份已有26名
            醫生染疫死亡,其中至少10人完整接種過2劑中國科興疫苗。 據《華爾街日報》報導
            ,印尼醫學協會風險緩解小組負責人阿迪布(Adib Khumaidi)日前披露,今年6月份該國
            至少已有26名醫生因感染中共肺炎而死亡,其中至少10人染疫前完整接種過2劑
            中國科興疫苗,其餘16名染疫死亡醫生的疫苗接種情況仍在核實當中。 阿迪布表示
            ,印尼防疫機構正研究可否讓醫護人員再追加接種1劑非科興疫苗,例如,牛津-阿斯利康疫苗
            (即AZ疫苗)就在研議之中。 據印尼醫學協會發布的消息,印尼從今年1月起開始在國內
            大規模施打中共肺炎疫苗,而醫護人員是優先接種疫苗的群體。該國9成以上的醫護人員
            施打的都是科興疫苗。然而,在過去的5個月時間裏,已有至少20名完全接種過科興疫苗的
            醫師死於中共肺炎。 事實上,中國科興疫苗在巴西、秘魯等國所進行的第三期臨床試驗的
            數據顯示,其防疫保護率都不高,只不過剛剛超過世界衛生組織(WHO )規定的50%的門檻,且
            相關的實驗數據和副作用等資訊,卻嚴重缺乏透明度。雖然該疫苗獲得了WHO 的
            緊急使用授權,但智利、巴西等多個國家大規模接種這款疫苗後,中共肺炎的新增確診人數
            不降反升,令外界質疑其實際保護效力低。 日前,新加坡衛生部官員已公開發出警告稱
            ,根據多國大規模接種科興疫苗後的發展狀況來看,依賴接種科興疫苗恐怕會導致防疫破口
            。 今年以來一直在大規模接種科興疫苗的印尼,其中共肺炎疫情如今持續飆升,單日新增
            確診人數已接連多日超過萬例,而該國的專家近日警告說,該國疫情的最高峰尚未到來,確診
            病例數量還會激增。預計在未來2至3週內,疫情會達到高峰。 據印尼官方週日(27日)通報
            的數據,該國累計確診病例迄今已達211萬5304例,累計染疫死亡人數達5萬7138人。
            外界認為,由於印尼國內的檢測率低,估計實際染疫和死亡的人數比官方通報的數據更高。
            '''
        ),
    )
    assert parsed_news.category == '國際,社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1624809600
    assert parsed_news.reporter == "黎明,梅蘭"
    assert parsed_news.title == '印尼月內26醫生染疫亡 至少10人接種過2劑中國疫苗'
    assert parsed_news.url_pattern == '2021-06-28-103153088'
