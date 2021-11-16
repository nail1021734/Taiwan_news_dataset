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
    url = r'https://star.ettoday.net/news/2085889'
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
            中國經濟增長趨緩態勢開始反映在消費數據上,八月社會消費品零售總額較七月衰退,年增率
            也趨緩。其中,家電零售年增率由正轉負,通訊器材(含手機)及汽車年增幅擴大。美國八月
            零售銷售雖意外優於預期,但受到持續的運輸問題及晶片短缺影響,八月電子產品及汽車的
            銷售額也出現月減幅擴大的情況。 缺貨依舊 照漲不誤 中美兩大消費市場的電子產品銷售
            趨緩,呼應近期電子品牌廠對供應鏈砍單的傳聞,市場對電子元件市場供需反轉的雜音並非
            空穴來風,邏輯上似乎站得住腳,卻忽略了部分事實。首先,部分品牌的零組件訂單調整,
            原因來自缺料導致產量減少、產品不夠賣,待缺料問題改善後訂單又會回籠。 其次,
            電子元件廠的產能供給並未增加,尤其是半導體晶圓代工產能,品牌廠短期砍單只是讓原先
            嚴重失衡的供需缺口稍為縮小,但實際上仍處於供不應求的情況,缺貨問題依舊存在,反映
            成本上揚的漲價潮將繼續上演,並不會因此中斷。 相信接下來只要各廠商漲價消息再次傳出,
            市場對供需反轉的擔憂就會自動消散,目前受砍單利空衝擊的錯殺股價未來都有獲得平反
            的機會。事實上,在原物料成本不斷墊高下,廠商調漲售價的動作在下半年更為積極,十月
            為第四季首個月份,不少廠商新一波漲價將生效,可預期屆時媒體又會拿來大作文章,成為
            炒熱股價漲升行情的助燃劑,投資人不妨可趁著現階段砍單雜音時逢低進場。 台積電掀起
            產業漲價蝴蝶效應 十月漲價重頭戲就是晶圓代工龍頭台積電(2330)十月起投片生產的
            晶片將全面漲價,成熟製程調漲二○%,先進製程調漲一○% ,成熟製程代工廠力積電(6770)
            也將於十月漲價,不僅會帶動整個晶圓代工廠的漲價潮,也會讓在其投片的IC設計廠更有理由
            轉嫁上揚成本跟客戶漲價,掀起半導體漲價的蝴蝶效應。台系一線IC設計廠日前已表示,預期
            明年第一季晶片平均單價將會再漲一○~二○%,並優先供貨給願意接受漲價的客戶。 在車用
            半導體領域市占率排行第六的安森美表示,因應上游原材料、製造及物流成本持續上漲,不得
            不同步提高價格,新的價格將在十月一日生效,並適用於新訂單和現有的積壓的未執行的訂單,
            距離上一次漲價的七月十日不到三個月時間,有利台灣車用半導體廠報價跟漲動作。另因車用
            晶片能夠優先獲得晶圓代工廠的產能支援,加上漲價效應貢獻,車用營收占比高的台廠營運將
            會有較大的成長動能。 德儀漲價又延交期 台廠獲得轉單機會 類比晶片廠德儀也表示,因應
            現在及可預見的未來原材料持續上漲的影響,九月十五日已先漲價,但有NB電池模組廠透漏近
            期臨時接到德儀通知,九月訂單部分必須遞延至十月出貨,還可能會在十月漲價一五%。 由於
            德儀的八吋晶圓廠產能短缺很嚴重,為了維持獲利優先生產單價較高的產品,導致單價低於一
            美元的產品產能嚴重不足,市場缺貨情況嚴重。德儀先前表示,超過八○%產品有穩定交期,
            隱含另外二○%產品交期並不穩定,造成市場搶貨嚴重價格暴漲,尤其是電源管理晶片。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1632478920
    assert parsed_news.reporter == '高適'
    assert parsed_news.title == '十月漲價潮 超級比一比'
    assert parsed_news.url_pattern == '2085889'
