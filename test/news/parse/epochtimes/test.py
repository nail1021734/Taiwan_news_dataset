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
    url = r'https://www.epochtimes.com/b5/19/12/30/n11756075.htm'
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
            還有幾十個小時,2020年就要到了。回顧2019年,圍繞著中共,發生了不少大事:香港半年有餘並且仍在繼續的大規模民衆抗爭、美中貿易戰兩度嚴重升級等等。這些事讓北京連連受挫,焦頭爛額。不過即使這樣,習近平仍然被「封」為「人民領袖」。法國《世界報》認為,2019年是北京「恐怖之年」。 中共「恐怖之年」 官方在昨天(12月29日)的通報中,給習近平頭上戴上了一個「人民領袖」的頭銜。 從2016年確立「習核心」,2017年把「習思想」寫入黨章,到2018年「習思想」寫入憲法,到如今被封「人民領袖」,中共官媒還公布了一張照片,是政治局開會時的場面,照片正中的位置是習在講話,其他人都在忙活記筆記。 對此,法廣表示疑惑:北京當局的領導地位已經至高無上,還用得著再加個頭銜肯定嗎? 說來說去,還是不自信的表現,因為2019年實在拿不出可以吹噓的事情。正如諸葛高參在大紀元文章《2019年終,只有一人在假睡》中所說,「如今,連最不要臉的黨媒都找不到什麼可煽乎的偉大成就了」。 與此對應的是,中國發生的事,哪怕是一個局部性的小事件,都會很快在全世界引起迴響。比如鎮原的圖書館員們焚燒60多本「政治不正確」的書,引起了世界大譁。 這麼個局部事件就能引起軒然大波,何況香港和貿易戰這些更大事件?法國《世界報》表示,對一個領導人來說,這是「最糟糕的」。2019年,對北京來說,就是一個「恐怖之年」。 香港人「死磕」 年初,港府推行《逃犯條例》,先後引起了2次大規模遊行和1次靜坐的抗議,但是北京仍然要求林鄭當局強行推動,引發了900多場大大小小的各種抗議活動,至今沒有停歇。 在6000多人被抓被打、無數人被摧殘折磨,甚至失去生命之下,香港年輕人毫無懼色,依然用血肉之軀向極權說「不」,要求北京兌現承諾。自從中共六四大屠殺事件以來,這是中共遇到的最嚴重政治事件。 其實香港事件就是衝著北京來的,承諾一國兩制,卻不斷蠶食;承諾直選,卻又遙遙無期,再加上港警濫權。香港人被步步逼仄的生活,讓他們感到「沒自由,毋寧死」。 香港民眾的「死磕」已經向世界昭示:香港年輕人已經做好了準備,與其生活在中共的魔爪之下,不如以犧牲去爭取自由。 香港人的努力,已經贏得了世界的支持。美國、歐盟、日本、英國、加拿大等等,多個國家都在聲援香港,聲討中共。 特別是美國,率先就香港人權問題專門立法,制裁那些侵害香港人權的所有官員。 貿易戰成北京的「滑鐵盧」 不過令北京更感到「恐怖」的,其實還是貿易戰。北京曾高喊2020年全面進入小康社會,但是在貿易戰的影響下,這個夢想可能會一直睡在2019年。 雖然美中雙方都表示已達成了第一階段貿易協議,但臨時協議根本不能終止貿易戰,美中根本性的分歧還沒有觸及。即使簽署了第一階段協議,貿易戰還是會隨時重燃戰火。貿易戰,是北京誤判、應對失策的開始,也是北京形象倒退的滑鐵盧。 在這一年中,中共花高價買俄羅斯豬肉,卻引進了非洲豬瘟,使養豬業遭受重創,生豬存欄僅剩1/3左右。豬肉飛漲的價格,使買豬肉成了「炫富」的形式。吃一口豬肉,竟然成了中國人最看重的節日——過年的一種奢望。 打了一年多的美中貿易戰,已經導致中國經濟全面滑坡,GDP出現了30年來的最慢增速。大量企業債務違約,據《日經新聞》報導,國企難以償付的債務就高達400億人民幣,比去年增加了3倍。 大量的工廠倒閉,使難以計數的工人失業,中國百姓怨聲載道,「茶壺風暴」正在逼近零界點。 這正是北京寢食難安、心驚肉跳的地方,倘若「群體性失業」引發「大規模暴動」,很可能就是中共政權的終結之日。 習近平在冒險 2019年,麻煩不斷。 歷史學家、中國問題專家林蔚(Arthur Waldron)曾對英文大紀元說過,習近平幕僚曾親口講過,體制內的人都知道中共已經進入了死胡同,步步是雷,走錯一步就可能「粉身碎骨」。 就是這種情況下,習近平的權力在不斷增加,現在又加上了「人民領袖」的頭銜。 這是典型的末日心態,看到中共在劫難逃了,誰也不想擔責任。於是使勁抬習,恨不得讓他頂上所有的頭銜。 分析中共黨政文件的研究機構「中國官方」董事總經理瑞安·曼努埃爾(Ryan Manuel)對《華爾街日報》表示,宣告自己擁有至高無上的決策權這是「冒險」,「在遇到困難的決策時,如果誰的決策出了問題,誰就需要承擔責任」。 好的,感謝您關注新聞看點,再會。
            '''
        ),
    )
    assert parsed_news.category == '新聞看點'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577635200
    assert parsed_news.reporter is None
    assert parsed_news.title == '法媒:2019 北京的恐怖之年'
    assert parsed_news.url_pattern == '19-12-30-11756075'
