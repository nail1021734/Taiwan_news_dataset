import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/13/8/7/n3935864.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            肯尼亞週三(8月7日)關閉主要國際機場--喬莫‧肯雅塔國際機場
            (Jomo Kenyatta International Airport)。該機場是通往撒哈拉以南的
            非洲地區等主要通道之一。黎明之前,機場發生大火燒燬了國際航班終點區,迫使幾十架航班
            被取消或者改道。 數百名乘客滯留在喬莫‧肯雅塔國際機場
            (Jomo Kenyatta International Airport)外,消防員與大火以及濃煙奮戰,
            據報導,消防員缺乏必要的滅火設備。 大火發生在機場的「抵達和移民」區域,目前沒有傷
            亡報告。據美聯社報導,乘客費捨爾(Barry Fisher)表示,「火勢凶猛,濃煙滾滾,(大火)似
            乎沒有停止。」 大火發生的原因尚不清楚。截獲的情報顯示,中東或非洲可能成為(
            恐怖主義)攻擊西方的目標。內羅畢的安全官員已處於高度戒備狀態。這個週三是1998年美
            國駐內羅畢和達累斯薩拉姆(Dar es Salaam)大使館被轟炸的週年日,那次轟炸造成224人死
            亡。 肯尼亞的反恐行動負責人Boniface Mwaniki告訴《美聯社》,他在等待大火撲滅後對
            現場進行檢查,以做出判斷和決定。 大火發生的潛在原因之一是肯尼亞機場官員和機場免
            稅店業主之間發生一些糾紛。由於租約到期,一些商舖被強行關門。 目擊者表示,消
            防員抵達滅火時間晚了,由於缺乏設備而滅火不力。截至上個月,內羅畢縣消防部門並沒有
            一輛工作消防車。該國《國家日報》報導說,「整個縣沒有一輛公共消防車處於工作狀態,
            這是一種恥辱。」 報紙還批評當地官員預留資金為縣政府的主要官員等人員配置車輛,置
            肯尼亞人民的直接利益而不顧。 肯尼亞的交通及內政部長卡馬烏(Michael Kamau)表示,該
            機場已經「無限期」的關閉。自大火發生以來,沒有航班抵達和起飛。 至當天下午早些時
            候,當局表示,他們已經控制住了大火,但機場繼續關閉。肯尼亞《國家日報》表示,預計週
            三下午本國航班將恢復。 卡馬烏說,「起火地點是機場的非常核心部份,這使得進出
            這個地方很難。」當地的電視畫面顯示,大火摧毀了部份航站,內部燒燬發黑,屋頂部份凹陷
            。卡馬烏說,大火撲滅後,調查將立即啟動。 這個東非地區最繁忙的機場的運行中斷將對肯
            尼亞經濟和整個地區造成重大打擊,並會在世界各地產生連鎖反應。該國向歐洲提供1/3的
            鮮花銷售,每年產生1億美元的外匯營收。機場關閉的時期,也屬於旅遊高峰期。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1375804800
    assert parsed_news.reporter == '徐清風'
    assert parsed_news.title == '肯尼亞國際機場大火 燒毀國際航班終點區'
    assert parsed_news.url_pattern == '13-8-7-3935864'
