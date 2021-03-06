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
    url = r'https://www.epochtimes.com/b5/20/11/5/n12528186.htm'
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
            「中共已經在干預(美國大選)。我們已經看到有些大型中國網路組群——其中一個叫
            Spamouflage Dragon——在YouTube、Facebook和Twitter上無情地攻擊川普總統
            。 「我們知道中共外交部和《環球時報》一直在包括冠狀病毒在內的一些問題上對美國政府
            進行惡意造謠。我們知道中國的假冒帳號(對外國宣傳的問題)。推特在6月刪除了了17.4萬
            個假帳號。這些事不勝枚舉。 「我們需要捍衛我們自己。我們可能反應過度,但我們需要
            開始採取措施,保護美國和我們的社會免受共產黨的攻擊。」章家敦說。 在這次電話連線
            採訪中,我們與中國問題專家章家敦(Gordon Chang)討論了中共在這次COVID-19疫情和
            川普總統感染病毒中的作用,北京如何干預美國大選,以及為什麼禁止所有中共黨員進入美國
            是個好決定。 這是《美國思想領袖》(American Thought Leaders)節目,我是
            楊傑凱(Jan Jekielek)。 楊傑凱:川普總統感染了冠狀病毒,也就是我們《大紀元時報》
            所說的中共病毒。你對這件事情有什麼想法? 章家敦:最終你要去找病毒源頭。我不知道
            這個病的來源:是在實驗室裡製造出來的,還是自然產生的?但我們知道,從2019年12月開始
            ,習近平採取了他知道或應該知道會導致這種疾病傳播到中國境外的措施。所以我相信
            ,中國(中共)造成了川普感染。 現在,人們可以說,美國的反應並不像它應該的那樣迅速
            。這方面會有很多爭論。但我們確實知道,即使中國在否認這種疾病的傳染性之後最終
            承認了,它也試圖淡化這種情況的嚴重性。這導致包括美國在內的國家,沒有採取他們本來會
            採取的預防措施。黛博拉·博克斯醫生(Deborah Birx)在3月31日的新聞發布會上談到
            他們上了中國統計資料的當,福西醫生(Anthony Fauci)也是同樣。因此它就是中共病毒
            ,正如你所言。 楊傑凱:這(個名稱問題)其實本身就是一個有趣的問題。川普總統稱它為
            中國病毒,我們稱它為中共病毒。為什麼你認為叫中共病毒名副其實? 章家敦:這其實是
            一個共產黨(導致)的事件。這是共產黨要負責的事情。我們也許可以說整個中國都要對它
            負責。但很顯然,共產黨需要負責。所以,把它稱為共產黨病毒,或者中共病毒,是準確的
            。 楊傑凱:國務卿蓬佩奧在他的演講和各種討論中,都特別強調要把中共和中國人民分開
            。 章家敦:在蓬佩奧7月23日在尼克松圖書館發表具有里程碑意義的講話中,他談到了和
            中國人民實際接觸。他稱之為親身外交。這一點很重要。我們必須記住,沒有任何東西比
            有人建議各國與中國人民對話、繞過共產黨能讓共產黨更瘋狂。我們需要儘一切努力消除
            中共的合法性,而與中國人民對話是這一舉措的重要內容。 楊傑凱:鑒於我們剛才談到的
            ,可能還有其它領域,你認為中共會干預選舉嗎? 章家敦:中共已經在干預。我們已經看到
            有些大型中國網路組群——其中一個叫Spamouflage Dragon——在YouTube、Facebook和
            Twitter上無情地攻擊川普總統。我們知道中共外交部和《環球時報》一直在包括冠狀病毒
            在內的一些問題上對美國政府進行惡意造謠。我們知道中國的假冒帳號(對外國宣傳的問題)
            。推特在6月刪除了了17.4萬個假帳號。這些事不勝枚舉。 除了試圖直接推翻總統之外
            ,還有報導說中國今年一直試圖在美國煽動暴力。一個自由亞洲電台的報導說,中共解放軍的
            一個情報小組的基地設在現在已經關閉的(中共駐)休斯頓領事館。那裡他們利用大數據來
            識別有可能參加「黑人的命也是命」和「安提法」抗議活動的美國人。然後解放軍給他們
            發了如何製造暴動的視頻。 有很多這種未經證實的報告,數量非常多。5月31日晚上和
            6月1日早上,在白宮北面16街的暴力抗議活動中——也就是聖約翰教堂被縱火的那個晚上——
            有一些中國人在用普通話交談,顯然是在協調行動,並無意中提到了是中共或中國政府召集了
            他們。 這些仍未得到證實,但它們確實和我們從洛杉磯和南加州其它地方參加抗議活動的
            華人那裡看到的報告相一致。所以,對於中共和中國政府在這個春天做了什麼,有很大的調查
            空間。 楊傑凱:你對中共官方喉舌之一《環球時報》總編輯胡錫進關於川普總統感染
            冠狀病毒問題的眾多推文進行了回應。我看了你的推文,我看到胡錫進已經把你回應的很多
            推文都刪除了。這些推文是關於什麼?你回應的是什麼? 章家敦:《環球時報》從技術上講
            是共產黨的媒體,因為它是由《人民日報》控制的。所以它不是中國社會的。 楊傑凱:非常
            正確。謝謝你這麽説,章家敦。 章家敦:《環球時報》所做的是在搞「我早說了」的新聞
            ,做出一種勝利者的姿態、是貶低性的、是冷嘲熱諷。大約一天後,《環球時報》撤下了這些
            推文,因為它明白這對中國沒有任何好處。接下來,我們開始看到中共外交部、然後是習近平
            本人的語氣變得柔和了。但我相信,最初的反應更能說明該黨對這一事件的實際感受。他們
            意識到,這麽搞不大好,所以就把它拿下來了,但這僅僅是策略。 楊傑凱:
            (他們自覺是)勝利者?總而言之,在你看來他們都說了什麼? 章家敦:我眼前沒有具體的
            推文,因為他們確實把它們關掉了。基本上是這樣說的:「我們告訴過你,你們對冠狀病毒的
            應對不力。」就是說共產黨技高一籌,諸如此類的。 楊傑凱:鑒於你剛才說的中共在這件事上
            的罪責,(中共)說這樣的話似乎很離譜。 章家敦:我覺得中共黨媒從來沒把真相當回事
            。 楊傑凱:沒錯。 章家敦:當然還有另外一方面。如果中共能夠理解美國人的情緒,美國
            就真的麻煩了。它是一個罔顧人性關懷的革命組織,是一個不人道的組織。所以很多時候
            ,他們的媒體舉措最後落得個適得其反。 楊傑凱:確實,這個提醒了我。你有一條推特說
            ,「為美國而戰,就像你的生命取決於它,因為確實如此。」這句話可能有很多含義。你想說
            什麼? 章家敦:我是說我們的共和國正處於危險之中。我們不能假設我們必將從中倖免
            。我們必須戰鬥,因為現在我們的敵人想傷害我們。當然,排在首位的是中國(中共)。它是
            敵人不僅僅因為它告訴我們它是我們的敵人,還因為它的強大並且此時此刻它正在採取行動
            顛覆我們的共和國。這對我們來說是一個關鍵時刻。我們有這樣的觀念,我們是美國,我們會
            渡過這個難關。我希望我們能,但我們必須為之奮鬥。所以,這就是我的觀點。 楊傑凱:
            類似的還有最近的這個行政令。我相信它在美國已經實行了一段時間,基本上目的是排除
            共產黨和其他極權主義黨員。無論他們在哪裡,都不能獲得赴美移民簽證。你對這件事有
            什麼看法?關於這個行政令的有效性和性質,有很多不同角度的討論。 章家敦:對共產黨進行
            去合法化沒有錯。我認為,我們應該拒絕中共黨員進入我國,無論是移民還是非移民
            。我認為,我們應該驅逐已經在美國的黨員。我認為,鑒於目前一切狀況,我們有權利監禁
            他們。所以我很高興採取嚴格的措施,我認為我們需要更進一步。 楊傑凱:對某個個人來説
            需要做什麽嗎?有很多人是中共的一員。在你看來,一個曾經是共產黨員或者是共產黨員的人
            ,要想進入美國,需要滿足什麼條件? 章家敦:放棄黨員身分。 楊傑凱:你覺得有些人會不會
            只為了進入美國而放棄黨員身分? 章家敦:是,當然會。簽證官一直在嘗試判斷簽證申請和
            面試時的陳述是否真實。我們當然必須要這麼做。但我認為,不允許現役共產黨員入境應當
            是一個絕對的要求。也許外交官可以除外,他們受到《維也納公約》的保護。但如果美國說
            ,你中共只能派遣不是共產黨員的外交官來,我就更滿意了。我對此沒有異議。但外交官確實
            屬於特殊類別。但其他人,如果你是共產黨員,你就不能進入我國,(因為)你是一個試圖推翻
            美國政府的組織成員。我看不出有什麼理由讓你進入我國。就這麼簡單。我們可能把這些
            事情想得太複雜了。 楊傑凱:就是。 章家敦:我們必須要宣布共產黨不合法。這是一個辦法
            。我不是說我們要拒絕那些有資格來美國的人入境。我可以理解。每個人的情況都不一樣
            。但我想說的是,有一條清晰的界限。有時候你需要用清晰的界限來保護自己。這是我認為
            我們應該採取的一個明確行動。 楊傑凱:有一些此起彼伏的雜音,對你的話唱反調。他們說
            如果我們限制中國人進入美國,就會產生各種各樣的問題。我不打算去列舉這些。你比我更
            了解他們。你對這些人怎麼說? 章家敦:對,當然,沒錯(是會有問題)。任何這樣的禁令都會
            造成美國要付出代價的情況。但是沒有任何無成本的解決方案,尤其在這一點上。我們需要
            捍衛我們自己。我們可能反應過度,但我們需要開始採取措施,保護美國和我們的社會免受
            共產黨的攻擊。也許之後當我們控制住了局面,我們可以考慮放鬆我們所採取的措施。但
            現在我們正處於緊急狀態。所以我認為,在這種情況下,需要採取緊急的解決辦法。 楊傑凱
            :非常好。章家敦,謝謝你抽出時間。
            '''
        ),
    )
    assert parsed_news.category == "美國思想領袖"
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1604505600
    assert parsed_news.reporter == "楊傑凱"
    assert parsed_news.title == '章家敦:美國危險 需擊退中共'
    assert parsed_news.url_pattern == '20-11-5-12528186'
