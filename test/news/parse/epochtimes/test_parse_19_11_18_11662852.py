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
    url = r'https://www.epochtimes.com/b5/19/11/18/n11662852.htm'
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
            法國王后瑪麗•萊什琴斯卡(Marie Leszczynska,1703~1768年)在位42年,是法蘭西在位
            最長的凡爾賽宮女主人。這位波蘭王室出身的王后忠實而虔誠,對法國的影響很大。她的影響
            不是政治上的,而是在法國人生活層面上。 瑪麗王后以身作則,無條件地獻身於丈夫路易十五
            世(1710~1774)、她的孩子們,和法國人民。她忠於自己的信仰,每天參加兩次彌撒,一次
            懺悔。巴黎議會主席、瑪麗的顧問查爾斯•讓•弗朗索瓦•漢諾(Charles Jean-Franco
            is Hénault,1685~1770)在他的回憶錄中寫道:「她以自己的榜樣,把放蕩的宮廷變成一個
            遵守宗教儀式,同時又不減損其歡樂或威嚴的地方。」 每天下午,在宮廷履行王室職責後,
            瑪麗回到她的私人公寓,在那裡她與家人及密友相伴,她的密友小圈子中包括作家、哲學家和
            大臣。 王后寬敞的公寓裡有王后私人祈禱禮拜所用的講演室、綠色畫廊、浴室、休息室和
            詩人房間。詩人房間是瑪麗存放她的詩集的「一個非常小的空間」,呂恩斯公爵查爾斯•菲利
            普•達伯特(Charles-Philippe d’Albert)在回憶錄中寫道。 這公寓有不少掛著花環的
            露台和陽台。瑪麗喜愛有著鉛雕塑和假山框架,名為Monseigneur的花園庭院,這個小庭院以
            路易十四和瑪麗•泰瑞斯(Marie Thérèse)的兒子命名。 這私人公寓是她的避難所,她在此
            閱讀、休息、祈禱、縫製或繪畫。儘管她的波蘭國王父親被廢,但瑪麗受過王室教育,學習
            語言、舞蹈、唱歌、樂器、繪畫等。在綠色畫廊中,她繪製鉛筆畫及油畫,聆聽音樂和使用
            自己的印刷機進行打印。 作為凡爾賽宮《瑪麗•萊什琴斯卡的品味:瑪麗•萊什琴斯卡,一位
            未知的王后》展覽展出的精選50幅畫作中一部份,我們有幸可欣賞到王后本人的作品和其它
            藝術品。展覽於4月16日開幕,一直持續到2020年春季。展覽由格溫諾拉•菲爾曼(Gwenol
            a Firmin)和瑪麗•勞雷•德•羅奇布魯納(Marie-Laure de Rochebrune)策展,他們都是
            凡爾賽宮和特里亞農宮國家博物館的首席策展人,並由藝術史博士文森特•巴斯蒂安(Vince
            nt Bastien)協助。 展覽作品中體現出瑪麗王后對家庭、上帝和美的熱愛。 全家福 瑪麗
            私人公寓中的許多畫作畫的是王后1727年至1737年所生的10個孩子。第一個男孩,法國王
            儲 (Dauphin ) 路易‧費迪南德(Dauphin Louis Ferdinand)出生時,王后委託瑪麗•亞
            歷克西斯•西蒙•貝勒(Marie Alexis-Simon Belle,1674~1734年)為他繪肖像畫。這
            幅畫掛在瑪麗的浴室裡。瑪麗王后非常喜歡這幅畫,後來又委託畫家把自己和王儲兒子畫在
            一起。 這幅母子肖像畫大概是在王儲路易出生一年後畫的。在這幅畫中,瑪麗正坐著並保持
            優雅姿態,體現了坎潘夫人所說的,瑪麗在年輕時的「優雅精神」。坎潘夫人是為瑪麗小女兒
            讀書的人。瑪麗的髮飾織有鑽石,與鑲在精緻的、像金屬刺繡的金色連衣裙上的珠寶相呼應
            。她輕輕地握住兒子的手。王儲路易還只是一個嬰兒,但面部表情與母親王室氣息相似,與
            他稚嫩的年齡不符。也許他知道他的命運,躺椅上的金冠標誌著他的未來。他坐在成為國王時
            用的、有鳶尾花圖案的披風上。 在法國王儲路易的父親——路易十五的一幅畫像中,可以看到
            類似的符號和服飾。這幅肖像畫由一位姓名不可考的畫家於1728年繪製。在畫裡可看見,
            路易十五戴著聖靈勳章的衣領,披著王儲路易與母親肖像畫上的斗篷。在他右邊的桌子上是
            國王的王冠、權杖和查理曼大帝的正義之手——這是一種法式權杖,以祝福的姿態展示上帝的手
            。 瑪麗王后的藝術實踐 根據呂伊內公爵(Duke of Luynes)的說法,瑪麗王后並非天生
            就有繪畫天賦,但是她可以畫得很好。他寫道:「她從(繪畫)中獲得了很多樂趣。」 讓-巴蒂
            斯特奧德里Jean-Baptiste Oudry(1686~1755)是瑪麗王后最喜歡的畫家之一。瑪麗複製
            了他的一幅畫。在她的畫作《農場,瑪麗•萊什琴斯卡 根據 讓-巴蒂斯特奧德里作品的仿作
            》中,寧靜的畫面上描繪了鄉村豐收的景象和勤勞的農場主。據信,宮廷畫家埃蒂安尤拉特
            (Etienne Jeaurat)幫助她進行了這幅畫的繪製。尤拉特指導王后進行繪畫長達15年之久
            。 1761年,瑪麗王后和為國王國家公寓工作的5位畫家,畫了一系列中國風油畫《中國商會》
            。該系列是按照中國風格,以鳥瞰圖角度繪製的。畫面上有著精美的建築、服飾和景觀細節的
            系列畫,展示了各種場景,例如茶道、耶穌會傳福音和南京的集市。 凡爾賽宮於2018年購買
            了《中國商會》系列畫。作為王后的遺贈,這些畫自1768年起一直由王后的侍女諾埃爾小姐
            (the Comtesse de Noailles) 的家族保管。 《聖弗朗西斯‧澤維爾之死》 瑪麗渴望能
            減輕他人的痛苦。據記載,王后說:「我不需要(更多)衣服,窮人甚至沒有襯衫。」她支持
            招待所、診所和慈善基金會,致力於幫助有需要的人。她在凡爾賽建立了一個女修道院,以
            教育貧窮的女孩。王后去世後,被女修道院追授了職位。 瑪麗王后的宗教信仰在她的公寓中
            、她讀過的書,以及她所喜愛的藝術品中有重要地位。她偏愛有關早期基督教殉道者和耶穌會
            修道士的主題。當時,耶穌會修道士被法國驅逐。 瑪麗對聖弗朗西斯‧澤維爾 (St. Franc
            is Xavier) 特別感興趣。 這位耶穌會修道士曾在印度度過一段時間,並於1552年前往
            中國大陸傳福音。可惜在傳福音前,他在廣東沿海的桑川島去世。王后委託查爾斯‧安托萬‧
            科佩爾(Charles-Antoine Coypel,1694-1752年)於1749年創作了《聖弗朗西斯‧澤維
            爾之死》。畫面上,地上聖弗朗西斯死氣沉沉的身體的暗色調,幾乎將畫面一分為二:死亡的
            黑暗迎上了天使召喚並歡迎這位耶穌會修道士進入天堂的神聖之光。
            '''
        ),
    )
    assert parsed_news.category == '文化網,藝海漫遊,美術長廊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1574006400
    assert parsed_news.reporter == '洛林'
    assert parsed_news.title == '虔誠奉獻的法國王后瑪麗‧萊什琴斯卡與她的品味'
    assert parsed_news.url_pattern == '19-11-18-11662852'
