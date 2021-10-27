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
    url = r'https://www.ntdtv.com/b5/2011/12/18/a633615.html'
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
            下面請看一週來的其他大事件。 1、美軍降旗結束9年伊戰 星期四,美軍在伊拉克首都巴格
            舉行降旗儀式,宣告美國在伊拉克九年的軍事行動正式結束。美國國防部長帕內塔在儀式上
            表示,隨著美國紀念伊拉克戰爭的結束,一個獨立自主的伊拉克之夢已變成現實。此前,美國
            總統奥巴馬在北卡羅來納州歡迎從伊拉克回國的美軍將士。他在致詞中感謝軍人的犧牲,留下
            一個主權獨立、穩定和自立的伊拉克,一個由伊拉克人民選出的政府”。 2、神韻全球巡迴
            演出首場隆重開幕 美國神韻藝術團2012全球巡迴演出首場,12月16日晚,在美國德州達拉斯
            市最負盛名的劇院–AT&T表演藝術中心溫斯皮爾歌劇院(AT&T Performing Arts Center
            ——Winspear Opera House)隆重開幕。恢宏正統的中國古典舞、氣勢磅礡的現場伴奏、
            壯麗靈動的立體天幕交織成一幅幅栩栩如生的畫面,將中華傳統文化的精髓詮釋得淋漓盡致,
            令觀眾們嘆為觀止。現場氣氛熱烈。舉辦方介紹,2012年度的神韻呈現給觀眾的又是一場
            全新的節目,神韻三個藝術團將同時在包括北美洲、歐洲、大洋洲及亞洲在內的近百個城市
            演出,歷時數月。 3、維基解密揭中共圍堵人又一例證 維基解密(WikiLeaks)網站公布了
            一份美國駐北京大使館2007年1月26日的電文,其中透露,美國電子證券交易機構納斯達克
            (NASDAQ)因對法輪功表達支持態度,其中國區代表潘小夏(Lawrence Pan)在2007年初遭
            中共當局拘捕和審問。當時該機構的亞太地區負責人歐國偉(James Ogilvy-Stuart)緊急
            聯繫美國大使館求助。歐國偉稱,潘小夏為了獲釋,可能對中共當局承諾,不再讓法輪功學員
            參與的納斯達克紐約總部的新聞。 4、“蝙蝠俠”闖禁區 北京當局陷尷尬 以“蝙蝠俠”走紅
            國際的好萊塢明星克里斯汀‧貝爾(Christian Bale),在出席中國的賀歲新片
            《金陵十三釵》首映之餘,驅車8小時前往山東臨沂探訪盲人維權律師陳光誠,遭中共守衛粗暴
            攔截,被迫離開。CNN網站隨後發佈的視頻顯示,貝爾曾被粗暴推搡,並被大量身著制服的
            守衛圍堵。由張藝謀執導的《金陵十三釵》耗資6億人民幣,還特別邀請貝爾出任男一號。
            現在“蝙蝠俠”闖禁區,另張藝謀和北京當局尷尬。 5、中國漁民刺死韓國警長 韓強烈
            抗議 12月12號,韓國仁川海岸警衛隊在攔截非法捕撈的中國漁船時,中方船長使用尖銳利器
            刺中兩名韓國海岸警衛隊成員,其中41歲李姓韓國警長不治身亡;另一名33歲海警受傷。韓國
            外交通商部當日召見中共駐韓大使,向中國提出強烈抗議。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324137600
    assert parsed_news.reporter is None
    assert parsed_news.title == '新闻周刊300期大事件'
    assert parsed_news.url_pattern == '2011-12-18-633615'
