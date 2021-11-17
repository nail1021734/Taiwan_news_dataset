import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/26309?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            Q:為何要舉行新憲公投? A:2012年12月,在現已遭罷黜的前總統穆爾西
            (Mohammed Morsi)主政下通過了後穆巴拉克(Hosni Mubarak)時代的憲法,
            但當時雖然以63.8%的比例通過,但投票人數僅佔埃及合法投票人口的32.9%,代表性不足,
            因此當穆爾西於去年7月遭罷黜後,這部憲法也遭冷凍。臨時政府希冀以更多的選票支撐來
            擴充這部新憲法,以及罷黜穆爾西的正當性,若新憲公投過關,也將進行新總統與新國會
            的選舉。 Q:舊憲法的缺失為何? A:前一部憲法由一個100名成員所組成的委員會起草,
            成員中大多為伊斯蘭政黨成員,無法忠實反映埃及社會中自由派與其他宗教的意見,也與
            2011年推翻穆巴拉克追求民主的主要訴求不符,其中有關軍事法庭的條款文字內容更遭人
            詬病,舊憲法對於佔了埃及人口10%的女性以或其他宗教人口的權利保障也嫌不足。 Q:
            新憲法有何不同? A:新憲由一個臨時組成的委員會起草,50名委員會成員中僅2名伊斯蘭
            政黨代表,保留了舊憲法中「伊斯蘭教為國教」的文字,但對於舊憲法中賦予伊斯蘭律法為
            立法基礎的條款細節予以刪除,新憲法僅保留「伊斯蘭律法為立法基礎」文字,不再
            贅述細節。其次,新憲法規定任何新設立的政黨不得以宗教、種族、性別與地域等為
            創設宗旨,避免激化衝突,但在舊憲法中僅著墨「不得以宗教歧視為創黨理念」。
            再者,軍事最高委員會(Supreme Council of the Armed Forces, SCAF)
            握有國防部長的任命權,也可以軍事法庭審判平民。最後,根據新憲法,埃及國會將
            首次擁有彈劾與起訴總統的權力。 Q:埃及人民怎麼看新憲法? A:大致分為三派:支持、
            反對與杯葛。支持陣營大多屬於自由派立場,對新憲法持反對意見的多為反對軍方藉此
            擴權的人士,意欲杯葛的旨在捍衛穆爾西的正當性。 Q:會發生衝突嗎? A:臨時政府誓言
            會讓公投過程平順進行,先前已規定超過10人的公開聚會必須登記,並表示對於非法聚會採
            「零容忍」(zero-tolerance)態度,除各地投票所外,大批軍警於投票期間也部署在
            埃及央行、水電設施與國會周邊,以防衝突爆發。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1389658800
    assert parsed_news.reporter == '簡嘉宏'
    assert parsed_news.title == '埃及新憲公投Q&A'
    assert parsed_news.url_pattern == '26309'
