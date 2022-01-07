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
    url = r'https://www.cna.com.tw/news/aipl/202110190043.aspx'
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
            在美、日職棒都拿過冠軍,合計170勝的 松坂大輔 決定退休,41歲的他所代表
            「松坂世代」畫下句點,但他投球時的霸氣、剛猛速球與令人摸不著頭緒的「魔球」將深為
            球迷懷念。 松坂高中就嶄露頭角,絕佳身體協調性讓他的球速輕鬆就能催破時速150
            公里。 1998年的日本全國高中棒球錦標賽(夏季甲子園)8強賽,他燃燒手臂250球完投
            17局,率隊擊敗勁敵晉級,4強賽後援1局無失分,幫助球隊闖進冠軍賽,接著投出賽史上
            第二場無安打比賽,率隊拿下甲子園冠軍,因此被稱做是「平成怪物」。高中畢業後,松坂
            投身日本職棒選秀,獲3隊第一指名,最終加入西武。進到職棒後,松坂立刻有亮眼表現,菜鳥年
            便繳出16勝5敗、防禦率2.60的成績,拿下太平洋聯盟新人王,開啟以他為名的
            「松坂世代」。 在日職前8年,松坂僅2002年勝投未達兩位數,期間拿過象徵日職投手
            最高榮譽的「澤村賞」、4次三振王、3次勝投王、2次防禦率王,率隊在2004年拿下
            總冠軍「日本一」,在日職極具人氣的他,生涯共6次獲選參加明星賽。 松坂2006年投出
            在日職生涯年,17勝5敗、防禦率2.13,球季結束後獲球團同意,讓他以「入札制度」挑戰
            美國職棒大聯盟MLB。當時吸引紐約的洋基與大都會、芝加哥小熊、波士頓紅襪、洛杉磯
            的道奇與天使等多隊目光,最終紅襪以5111萬美元的競標金拿下交涉權,並以6年5200萬
            美元簽下松坂。 加入紅襪後,松坂首年出賽32場,投204.2局,謎樣的
            子彈球(Gyroball)掀起熱議,也讓他共賞給對手201次三振,繳出15勝12敗、防禦率
            4.40的成績,成為首位在世界大賽拿下勝投的亞洲投手,並在菜鳥年就助紅襪拿下世界大賽
            冠軍;隔年雖只出賽29場,共投167.2局,但成績更上層樓,拿下18勝3敗,
            防禦率2.90。 美國媒體暱稱松坂大輔為「Dice-K」,主要是取大輔的羅馬拼音
            Daisuke,將之改為原意為骰子的Dice,有一擲定乾坤或紅襪將他當成下賭注的大籌碼
            含意;K則是代表他的三振能力。 松坂生涯的分水嶺出現在2009年,當年他因傷掉出
            先發輪值,成績也開始下滑,只出賽12場,戰績4勝6敗,防禦率5.76,往後就因頻繁進出
            傷兵名單而在大聯盟載浮載沉;2010年稍微回穩,出賽25場,戰績9勝6敗,
            防禦率4.69。 但2011年起松坂出賽銳減,2012年更只拿1勝,防禦率高達8.28。球季落幕
            後紅襪中止合約,松坂成為自由球員。隔年松坂改披紐約大都會戰袍,在大都會待了兩季,每季
            戰績都是3勝3敗。 2014年球季結束後,大都會宣布不與松坂續約。總計松坂在大聯盟
            8年,共拿下56勝43敗,防禦率4.45。 松坂接著回到日職加盟軟銀,2015年接受手術整季
            報銷,隔年他只投1局,2017年拒絕球團兼任教練的要求,整季沒有一軍出賽紀錄。 2018年
            加入中日,戰績6勝4敗、防禦率3.74,還獲得日職的東山再起獎肯定;但隔年只出賽2場,戰績
            0勝1敗、防禦率16.88。 去年回到職棒起點西武,但傷勢和年紀讓松坂一直無法在一軍
            出賽,終於在今年7月決定卸下戰袍。他生涯在日職前後共獲得114勝65敗,防禦率
            是3.04。 在美、日職棒合計拿下170勝的松坂,國際賽的表現也十分亮眼,曾率日本拿下
            2004年雅典奧運銅牌,和2006、2009年世界棒球經典賽(WBC)冠軍,並兩度獲選為WBC
            最有價值球員(MVP)。 在松坂飽受傷勢所苦,不得不退休前,和他同世代的杉內俊哉、
            新垣渚、藤川球兒、村田修一、木佐貫洋等名將都已先褪下球衣,「松坂世代」只剩下
            40歲的左投和田毅仍在場上孤軍奮戰。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634572800
    assert parsed_news.reporter == '東京'
    assert parsed_news.title == '松坂大輔美日通算170勝 霸氣平成怪物步下投手丘'
    assert parsed_news.url_pattern == '202110190043'
