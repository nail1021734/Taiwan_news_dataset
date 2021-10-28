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
    url = r'https://www.epochtimes.com/b5/13/2/18/n3803627.htm'
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
            除了《大衛》和《卡西納戰役》,米開朗基羅同時期承接的工作還包括一座青銅的《大衛像
            》(今遺失),聖母百花教堂委託的《十二使徒像》(後來僅做了《聖馬太》粗雕),一座《布
            魯日聖母》,兩幅圓形的《聖母子》浮雕,還有一幅較知名的《聖家族》——即《多尼圓幅》
            (Doni Tondo),或稱《多尼聖母》(Doni Madonna)。 《聖家族》與聖母題材 《聖母子》或
            《聖家族》題材在文藝復興時期極受歡迎,純真美好的聖母子形像令人愉悅,不僅傳達聖經
            寓意,也符合了世人對家庭溫馨諧和的願望;因此常用代表圓滿、完美的圓幅創作。 米開朗
            基羅的圓幅蛋彩畫《聖家族》,是應佛羅倫斯富商安喬羅·多尼(Agnolo Doni)所託而繪製的
            。這也是米開朗基羅傳世的唯一完成的木板蛋彩畫,據推測是多尼為紀念與妻子
            Maddalena Strozzi的婚姻(1503~1504左右)而作。這幅《聖家族》遠超出當時約定俗成
            的表現法,再度顯示了米開朗基羅的藝術原創性。 首先,人物的安排十分緊密,這一點倒可能
            是受達芬奇1501年繪製的《聖母子與聖安娜》草圖影響——將幾個人物緊密重疊、壓縮在一個
            狹小的空間裡,形成更集中、有力的構圖。畫中以聖母為中心人物,跪坐在地,正轉過頭將聖嬰
            從後方聖約瑟的手中小心地接過來(一說是聖母將聖嬰遞給聖約瑟)。這個不自然的扭轉姿勢,
            不完全為了達到造形的目的,也具備了宗教的內涵:聖母仰望聖嬰的眼神,有慈愛也有崇敬,她以
            莊嚴的姿態承接了神的託付。聖母的造形也前所未見,她身著古代服飾,並沒有披戴頭巾或面
            紗,不但身體健壯,還裸露著一隻手臂,可說預告了西斯汀禮拜堂天頂《創世紀》中巨大女先
            知的形象。整體偏冷的色調,銳利的對比,都與當時社會流行的愉悅、諧和氣氛大相徑庭。
            畫面質感如雕刻般光滑、冰冷,卻也明亮細緻,散發著光輝。 聖家族三個人物互相凝視的眼
            神、扭轉的肢體都環繞成封閉的動勢,正好配合了整個圓形構圖。一道水平方向的石牆將畫
            面隔成前後兩個區塊:後方裸體人群是約旦河邊等待受洗的人們,象徵了耶穌到來之前的未
            開化世界,前方的聖家族則代表了基督降臨後的新世界;而在兩者間的小男孩,正是未來以洗
            禮帶領人們進入基督教化的施洗約翰。在舊世界,他是唯一仰頭望見未來救贖的人物。 這
            幅圓形作品的木框也十分具有特色,除了精美的浮刻雕飾,還有五個栩栩如生的聖人頭像突
            出環繞在框上,正上方是耶穌,下方是聖徒和天使。一般推測米開朗基羅可能參與或製作木
            框的設計。 米開朗基羅的聖母子作品中,從《梯邊聖母》算起,聖母的神情平靜肅穆者居多
            ;沒有達芬奇式的朦朧笑意,更無拉斐爾的甜美親切,這或許是藝術家的個性與強烈的宗教情
            感使然。如《布魯日聖母》雕像(1501~1503),聖母子二人眉目低垂,莊嚴靜肅,似乎延續了
            凡蒂岡《聖殤》的悲傷氣氛。之後的兩塊未完成的圓形浮雕《碧堤圓浮雕》(Pitti Tondo)
            和《塔戴圓浮雕》(Tadai Tondo),則由於其中幼童(耶穌和施洗約翰)的動態而顯出較人性
            的表現:如《碧堤聖母》中的聖嬰手托著額頭,哭喪的臉孔似乎因疲倦而向母親尋求慰藉,
            後方的小約翰則報以同情的目光;《塔戴聖母》中的聖嬰則被約翰抓來的小鳥所驚嚇而躲避。
            小鳥可能和拉斐爾所繪的《金翅雀聖母》中的小鳥有同樣的寓意,金翅雀喜歡在
            荊棘中築巢,暗示耶穌未來的受難。 此後米開朗基羅少有聖母子的主題,直到為美第奇家族
            設計的陵墓(1521~1534)中才再次出現。 由布魯日(Bruge)的慕斯克隆家族為裝飾當地聖母
            院而收購。 《碧堤圓浮雕》(Pitti Tondo)和《塔戴圓浮雕》(Tadai Tondo),兩幅均因委
            託人而得名。Tondo源自意大利文rotondo,原義為圓形。美術名詞意指以圓形為基底的繪畫
            或雕塑創作結構,可能是圓形的木板,也可能是在圓框之內構圖。文藝復興時期圓幅畫象徵
            完美、圓滿,通常用於祝福家庭或婚姻,題材也較為溫馨。 還有兩幅木板畫被推論是米開朗
            基羅早年的作品,一是《曼徹斯特聖母》(Manchester Madonna),估計是1495~1497年間在羅
            馬所作;另一件是《安葬耶穌》(Desposition in the Tombe,1500~1501),目前均收藏於倫
            敦國家畫廊。近年越來越多學者認同是米開朗基羅的真跡。 創作時間也可能與拉斐爾繪製
            Doni夫妻肖像畫同時(1505~1506)。 米開朗基羅曾經去臨摹達芬奇的《聖安娜》,然而即使
            臨摹他人作品,米開朗基羅也總是加上自己的見解,從新發展,不是完全模仿。
            '''
        ),
    )
    assert parsed_news.category == '文化網,藝海漫遊,美術長廊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361116800
    assert parsed_news.reporter is None
    assert parsed_news.title == '米開朗基羅《聖家族》'
    assert parsed_news.url_pattern == '13-2-18-3803627'
