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
    url = r'https://www.epochtimes.com/b5/19/4/24/n11210656.htm'
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
            美中雙方將在下週繼續談判,試圖解決持續了一年的貿易戰。白宮在昨天(4月23日)發表了一
            份聲明,指出貿易代表萊特希澤(Robert Lighthizer)和財政部長姆欽(Steven Mnuchi
            n)將前往北京,在4月30日與中共副總理劉鶴進行磋商。隨後劉鶴回訪華盛頓,5月8日接著談
            。 稍早前,白宮首席經濟顧問庫德洛(Larry Kudlow)在美國全國記者俱樂部的午宴上表示
            ,美中貿易談判正在取得進展,「比美中貿易歷史上的任何時候都走得更遠、更深入、更廣泛,
            規模也更大」。 不過他強調指出,「我們(美中)還沒有達成協議」。言詞中,體現出的是對
            談判前景的「謹慎樂觀」態度。 談判「龜速」 回到原點? 談判時序排進了5月,德國之聲
            認為談判的前進速度非常緩慢,堪稱「龜速」。那麼雙方的談判還存在著哪些分歧?是什麼
            原因造成「川習會」只能是一拖再拖? 庫德洛表示,美中雙方仍在解決問題,也就是「結構性
            問題、技術轉讓問題」。他還補充說,「外資持股限制無疑至關重要。降低買賣農產品和工業
            大宗商品的壁壘,都在討論範圍之內。」 白宮在聲明中也指出,第10輪的談判將聚焦7個範疇
            的議題,「將涉及包括知識產權、強制技術轉讓、非關稅壁壘、農業、服務業、採購和執行
            在內的貿易問題」。 從庫德洛的說法以及白宮的聲明內容來看,下週的北京談判內容,涵蓋了
            美中貿易紛爭的大部分問題。也就是說,這些項目跟過去的幾次談判內容沒有太大的差異,談判
            似乎回到了「原點」。 庫德洛說「取得進展」沒錯,但沒有一項讓美中雙方都滿意、成功退出
            談判清單。《金融時報》認為,這突顯出了經過幾個月的談判之後,這幾個關鍵問題仍然阻礙著
            雙方達成最終貿易協議。 「懲罰性關稅」如何了? 不過美國之音指出,談判卡在了最後一個
            重大分歧:美方是否同意一次性、全部撤銷對華商品的懲罰性關稅。 大家知道,美方堅持保留
            關稅,至少也是一部分,這也是被中共逼得沒有辦法。早前萊特希澤在眾議院作證時曾說過,
            「關稅是一件鈍器,但美國沒有其它選項」。 中共簽署過很多協議,跟很多國家都有,加入
            世貿組織(WTO)時也簽了入世協議。但簽過之後,中共並沒有遵守,依然我行我素,從來不守
            規矩。這一點,不僅美國有意見,歐盟、日本等很多國家都有意見。所以現在美、日、歐要聯手
            推動世貿改革,就是針對言而無信的中共。 中共輕諾寡信的歷史,讓美國意識到,想讓北京
            老老實實兌現承諾,必須有監督「執行機制」,而且要保留關稅作為懲戒的一部分。 「執行
            機制」如何了? 但是本月早些時候,《華爾街日報》引述姆欽的說法,「預計執行機制將是
            雙向的」。雙方都設立「執行辦公室」,監督協議的執行情況。不過庫德洛的最新講話中並
            沒有提到這一點。 如果「執行機制」是雙向的,那就意味著,北京方面也可以認為美國沒有
            遵守協議,也會對美國進行懲罰,比如加徵關稅。 這與美方早前所說的「執行機制」是不同的
            ,美方要求的是單向「執行機制」。如果美國判定北京沒有履行協議,那麼美方有權對中方採取
            新的關稅措施。但中方不能採取報復行動,也不能訴諸世貿組織。 但是「雙向執行機制」就
            不同了,它存在一種可能——中共可能會惡意報復。假如這次在「雙向執行機制」的前提下簽了
            協議後,中共肯定會舊病復發,那麼美國就會對它懲戒。但是中共極有可能反咬一口,說美國
            也沒有遵守協議,然後報復美國。 因為中共不是一個正常的政黨,它不僅輕諾寡信,而且顛倒
            黑白。用網友的話說,只有你想不到,沒有它做不到。這也正是不少美國商業團體對協議能否
            長久「缺乏信心」的原因。而如果是「雙向執行機制」,更加劇了協議的「脆弱性」。 觸及
            雙方底線 久未達成 「單向」和「雙向」,一字之差,成了美中雙方的膠著點。何時撤銷關稅,
            遲遲談不攏,「川習會」只能一再拖延。 華盛頓智庫布魯金斯學會(Brookings Institu
            tion)桑頓中國研究中心高級研究員杜大偉(David Dollar)對美國之音表示,撤銷關稅之
            所以成為雙方談判的最後一個主要障礙,是因為它涉及到美中雙方的底線,華盛頓和北京幾乎
            都沒有什麼迴旋餘地。 杜大偉指出,如果接受「保留全部關稅」的協議,會讓北京感到「有失
            尊嚴」。中方希望協議達成後,美方要迅速撤銷全部加徵的關稅,一步到位。但美方很明顯希望
            逐步取消關稅,至少保留部分關稅,當北京兌現了承諾再全部取消。他認為雙方可能會採取取消
            部分關稅的「妥協方案」,這「是可以達成的」。
            '''
        ),
    )
    assert parsed_news.category == '新聞看點'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1556035200
    assert parsed_news.reporter is None
    assert parsed_news.title == '川習會一拖再拖 美中談判卡在哪'
    assert parsed_news.url_pattern == '19-4-24-11210656'
