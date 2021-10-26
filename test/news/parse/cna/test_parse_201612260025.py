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
    url = r'https://www.cna.com.tw/news/aipl/201612260025.aspx'
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
            美國準總統川普質疑「一中」政策,北京表面上反應克制,未曾指名道姓批評。但北京並未
            忍氣吞聲,近期大打「一中」宣傳戰,招數不斷,一如南海仲裁期間爭取國際認同的手法
            。 川普(Donald Trump)2日與總統蔡英文通電話後接受美媒專訪時說,他完全了解
            「一個中國」政策,但不懂美國為何要被「一中」政策束縛,除非美中在貿易等其他議題上
            「達成協議」(make a deal)。 川普發表這番言論前,才在推特和謝票場合抨擊中國大陸
            在貿易、北韓、南海等議題上的作為。此話一出,外界解讀他想以美國長期奉行的
            「一中」政策,當作和北京在前述議題上討價還價的籌碼。 對北京而言,所謂的「台灣問題」
            涉及核心利益,面對還未上任的川普公開挑戰「一中」原則底線,自然不可輕忽
            。 大陸外交部發言人耿爽12日在記者會表示,「一中」原則若受干擾或破壞,中美關係健康
            穩定發展和兩國重要領域合作就無從談起。大陸外交部長王毅緊接著在瑞士說,若試圖
            破壞「一中」原則,「最終只能是搬起石頭砸自己的腳」。 這些隔空喊話雖未點名川普,卻
            明顯是針對川普而來。 北京以此表明「一中」是無法擺上談判桌交易的「非賣品」後
            ,接下來一連串看似毫不相干的事件,都被大陸摻進「一中」元素。北京開始打起宣傳戰,塑造
            國際社會力挺「一中」原則的氛圍。 首先,法國外長艾侯(Jean-Marc Ayrault)14日
            接受法媒訪問時批評,川普質疑「一中」政策的談話「不太聰明」。大陸官方隨即公布,王毅
            和艾侯通電話時讚賞他對「一中」原則問題表明的立場。 隨後
            ,挪威外交大臣布倫德(Borge Brende)訪問大陸,中挪宣布雙邊關係正常化,結束因
            大陸異議人士劉曉波2010年獲得諾貝爾和平獎而陷入冰點的關係。 據陸方新聞稿,布倫德
            19日在北京會見王毅時提到,挪威政府堅定奉行「一中」政策。大陸國務院總理李克強隨後
            會見布倫德,讚賞挪威「堅持『一個中國』政策、致力於改善和發展對華關係的誠意」
            。 最後便是聖多美普林西比20日宣布與台灣斷交。 有別於甘比亞2013年11月與台灣
            斷交時的低調反應,大陸外交部發言人華春瑩這次立即表示讚賞,歡迎
            聖國「回到『一個中國』原則的正確軌道上來」,還說斷交決定體現聖國對「一中」原則的
            認同。 這些事件都留下北京密集操作「一中」原則的鑿斧痕跡,但大陸涉外官員卻在私底下
            輕描淡寫地說:「What a happy coincidence.(多麼美妙的巧合)」 北京清華大學
            台灣研究院副院長巫永平認為,川普與蔡總統通話,質疑「一中」政策之餘還
            暗示可拿來交易,北京必須對川普有所「提醒」,表明北京「不會讓這事情發生就過去了」
            。 巫永平表示,上述一連串事件,特別是台聖斷交,正好讓北京有機會向世界上所有國家表明
            「『一中』是跟大陸建立正常關係必須要堅守的原則」。 這不禁令人想起,南海仲裁結果
            7月出爐前,大陸涉外部門不斷拉攏其他國家,替北京主張透過雙邊協商解決爭議的立場背書
            。大陸外交部曾宣稱,全球有60多個國家認同北京抵制南海仲裁的立場。 但華爾街日報6月
            報導指出,實際上僅有8國支持北京在南海仲裁問題上立場,而且以小國居多。 南海仲裁裁決
            公布後,北京除拒不承認「九段線」主張遭否定的結果,也持續在國際社會宣傳
            以「雙軌思路」解決南海爭議的思維,力阻美國等域外國家插手。 由此可見
            ,在美國新政府的台海政策明朗前,北京為捍衛「一中」原則,這場「一中」宣傳戰預料仍會
            打下去。但能否達到預期目標,讓川普陣營在「一中」政策立場上有所軟化,就要另當別論了。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1482681600
    assert parsed_news.reporter == '尹俊傑北京'
    assert parsed_news.title == '北京發動一中宣傳戰回擊川普'
    assert parsed_news.url_pattern == '201612260025'
