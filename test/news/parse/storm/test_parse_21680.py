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
    url = r'https://www.storm.mg/article/21680?mode=whole'
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
            預防乳癌 芳香酶抑制劑效果佳 權威醫學期刊《刺胳針》(Lancet)12日發布最新論文指出,
            乳癌賀爾蒙療法用藥「芳香酶抑制劑」(aromatase inhibitor),對於乳癌高危險群有
            很好的預防效果,能夠降低罹癌機率一半,也能抑制對側乳房腫瘤的生長,建議可做為更年期
            後婦女的預防用藥。 對於乳癌患者與高危險族群──乳癌激素受體(ER)呈陽性的婦女,
            荷爾蒙療法對5成以上婦女有效,常用藥物包括抗動情素「泰莫西芬」(Tamoxifen)、
            「雷諾芬」(Raloxifene)、或芳香酶抑制劑如「安美達錠」(Anastrozole),後者能延長
            病患存活期,副作用較少,也減少子宮內膜癌、靜脈栓塞發生率,但有骨質疏鬆、心血管疾病
            的副作用,兩種藥物常搭配使用。 倫敦大學瑪莉王后學院所進行的「國際乳腺癌干預研究」
            (IBIS-II)第二臨床研究,在2003年2月2日到2012年1月31日間,追蹤18個國家約4000名
            40歲到70歲高乳癌風險婦女,進行隨機雙盲安慰劑對照的臨床實驗。 實驗組(1920人)每天
            服用1毫克Anastrozole持續五年,對照組(1944人)則於相同時間服用安慰劑。5年後,
            實驗組有40名(2%)婦女罹癌;對照組85名(4%)婦女罹癌;7年後,實驗組有罹癌率2.8%;
            對照組罹癌率5.6%;期間實驗組共有18人死亡,對照組17人死亡,研究未說明
            死亡原因。 研究結果證明,Anastrozole可以有效預防停經後的乳癌高危險群,
            降低乳癌發生機率53%。英國等國家會開Tamoxifen、Raloxifene給35歲以上高乳癌風險
            婦女,但預防效果不如Anastrozole,痠痛等副作用更多。 主持這項實驗的
            庫奇克(Jack Cuzick)教授說:「有乳癌家族病史的停經後婦女,有更多預防用藥的選擇,
            衛生機關應考慮將Anastrozole納入高風險族群的預防用藥。」 荷爾蒙因素是乳癌發生的
            重要危險要素。婦女曝露在內因性(體內)、月經周期性動情素及黃體素的時間愈長,罹癌風險
            愈高。因此,初經來得太早、沒有生產、停經太晚都會增加罹患乳癌風險,這是因為
            曝露在內因性動情素及黃體素的時間增長的緣故。相反的,初經來得晚、年輕時懷孕生產,
            則罹癌風險較低。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386903300
    assert parsed_news.reporter == '楊芬瑩'
    assert parsed_news.title == '預防乳癌 芳香酶抑制劑效果佳'
    assert parsed_news.url_pattern == '21680'
