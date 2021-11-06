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
    url = r'https://www.epochtimes.com/b5/13/2/7/n3795671.htm'
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
            《安加里之戰》與《卡西納之役》 佛羅倫斯在一四九四年成立共和國後,新政府決定在維
            奇歐宮(舊宮,Palazzo Vecchio,今市政廳)增設一個能容納五百人的議會大廳
            (salon dei Cinque-cento)。大部分的建築工程在一五〇〇年完成,但會議廳的兩側
            需要裝飾壁畫以展現共和國的光榮歷史,特別是一三九四年對比薩和一四四〇年對米蘭的
            兩次勝利戰役。政府決定邀請藝術界的重量級大師來共襄盛舉。於是首先邀請了米蘭
            《最後的晚餐》的作者達芬奇繪製《安加里之戰》;幾個月後,又託藝壇新星米開朗基羅繪製
            另一面牆壁,表現戰勝比薩的「卡西納」戰役。這是完成《大衛像》之後,米開朗基羅立刻
            面對另一項重要的公共工程。 在佛羅倫斯,達芬奇和米開朗基羅兩位藝術天才之間的不睦是
            眾所周知的。年齡的差距
            使他們分別屬於兩個不同的世代:達芬奇屬於十五世紀偉大的羅倫佐時代;而年輕二十三歲
            的米開朗基羅則屬於薩弗納羅拉以後的共和時代。在外表和性格上倆人也不同,達芬奇注重
            外表,儀態溫雅;米開朗基羅不修邊幅,直率粗魯;達芬奇喜以理性、科學的態度來對待藝術,
            米開朗基羅則以內在激情表現靈性之美。藝術觀點上,達芬奇認為繪畫是最高尚的藝術,能
            真實表現出所有眼睛看到的所有景物,以雕刻家自居的米開朗基羅認為雕刻是更偉大的藝術
            。米開朗基羅曾經當眾嘲弄達芬奇米蘭青銅騎馬像的失敗;而達芬奇也在《大衛像》安置的
            會議上和米開朗基羅意見相左,欲使大衛放在不起眼的地方。 所以,當兩大巨星將在維奇歐
            宮會議大廳對壘競技的消息傳出後,立刻成為佛羅倫斯街談巷議的熱門話題。共和政府的用
            意在於掀起活動熱潮,同時可以此競爭刺激兩位大師將才華發揮到極限,為佛羅倫斯再創作
            出偉大藝術。這個事件確實哄動一時,甚至許多其它地區的藝術家(例如拉斐爾就是其一)都
            把握這難得的機會,慕名前來觀摩兩位大師的作品。可惜的是,兩個藝術家最終都沒有完成
            他們的工作而離開了佛羅倫斯。倒不是藝術家不夠努力,其實倆人都準備了巨大的厚紙板草
            圖,也都曾經公開展示在公眾眼前。 由於達芬奇不願受限於濕壁畫,再次大膽嘗試陌生的技
            法—失傳已久的羅馬蠟畫技術,結果以失敗告終;而米開朗基羅甚至還沒有動到筆刷,就因為
            教皇儒略二世的緊急徵召而前往羅馬簽約,為教皇設計靈寢雕像。 至於《卡西納戰役》的
            圖稿,在米開朗基羅離開之後曾經轉傳於藝術家之間,可惜被過度的臨摹而逐漸毀損,甚至被
            搶撕成數片,散落於意大利各地宮廷,最後不知所終。我們只能從後世幾代畫家的臨摹版本
            和米開朗基羅的素描習作中,大致揣摩出原作的樣貌。 米開朗基羅為《卡西納戰役》所作
            的習作,人體的大幅度扭轉能表現肌肉結構的變化,充滿力量。 根據Giovanni Villani的十
            四世紀編年記載,在卡西納附近紮營的佛羅倫斯士兵們,正在亞諾河中洗浴時突遇敵軍來襲
            。米開朗基羅的草圖中,表現了裸身洗浴的士兵們聽到號角響起,慌忙中抓起武器起身應戰
            的情況。藉著這個題材,米開朗基羅充分表現了的人體大幅度扭轉的各種動態,充滿緊張與
            陽剛的力量;與他早年的浮雕《山陀兒之戰》遙相呼應。相較於達芬奇從繪畫的角度來經營
            畫面效果,米開朗基羅自始至終沒有忘記他雕刻家的身分,他以人體為表現元素,畫中人物一
            個個如雕像般肌肉結實,輪廓分明;整體的造形力度生動而緊密。 這一場原來被高度期待的
            藝術對決就這樣勝負未定而不了了之。 十六世紀中期Anonimo Magliabechiano在他的手稿
            中記載了一段軼事:一日達芬奇和喬凡尼‧達‧加文偶然經過聖三位教堂,一群紳士正在討論
            但丁的一段文字,他們叫住達芬奇請他解釋其中涵意。正好米開朗基羅也經過,其中有人和
            他打了招呼。達芬奇就說:「問米開朗基羅吧,他可以為你們解釋。」米開朗基羅以為達芬
            奇在嘲弄他,就氣沖沖地回答:「你倒是自己解釋,畫了騎馬銅像的草圖又鑄不出來,把它留
            在那兒走了,真是丟臉。」說完後大步走開,留下了面紅耳赤的達芬奇。 達芬奇使用古代的
            蠟畫技術,上色前將蠟和顏料溶合,在塗了松脂的石膏表面作畫,由於這種技術本身的用法,
            色彩無法自然乾;加上天候不佳,突然的潮氣使得固定草圖的泥灰液化。達芬奇為了克服這
            種情況使用火盆暖牆,結果使得上方的色彩尚未凝固,下方的顏色卻因火烤而溶解流失了。
            最後畫家不得不宣布放棄。
            '''
        ),
    )
    assert parsed_news.category == '文化網,藝海漫遊,美術長廊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1360166400
    assert parsed_news.reporter is None
    assert parsed_news.title == '米開朗基羅與達芬奇交鋒'
    assert parsed_news.url_pattern == '13-2-7-3795671'
