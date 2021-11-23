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
    url = r'https://www.epochtimes.com/b5/19/12/13/n11721610.htm'
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
            澳大利亞的一樁重大醜聞暴露出中共的猖獗情報活動。 據澳大利亞媒體報導,在五月大選
            之前的某一天,中共情報人員接觸了富有的32歲豪車經銷商尼克‧趙(Nick Zhao),讓他為
            中共工作。 趙是華裔澳大利亞人,是自由黨成員。據稱中共試圖招募他競選國會議員。報導
            說,他們向趙提供了近70萬美元的競選資金。關於中方向趙提供資金的其它方面的細節尚不得
            而知;但是,如果他贏得議會席位,中方將向他定期支付薪水,這將是整個計劃的一部分。 中共
            的情報以價格低廉而臭名昭著,但他們將不得不拿出足夠好的條件,讓本來已經很富有的趙能夠
            動心為他們工作。由於他們僅為趙的競選活動就提供了近70萬美元,由此可以估計,中共一定
            考慮過要每年向趙支付100萬美元薪水。 按照情報界的標準,這筆錢也是金額巨大了。如前
            所述,對慣於精打細算的中共情報活動來說,這筆錢更是大手筆。 這起醜聞透露出許多有趣的
            地方。對於中共來說,他們願意在一段時間內投入數百萬美元,以獲得情報來源和能在澳大利亞
            國會內部有影響力的代理,這對他們而言,是高度優先的任務。 好消息是,他們顯然沒有達到
            想在澳大利亞國會內部獲得情報或影響力的目的。壞消息是他們在這個問題上正在努力爭取,
            並且願意冒較大的風險以取得進展,可以打賭他們現在很忙。 澳大利亞顯然在中共的目標名單
            上,並且對於這種類型的攻擊還沒有做好準備,從趙氏案的處理方式就能看出來。話雖如此,
            澳大利亞已經意識到這一問題,並為此做好準備,2018年通過了新法律,以對抗外國干擾
            。 毫無疑問,中共長期以來打算控制南中國海、南太平洋直至澳大利亞。為達此目的,中共
            幾十年來一直在招募澳洲華裔做間諜,這已成為中共的慣用伎倆。 關於趙跟與他接觸的、據稱
            是中共情報人員的談話內容,目前沒有公開信息,但他如實地向澳大利亞安全情報組織(ASIO)
            報告了整個事件。 ASIO公開表示他們正認真對待此事,並且清楚地意識到來自中共的威脅是
            真實存在的。今年早些時候,趙某被發現死在一家酒店的客房裡。死因可疑,驗屍官正在調查
            。 在另一起事件中,華裔澳大利亞議員廖嬋娥(Gladys Liu)成功當選澳大利亞國會議員。
            澳大利亞媒體披露,她與親北京的團體有關聯,後來她受到了嚴格的審查。她否認有任何不正當
            行為或效忠北京,澳大利亞總理斯科特‧莫里森(Scott Morrison)力挺廖嬋娥,並辯稱她受
            了誹謗中傷。 值得注意的是,廖嬋娥確實與親北京的團體有聯繫,但此後被忽視或被認為微不
            足道。全球範圍內有許多這類情況,在維基上稍微搜索一下就會發現,近年來有30多個華人
            被捕或被指控從事針對美國的情報活動。 澳大利亞媒體還報導了王立強案,王自稱是中共間諜
            並已在澳大利亞申請庇護。據報導,王向當局提供了有關在香港、台灣和澳大利亞從事間諜
            活動的信息,並聲稱曾「親自參與」。 2018年,美國的消息披露加利福尼亞州的聯邦參議員
            范士丹(Dianne Feinstein)的司機為中共情報部門工作了20年。 范士丹淡化這一指控,
            稱司機從未接觸過機密信息。問題在於,他不需要接觸機密信息也可以發揮很大的作用。 他
            不僅僅是一名司機,還是一個辦公室經理。他也是亞裔美國人社區的聯絡人,還代表參議員出席
            在中共領事館的活動。他可能能夠接觸范士丹的捐款人,並可能與新的捐款人建立聯繫。而
            這些捐款人中可能有人跟中共有某種聯繫。政客競遠活動的大筆捐款確實對立法有影響
            。 而且,出於國家利益也應該找出這位司機間諜是否推薦或發展了范士丹在華盛頓辦公室的
            工作人員,在那裡他們可以擴大蒐集有用信息的範圍。 出於政治原因而將所有注意力都集中
            在俄羅斯情報部門,這種行為是在損害美國的國家安全。儘管俄羅斯確實構成威脅,但美國面臨
            的最大的長期戰略威脅是中國(中共),而不是俄羅斯。僅關注俄羅斯而忽略中共是破壞性的,
            也是危險的。 布拉德‧約翰遜(Brad Johnson)是美國中央情報局(CIA)已退休的資深
            情報官,曾任情報站負責人。他是「美國情報改革」機構的總裁。
            '''
        ),
    )
    assert parsed_news.category == '時政評論'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576166400
    assert parsed_news.reporter is None
    assert parsed_news.title == '中共在澳洲間諜活動猖獗'
    assert parsed_news.url_pattern == '19-12-13-11721610'
