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
    url = r'https://www.epochtimes.com/b5/19/5/20/n11268809.htm'
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
            北京當局毀約,導致貿易戰升級。昨天(19日)晚上,川普在福克斯新聞專訪中表示,中方最終
            會同美國達成協議,但任何協議都不能是「50-50」協議,必須更有利於美國。否則,中國
            (中共)將被關稅徹底扼殺。 川普政府在提升中國商品關稅的同時,也加大了在全球範圍內
            圍堵中共科技巨頭華為的力度。日經亞洲評論引述消息說,德國芯片生產商英飛凌
            (Infineon Technologies)也暫停了向華為供貨。 在此之前,路透社引述知情人的消息
            報導,谷歌(Google)已經暫停了與華為的部分業務合作。此外還有英特爾(Intel)、高通
            等美國頂尖科技企業,都暫停了與華為的往來。 對華為來說,每一次打擊都是重錘。不過華為
            今天(5月20日)回應稱,有能力繼續發展和使用安卓(Android)生態,甚至可以使用自家的
            操作系統、上海交大陳海波領導開發的自主知識產權系統「鴻蒙」,以此替代安卓系統。但是
            華為的如意算盤能打得響嗎? 失谷歌支持 華為手機安卓系統停擺 大家知道,一個手機品牌
            是否成功,有個指標很重要,就是「海外出貨量」。近年華為在大力擴展海外市場,多家機構
            分析認為,華為手機在2016年、2017年的出口占比是三成多,現在已經有四成左右,他們還在
            爭取超過五成。 但是失去了谷歌的支持,華為手機的安卓系統不能再更新了,那麼它的Play
            商店、Gmail、谷歌地圖和youtube等等,包括Chrome瀏覽器,都不能再使用了。 市場人士
            分析,這對國內市場沒什麼太大實質影響,因為中共一直在禁止使用這些功能服務。但海外
            市場的用戶量很大,安卓不能更新,將會使海外市場陷入困境。 數據資訊中心CCS Insight
            的副總裁布雷博(Geoff Blaber)認為,華為在歐洲的手機業務將會受到很大的衝擊。「智能
            手機製造商如果要在歐洲等地保持競爭力,那些應用軟件就十分重要。」 華為用「鴻蒙」來
            替代安卓? 不過任正非認為,美國的制裁對華為的影響是「輕微」的。他對日本經濟新聞表示
            ,華為會自主研發芯片,減輕對公司的衝擊。任正非信誓旦旦地表示「華為不會有問題,已經
            為此做好了準備」。 任正非所說的「準備」,可能指的是從2012年開始,在Linux基礎上
            開發自家的操作系統「鴻蒙」。華為消費者業務CEO余承東也曾表示,一旦不能再使用谷歌和
            微軟的操作系統,華為就會啟動B計劃,用「鴻蒙」來替代安卓。 華為也許有這樣的技術,不管
            是偷來的還是自主研發的。但開發一套新操作系統,面對的並不僅僅是技術問題。香港經濟
            日報指出,這裡面有更重要的兩大難點:數據交換和軟件生態。 用過蘋果手機、電腦和安卓
            手機、電腦的朋友常遇到這樣一種情況,一方的文件,另一方往往打不開。要經過轉換文件
            格式才能打開,這就是所說的數據轉換。 也就是說,如果華為用「鴻蒙」替代安卓,那麼可能
            同樣存在這個問題。人們通常使用的文件格式,包括音視頻和其它文件,可能在新系統中打不開
            。如果想打開,必須連接外面的世界才行。 「鴻蒙」想立足 華為需開發大量轉換器支撐 那
            也就意味著「鴻蒙」如果想立足,華為就得開發大量的轉換器來支撐,把安卓的可讀文件進行
            轉換。而現在世界上各種通用的文件格式成千上萬,對華為來說,這是「海量的工作」,也是
            第一道難關。華為有能力去完成這項任務嗎?值得懷疑。 另外軟件生態也是華為「鴻蒙」所
            面臨的一個現實問題。眾所周知,目前的手機市場基本有兩大部分,一是安卓,另一個是IOS。
            安卓系統幾乎占據手機市場的99%,大量的軟件都是圍繞著安卓系統開發的,涵蓋了生活的各個
            層面。 對市場來說,「鴻蒙」是「新生兒」,基本上沒有軟件支持。業內人士表示,沒有軟件
            支持,就算「鴻蒙」再強,充其量也只能算是一部功能機。現在安卓上通用的軟件數不清,華為
            有能力讓軟件開發商再專為「鴻蒙」開發一套新的軟件嗎?香港經濟日報認為,這「屬於
            不可能的任務」。 大家知道,微軟當年想撼動谷歌,也推出了微軟手機,結果以失敗告終。
            而谷歌也曾想打入windows雄霸的小型電腦市場,也花了很多的心思,但現在仍然成不了氣候
            。 開發新系統 成功機會「微乎其微」 這兩個例子說明,想開發一套新系統取代市場的主要
            占據者,成功的機會「微乎其微」。微軟和谷歌尚且如此,華為比他們如何呢?就算是在大陸
            推出「鴻蒙」,又會有多少人支持呢?這些都是問題。 華盛頓智庫戰略與國際研究中心中國
            問題專家甘思德(Scott Kennedy)認為,美國對華為所設的限制「很可能會摧毀這家公司」
            。 財富雜誌也分析認為,美國的措施可能會使華為陷入癱瘓,對它推出5G網絡將是極大的阻礙
            。 不確定川普是否讀過中國兵法,但他的這個舉措,就是現實版的「釜底抽薪」,從根本上
            截斷了華為的生存根基。 失去了谷歌等高科技公司的重要支撐,華為就像是「沙灘上的高樓」
            ,蓋得越高,坍塌得越快。不只是「走出去」的能力被極大削弱,它的死去也是早晚的事。
            '''
        ),
    )
    assert parsed_news.category == '新聞看點'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1558281600
    assert parsed_news.reporter is None
    assert parsed_news.title == '失去谷歌支持 華為將受多大打擊'
    assert parsed_news.url_pattern == '19-5-20-11268809'
