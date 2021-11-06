import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/1200181'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            年底選戰將至,《ETtoday新聞雲》最新民調顯示,高雄市長選舉,
            有32.0%支持民進黨陳其邁,30.4%支持國民黨韓國瑜,兩人差距僅1.6個百分點,這是兩人民
            調最接近的一次,選情相當緊繃。民進黨的執政包袱導致蔡英文的民調不理想,影響年底選
            情。此外,台北市長柯文哲近日拜會政壇大老時,傳出他與前立法院長王金平透露「蔡英文
            被太子、太后掌控」,似乎暗指蔡英文在黨內的權力被架空。《雲端最前線》27日邀請美麗
            島電子報董事長吳子嘉、資深評論員詹錫奎、資深媒體人陳敏鳳,與主持人楊文嘉帶您深入
            探討年底選舉縣市長選情發展。 《ETtoday新聞雲》於5月4日至6月19日進行「高屏縣市長
            選情大調查」。調查結果針對設籍於高雄市民眾進行分析發現,有32.0%支持民進黨陳其邁,
            而30.4%支持國民黨韓國瑜,兩人差距僅1.6%,另8.8%表示都不支持,24.7%則未表態,因此合
            計約三成四的高雄市民將可能成為未來左右選戰結果的關鍵,後續選情變化仍有待觀察。另
            一方面,從政黨傾向來看,在政黨傾向中立者的支持度,陳其邁15.5%、韓國瑜22.0%,兩人差
            距不大;然而仍有合計近六成的中立者為都不支持或未表態,因此這群中間選民的動向將成
            為未來決定誰勝誰負的關鍵。 事實上,執政黨近期爭議不斷,先是台大校長遴選案、年改衝
            突、斷交危機,再到吳音寧風波。對此,《美麗島電子報》董事長吳子嘉表示,蔡英文執政兩
            年多來,任用學者官僚和社運人士的政府團隊,造成許多錯誤的決策。小英在民進黨內以絕
            對領導來鞏固「蔡核心」的權威,現在看來已面臨崩盤。 根據《美麗島電子報》日前公布
            的國政民調,總統蔡英文民調持續低迷,行政院長賴清德施政滿意度呈現「死亡交叉」,不滿
            意度首次高於滿意度,顯示重大政治危機。對此,前總統陳水扁直呼總統、閣揆、政黨「三
            管齊下」,更透露年底選舉民進黨恐輸掉4、5個縣市。而民進黨黨內評估較危險的執政縣市
            包括:彰化縣、台中市、宜蘭縣、嘉義市、澎湖縣,竟與陳水扁的預測不謀而合,可能會掉4
            至5席縣市長。 值得關注的是,為拚2018連任,台北市長柯文哲近日積極拜會政壇大老,尋求
            建議或支持,卻傳出柯文哲拜會前立法院長王金平,談話時提到「蔡英文被太子、太后掌控
            」,暗指總統府秘書長陳菊是太后,綠營派系新潮流是太子,似乎點出蔡英文在黨內的權力被
            架空。對此,柯文哲受訪時未否認說過「太子、太后」,僅強調這是私底下聊天的內容。而
            媒體詢問柯文哲,是不是認為蔡英文被綁架,所以才不敢支持他?柯文哲回應,每一個政黨還
            是有它的派系問題,這也沒辦法,「我們就還是那句話,且戰且走,朋友要多、敵人要少,然後
            設法去爭取,其實投票的還是市民嘛」。 選戰倒數五個月,面對藍綠結構五五波的中台灣以
            及民進黨執政包袱,綠營選情相當緊繃,年底選情發展也讓總統蔡英文相當憂心。《雲端最
            前線》27日邀請美麗島電子報董事長吳子嘉、資深評論員詹錫奎、資深媒體人陳敏鳳,與主
            持人楊文嘉帶您深入探討年底選舉縣市長重大趨勢及選情發展。
            '''
        ),
    )
    assert parsed_news.category == '政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530070920
    assert parsed_news.reporter is None
    assert parsed_news.title == '高雄市長支持度陳其邁32%、韓國瑜30.4% 僅差1.6!'
    assert parsed_news.url_pattern == '1200181'
