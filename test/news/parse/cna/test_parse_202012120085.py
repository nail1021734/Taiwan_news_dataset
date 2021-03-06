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
    url = r'https://www.cna.com.tw/news/aipl/202012120085.aspx'
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
            疫情衝擊全球經濟活動,台灣防疫有成,經濟逆勢成長,表現居亞洲四小龍之首。股市飆漲、
            房市與車市交易熱絡,不僅國內電商,因為疫情無法海外旅行,跨境電商業績銷售也
            創新高。 2019冠狀病毒疾病(COVID-19,武漢肺炎)疫情帶給全球震撼,疫情衝擊下,
            出走20年的台商大批湧入,去國多年的海外菁英在台灣角落現蹤,哈佛、麻省理工學院學子
            回台就學,台灣似乎在荊棘滿布的2020年,找到一片獨有的天空。 在超低利率、資金寬鬆
            情況下,全球大開熱錢派對,今年以來,台灣股匯雙漲成為新常態,除了熱錢滾滾而來,
            台灣防疫成功,出口暢旺,也成為推動匯率走強另一大關鍵;新台幣兌美元匯率從年初30元
            持續走升,10月中旬過後,更直接揮別29元價位,站穩28元,升勢一路不回頭。 2020年
            已近尾聲,COVID-19影響勢必延續到2021年。疫情不僅影響全球生活互動、交通往來
            的習慣及運作,也改變了經濟、消費、工作、教育的模式,遠距及居家工作成為新常態,
            出差旅遊受限也使產油國降低原油生產、航空客運業則面臨減班裁員。 不過,疫情衝擊全球,
            卻絲毫不影響台灣消費動能,經濟部統計顯示,超級市場與零售式量販店今年前10 月營業額年
            增率分別為11.4%、9.2%,增幅刷下歷年同期新高與次高水準,國內消費並未受到疫情衝擊
            而疲軟。 在今年消費趨勢中,線上購物成為疫情下的受惠產業,前10月電子購物及郵購業
            營業額達新台幣1894億元,年成長15.9%,增幅創下10年來同期新高。 經濟部統計處副處長
            黃偉傑分析,今年2至4月,百貨公司營業額受社交距離等防疫措施影響,出現2成以上的
            負成長,但超市與量販受惠於民眾搶購物資,營業額不減反增,再加上疫情解封後,政府推出
            三倍券刺激消費等因素,使超市、量販今年表現特別亮眼。 其中,消費亮點當屬海外網購,
            比以往更盛行,因為疫情讓民眾無法出國大買特買,轉而在線上血拼,黃偉傑預期,年末
            許多電商推出購物節刺激買氣,預估電子購物及郵購業全年營業額有很高的機率可以超越去年,
            創下史上新高。 根據研究機構Accenture Post and Parcel Industry Research
            資料顯示,全球電商銷售額20%來自跨境電商,預估全球跨境電商銷售額成長速度將達到本土
            電商成長速度的2倍。 亞馬遜全球開店台灣總經理陳思芬表示,全球消費正在從線下向線上
            轉移,消費者可能「再也回不到過去了」。調查顯示,68%的消費者在疫情緩解後會繼續在
            線上購買生活必需品,43%的歐美受訪者預期會進行更多線上購物。 陳思芬說,在疫情期間,
            台灣賣家憑藉製造和產業優勢,為全球消費者及企業買家提供大量辦公用品、電腦周邊產品、
            無線配件、電子設備等,滿足因疫情居家隔離消費者所需的遠端辦公、遠端教學、視訊會議等
            產品需求。 此外,隨著疫情帶動零接觸、宅經濟商機,不少台灣賣家在居家生活相關產品的
            供應上也展現強勁成長力道。 阿里巴巴國際站亞太區總經理郭奕麟觀察,對台灣商家來說,
            最受歡迎的買家來源包括美國、印度、菲律賓、加拿大、英國。台灣在優秀的防疫表現下,
            仍緊緊抓住歐美大國的採購趨勢與需求。 從台灣具有優勢的前5大產業來看,今年在阿里巴巴
            國際站上的活躍買家數大幅成長,其中健康保健商品買家數年增116%、汽車零配件買家數年
            增60%;美妝保養、機械、五金工具買家數分別年增36%、21%、13%。郭奕麟說,這代表在
            全球防疫及貿易戰期間,台灣確實是受惠市場,吸納大量的歐美轉移訂單。 郭奕麟認為,
            即使疫苗問世,進入後疫情時代,電商買家的消費行為和採購行為依然不可逆轉,買家會
            更習慣透過線上方式交流與溝通,商家要注意是否已準備好線上工具與相關能力。 除消費
            市場外,資本市場也是熱鬧滾滾。台股今年先冷後熱,年初受到疫情爆發影響,接連引發中國
            大陸封城、工廠停工及供應鏈中斷,衝擊投資人信心,鼠年紅盤日重挫696.97點,創下台股
            史上單日最大跌點;隨後在全球疫情加劇、美股崩跌多次熔斷下,台股跌落萬點關卡、於
            3月19日創下今年最低點8523點。 不過在國安基金宣布授權進場護盤、台灣經濟活動回復、
            政府振興經濟方案、受惠轉單效益、資金流入等多重題材下,台股重現生機,於4月8日
            重回萬點,7月27日突破高懸30年的台股天花板12682點;第4季在開放盤中零股交易,
            輝瑞、Moderna等疫苗問世,以及台積電、聯電等權值股帶領下,本土資金螞蟻搬象推升
            指數頻創新高,一路衝高於12月9日創下台股14427.41點新紀錄。 隨著台股指數攀高,
            台股市值也扶搖直上。依台灣證券交易所統計資料顯示,至12月11日全體上市公司
            市場總值達新台幣43兆4428.26億元,和2019年12月27日封關日市值36兆6969.08億元
            大增6兆7459.18億元。 除了台股熱度不墜外,房市也是驚奇連連,甚至亂象百出。
            在海外資金回流、資金寬鬆與低利環境3大條件,以及台灣疫情控制得宜,民眾恐慌情緒不再、
            購屋意願轉升,房地產市場迎來熱絡買氣,甚至出現半夜排隊、開賣秒殺、掮客
            紅單交易頻繁等情況,引發政府出手降溫,打擊炒房歪風。 觀察房市重要的交易量指標,
            台灣今年9月六都買賣移轉棟數衝高至2.4萬棟,單月交易量下創57個月新高;若與
            去年同期相比,年增率高達36.1%;累計今年前10月買賣移轉棟數已高達26萬棟。 房仲業者
            預期,房貸利率維持歷史低檔,且市場資金充沛,吸引自住、換屋及置產族群入市,全年
            移轉棟數有望衝過2019年的30萬棟,並挑戰2014年32萬棟,今年房市交易熱度將是近6年
            最佳表現。 業者分析,低利環境、資金寬鬆政策有利房市發展,加上台商回流帶動土地、
            建廠需求,促使房市急速升溫,呈現量增價揚格局。不過這次房市漲勢並非全面上揚,台中、
            台南、高雄、桃園等地房價明顯走高,雙北漲勢則較緩。 房地產市場增溫,建商推案意願
            普遍提升。根據住展雜誌統計,北台灣在今年前3季累計推案量已達新台幣9405.75億元,
            較去年同期增加600億元;預估全年推案量在1.24兆元至1.27兆元間,有望創下史上第2大量,
            僅次於2013年表現。 房地產市場的多頭行情也吸引投機性買盤趁勢而起,中南部地區
            「炒紅單」重出江湖。為了抑制炒作風氣,內政部展開稽查紅單,國發會端出健全房地產市場
            方案,央行更在12月7日宣布,祭出睽違10年的選擇性信用管制。 疫情同樣影響今年汽車市場
            表現,農曆年後的現場賞車人潮急墜,但因民眾憂心大眾運輸系統的感染風險,反而催出了
            尋求「移動自主」的購車新需求;後續爆發的國旅需求及新車話題,更帶動新車銷售呈現一路
            成長態勢;至11月更在國產休旅車發威及車輛汰換補助政策即將到期下,再催出新一波買氣,
            推升新車掛牌數一舉衝上4.63萬輛,創下歷史上最旺11月新紀錄,也是今年最旺的一個月,
            超越1月及7月傳統旺季表現。 品牌車廠指出,「汽機車汰舊換新貨物稅減免補助」將在
            2021年1月7日到期,因政策延續與否還不明朗,在補助政策可能落日的預期下,消費者趕在
            今年底前購車,各家車廠接單均出現「爆單」,熱銷車款都傳出缺車;包括國瑞汽車、福特、
            裕隆、三陽等均全面加班因應,需求之旺歷年罕見。 觀察全球車市銷售狀況,受到疫情影響,
            市場預估2020年全球汽車銷售年衰退約10%。其中,中國預估衰退5%,美國預估衰退15%;
            台灣車市截至11月底新車總領牌達41萬1930輛,較去年同期逆勢成長4.6%,更是
            全球少見。 業者表示,有別以往因跨年度考量,第4季為新車銷售淡季;今年反而愈到年底
            買氣愈旺,預估全年掛牌量可望輕易跨越45萬輛門檻,改寫15年來銷售紀錄。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1607702400
    assert parsed_news.reporter == '潘姿羽、吳家豪、蔡芃敏、楊舒晴、韓婷婷台北'
    assert parsed_news.title == '台灣錢潮滾滾/台灣經濟驚嘆號 股匯齊飆房車市熱電商亮眼'
    assert parsed_news.url_pattern == '202012120085'
