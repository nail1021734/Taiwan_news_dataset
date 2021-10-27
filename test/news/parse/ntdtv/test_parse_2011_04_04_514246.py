import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/04/04/a514246.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            近一段時期以來,中共為形成寒蟬效應,掀起逮捕異議人士浪潮。國際社會除了對中共表示
            強烈譴責之外,包括美國、英國和多個人權組織對中國的人權狀況表示憂心忡忡。 目前,
            中國大陸至少有四名異議人士付出慘重代價。由於他們在網上轉載呼籲“中國茉莉花集會”
            的消息,被當局以「煽動顛覆國家政權罪」逮捕,他們分別是四川的陳衛、冉雲飛和丁茅,以及
            浙江的郭衛東。 此外,中共還剛剛拒絕了聯合國委員會要求立即釋放被無理關押的維權律師
            高智晟的要求。但查禁目錄(Index on Censorship)組織在3月24號把言論自由獎頒發
            給了高智晟。 據《美國之音》報導,美國國務院東亞事務助理國務卿坎貝爾
            (Kurt Campbell)31號在國會聽證會上表示,中國近來發生的包括人權律師被強制失蹤和
            打壓外國記者等現象,增加了美國對中國人權狀況的擔憂。 坎貝爾還說,美國已經就
            人權問題,多次向中共國家主席胡錦濤在“公開和私下都進行了嚴肅表態”。 “北京之春”
            主編胡平:“今天中共當局堅持對自由,民主的普世價值的拒絕,已經跟它當初的共產革命那
            一套意識形態來衡量截然相反。實際上就是變成了一種赤裸裸的維護自己權力和特殊利益的
            這麼一個集團。只要它覺得對自己利益有妨害的,它就一概拒絕。” 同一天,英國外交部發佈
            2010年人權與民主報告指出,中共為期兩年的人權行動計劃已經到期,但在人權和政治開放
            領域卻出現惡化。 據BBC報導,這份報告顯示,當局對維權活動人士和言論自由都加緊了打壓
            和鉗制,中國司法不透明並且執法不一致。中國是被報告點名的26個在人權問題上需要關注的
            國家之一。 “大赦國際”亞太地區主任扎裡費(Sam Zarifi)也對《美國之音》表示,中共
            當局對批評越來越敏感,而打擊行動甚至擴大到了那些不應該被認為是異議人士的人身上。
            扎裡費對這種趨勢感到憂心忡忡。 位於香港的“維權網”(Human Rights Defenders)
            形容中國的活動人士在一個“敵對而危險的環境”中生存。 這個組織指出,根據記錄,2010年
            發生3,544起隨意拘押、118起虐待和36起活動人士失蹤事件。 巴黎的“無國界記者”組織也
            譴責中國警察對待外國記者的“流氓態度”。 此外,對華援助協會在3月31號發佈《中國大陸
            境內基督教會和基督徒遭受政府逼迫的年度報告》指出,2010年中國(共)對基督教會和
            基督教徒的迫害程度增加。 對華援助協會說,去年收集到的中國基督教會和教徒受迫害的
            案例有90件,比前一年上升16.9%,受迫害人數3343人。而被當局抓捕的人有556人,比上年
            增加了42.9%。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1301846400
    assert parsed_news.reporter == '李靜,王明宇'
    assert parsed_news.title == '中國人權告急 國際社會憂心忡忡'
    assert parsed_news.url_pattern == '2011-04-04-514246'
