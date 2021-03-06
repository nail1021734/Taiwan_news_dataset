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
    url = r'https://www.epochtimes.com/b5/19/12/19/n11731456.htm'
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
            今天是12月17號,很高興又和大家見面了,歡迎大家繼續關注我們的頻道。 最近這兩天,在
            中共大外宣領域接連發生大事件,而且當事人稱得上是一個比一個大牌,一時間網絡輿情洶湧,
            可以說賺足了公眾的目光。 首先是德國球星厄齊爾涉疆言論事件,小粉紅們在莫雷NBA事件
            後新一波口誅筆伐的高潮還沒結束,台灣網紅波特王和號稱中國第一網紅的papi醬又爆出涉台
            言論事件,而這一次的事件就更嚴重,不但氣勢洶洶討伐所謂台獨的攻勢被化解,沒討到半點
            便宜,反倒惹火燒身,把身後真正坐莊的大老闆牽連曝光,甚至還牽連到了剛被中央級黨媒高調
            表揚的另一個大牌網紅李子柒。感覺就像你本來只是買個漢堡,結果給你端來了套餐。意外
            且驚喜。下面我們就來聊聊這幾個話題。 當前最受關注的事件,無疑要算台灣網紅波特王
            解約事件。這個事件不但牽扯到中華民國總統蔡英文,更牽扯出號稱大陸第一網紅的papi醬,
            而papi醬的背後,居然還挖出了和王立強爆料中共間諜向心之間的關係,稱得上是一波三折,
            讓人大開眼界。 波特王事件其實本身很簡單,台灣網紅波特王本名陳加晉,在海峽兩岸都有
            不少粉絲。上週末,他在Youtube上發表一部與台灣總統蔡英文合拍的影片,裡面不少和
            蔡英文開玩笑的畫面。這部影片上傳之後立即引發不少關注,在臉書上的播放量超過300萬,
            Youtube上也超過100萬。 結果問題出來了,他在片中幾次稱呼蔡英文總統——當然這是很
            正常的事情,他是中華民國公民,稱呼蔡英文不喊總統難道要喊蔡書記嗎?而且他的視頻放在
            Youtube,並沒有往牆內放,但就這麼個不是問題的問題,他在大陸的推廣合作方,一家叫
            papitube的公司,也叫做徐州自由自在網絡科技有限公司,就很強硬要求他立馬刪除視頻,
            說稱呼蔡英文總統是犯了大忌,同時威脅如果不順從就要立即解約。 這種威脅過去對大多數
            港台藝人都有效,周子瑜就是典型。但沒想到的是這次踢到了鐵板,波特王很爽快說那就解約
            吧,這錢不賺也罷。 這個事件很快發酵,一大因素當然是因為,波特王是近年很少見的,敢對
            中共的戰狼式外宣說不的網紅。而更大的原因,是事件牽扯到了大陸的另一個名人,號稱大陸
            第一網紅的papi醬,因為papi醬就是這家papitube公司的創始人之一。於是,一樁不歡而散
            的商業合作,無形中變成了海峽兩岸兩大網紅的價值觀對撞,大陸的粉紅們依舊按照此前屢試
            不爽的套路,到波特王的微博高喊抵制,而海外大批網友也紛紛到papi醬的臉書賬號留言洗版,
            就此引發一場網絡對戰。 事情到這裡還沒有完,因為很快又有台灣媒體挖掘出papitube公司
            的背景,是受控於papi醬大學同學兼合夥人楊銘的公司泰洋川禾,而泰洋川禾背後的金主,是
            光大集團控股的印紀光大文化產業基金。這條線追到這裡,有人可能已經發現了,世界真小。
            什麼意思呢,因為前不久才被曝光的王立強向心間諜案,向心創辦的中國創新投資公司,也是
            受控於這家光大集團。 這可以說是典型的挖出蘿蔔帶出泥,同時也很完美的解釋了,為什麼
            papitube公司對波特王喊幾句總統會那麼敏感而且態度如此強硬,因為它的背後是中共國有
            企業巨頭,而且是帶有情報、統戰、外宣多種功能的半軍工複合體。 在我看來,這個事情的
            真正重點,已經發生變化,它不再是簡單的兩岸關於一個稱呼的口水糾紛,而是涉及到中共
            大外宣的黨文化輸出、滲透和操控問題。 其實總統這個稱呼,從來不是問題所在,馬英九自己
            就說,他和習近平舉行習馬會的時候,習近平直接稱呼總統府,包括《環球時報》這種以叼盤
            為生的媒體,也同樣使用過台灣總統這樣的稱呼,只不過總統兩字打上了引號。 就是說,連黨
            的最高領導人和黨媒,都沒有避諱總統兩個字,為什麼一家企業會如此緊張,甚至比黨媒審查
            還嚴格呢? 有人說這是因為企業恐懼被中共打壓的一種自我保護,我覺得說不通。因為波特王
            這個視頻是發在牆外的,嚴格說對牆內沒有什麼影響,而且官方甚至都沒有注意到這個視頻,是
            papitube這家企業自己主動的,很強勢地去審查打壓波特王的言論,才導致事件發酵。 所以,
            這場風波真正的原因,是有國企背景的大陸公司,在主動承擔把海內外輿論逐步一統江湖的
            過程中,必然爆發的衝突。其實留心一下就會發現,中共近幾年在有意識的,半公開地把輿論
            管控從國內向海外延伸。尤其港台等華語地區是重災區。各種版本的周子瑜事件已經不知上演
            過多少次。 習近平和黨媒稱呼總統,和執行統戰操控職能企業,對港台藝人自媒體人進行言論
            審查,其實並不矛盾。這是一枚硬幣的兩面,高層稱呼總統是為了安撫和欺詐,而職能企業審查
            總統稱呼是為了脅迫和操控,二者的目的一致,都是為了引導、掌控輿論,服從黨的需要。 相似
            的情況還出現在厄齊爾事件中。 厄齊爾事件大家可能都比較了解了,就是一個足球明星
            厄齊爾在推特發表了涉及新疆的言論,於是同樣遭到官方和民間的封殺抵制。只不過這次的
            抵制也同樣踢到了鐵板。 厄齊爾事件很容易讓人聯想到拿NBA的莫雷事件來對比,而且正應了
            那句話,沒有對比就沒有傷害。 我們都知道,莫雷當初發帖,只是表達支持港人為自由抗爭,
            並未直接提到中共,厄齊爾不同,不但直接譴責了中共在新疆的暴行,還呼籲國際社會聯合起來
            阻止迫害;莫雷在輿論發酵後很快刪除了帖子,厄齊爾至今仍然保留帖子;火箭隊第一時間發
            聲明和莫雷切割,當家球星哈登出面道歉示好,NBA首次官方聲明也指責莫雷是「不當言論」,
            但所有這些都沒擋住中共居高臨下的報復,大批合作商中止合同,騰訊更是立馬宣布停止直播
            NBA。但這次阿森納俱樂部除了一份「球員言論只代表個人觀點」的聲明,基本就是一副愛
            咋咋地的態度,再沒有任何表示,俱樂部和厄齊爾本人也都沒有任何道歉。 而更反常的是,
            碰了一個軟釘子的中共這次也出奇地低調,足協例行公事地譴責了一下,央視取消轉播阿森納
            的一場比賽,無論官方煽動炒作力度,還是民間網絡熱度,都遠遜僅僅兩個月前的NBA事件。 按
            中共的標準,厄齊爾事件性質遠比莫雷要嚴重,為什麼最終的處理卻出現這麼巨大的反差? 比較
            直接的一個表面原因,是中共吸取了NBA事件的教訓。黨媒在NBA事件中幾乎是無限度地開火,
            嚴重透支了小粉紅的口水資源,結果適得其反,NBA總裁肖華態度轉硬,美國主流輿論開始高調
            反擊,中共才開始體會到什麼是過猶不及。黨媒對NBA撒潑,充其量也就是得罪了美國人,因為
            NBA觀眾基本盤就在美國,國際市場主要就在中國大陸。但足球大不同,足球的國際化程度可以
            說是NBA望塵莫及的。我們只需要看一個數據:全世界職業運動項目排名統計,從2002年起到
            現在,前三名一直是足球、F1、高爾夫沒變過,而NBA甚至沒有進入前十名,還比不上冰球聯盟
            和職業拳擊聯盟。 也即是說,如果中共的大外宣要想對英超複製NBA那種歇斯底里模式,那種
            慣用的株連式抵制模式,因為厄齊爾是土耳其血統,土耳其是第一個公開譴責中共新疆政策的
            歐盟國家,他又是德國球星,現在英超踢球,所以應該把這三國加英超德甲一起抵制。那可能
            意味著在短短的幾天之內,中共將成功為自己樹立數以億計的敵人。 那麼更深層次的原因,
            官方這次的低調背後,恐怕是有更精明的利益算計。什麼意思呢,我們都知道英超2019-2022
            賽季的轉播費總收入達到117億美元,而中國大陸蘇寧買下的該賽季全媒體轉播費也僅僅只有
            7億美元出頭,換言之,只相當於別人一個零頭,這麼點分量,顯然遠遠達不到可以對別人
            頤指氣使的程度,不但傷不了人,還可能把自己的一大產業搞垮了。大外宣對此應該是心知
            肚明。 所以,中共操縱的愛國主義,只是一種精心盤算的愛國主義,或者說是一門愛國生意。
            他們的外宣輿論力度,是要看對象的,也要看經濟效益的。 這兩個例子我們可以看到,中共
            過去幾乎是立竿見影的脅迫操控手段,好像最近開始失效。這並不是偶然現象,而是大外宣
            系統長期透支所謂銳實力輸出,透支其政治紅利的必然結果。正所謂一鼓作氣,再而衰,三而竭
            ,人間很多事情,都是利弊同在,相生相剋的。如果說初期的戰狼式大外宣頻頻得手,是因為
            國際社會尚未適應這種新型的銳實力侵略,那麼現在可以說,這種手段已經走入衰竭期,其負面
            的反作用會表現得越來越多,越來越強烈。 這個重大的轉折,應該和川普引發的破窗效應有
            密切關係。大家可能都知道這個破窗效應,原本是描述犯罪社會學的一個理論,意思是一座建築
            如果窗子被打破了沒及時修理,會導致更多的人打破更多的窗戶,甚至最後占領或搗毀這個建築
            。 其實中共這套極權體制,可以說就是一座高壓封閉的建築,無人敢於衝擊它的時候,看上去
            似乎它固若金湯,堅不可摧。但一旦有人打破了第一塊窗戶,很多受過這個建築主人壓迫的人們
            就會迅速跟進,打破更多的窗戶,直到最後摧毀它。川普,可以說就是打破中共窗戶的第一人,
            而且這個效應已經產生連鎖反應,還在迅速擴大中。 這就是我們看到的,為什麼美國、歐洲
            和以港台為代表的亞太地區,越來越多的人和國家開始對中共大聲說不。在這樣的背景下,中共
            大外宣由硬轉軟,恐怕會成為必然的選擇。 這個趨勢已經出現了,一個代表性的例子,就是
            最近突然被中央級黨媒高調表揚的李子柒。 李子柒的視頻,主要表現的都是農村傳統的一些
            家常菜,以及一些傳統手工藝製作,包括視頻畫面透出幾分傳統的田園生活的韻味。這些都是
            過去的中國社會生活常態,廣義地講,都算是中國傳統文化的一部分,儘管僅僅是比較鄉土,
            比較粗淺的一部分。 也就是說,李子柒的視頻之所以在海內外廣受歡迎,正是因為比較真實地
            表現了中國傳統一部分東西,這恰恰從一個側面,證明了中國傳統文化強大的生命力和內涵的
            魅力。而這部分東西,包括比這更博大精深,更值得追尋繼承的東西,恰恰正是中共建政以來,
            在極力破壞的目標。 很顯然,觀眾愛上的是中國,以及中國文化,並不是愛上中共。黨媒對
            李子柒的利用及拉攏,不過是在蹭中國文化的熱度,原因很簡單,中共自己那套黨文化早就成為
            人人厭惡的殭屍文化。坊間不是流傳一句話嗎,說大外宣花了幾百億,不如一個李子柒,可以說
            一語道盡黨文化的醜陋與可笑。 黨媒對李子柒的捧場表揚,其實和統戰機構對波特王的打壓
            是一回事,都是中共在開始染指操控自媒體網紅的象徵。中共有一種非常頑固的特性,就是要
            對任何有影響力的事物,尤其涉及到輿論方面,有公眾影響力的事物,要達到完全操控。順從的
            ,遲早變成黨的喉舌的白手套,成為黨不同層面針對不同對象的宣傳工具;不順從的,遲早被
            封殺消音,或者上電視認罪,或者被污名化,最後失去影響力。 這其實已經形成新的模式,一種
            變相的摘桃子,割韭菜模式,表面上你是自由自在的自媒體,就像papi醬那個公司名字,但實際
            上已經身不由己,言不由衷,只能逐步按照黨的需要去演繹所謂正能量的劇本。一個自媒體人
            辛苦數年打拚出來的品牌和影響力,被一次投資,或一篇文章,就收編至黨的麾下。為什麼
            總有人說中共是中國的萬惡之源,從這個角度,我想就不難理解了吧。
            '''
        ),
    )
    assert parsed_news.category == '大陸新聞,社會萬象'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576684800
    assert parsed_news.reporter is None
    assert parsed_news.title == '中共戰狼式大外宣頻頻觸礁'
    assert parsed_news.url_pattern == '19-12-19-11731456'
