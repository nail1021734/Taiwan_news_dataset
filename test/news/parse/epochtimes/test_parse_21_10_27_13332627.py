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
    url = r'https://www.epochtimes.com/b5/21/10/27/n13332627.htm'
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
            中華民國國防部在送達立法院的最新專案報告中指出,今年以來共機擾台已逾680架次,兩岸
            軍事對峙短期難緩解。報告分析「台海軍事緊張升高」對美中台三方關係的影響。 中華民國
            立法院外交及國防委員會28日邀請國防部長邱國正,就「台海軍事緊張升高對我國防戰備與
            美陸台三方關係之影響」進行專案報告。 報告指出,中共運用灰色地帶手段在台海周邊對台
            侵擾,透過演訓活動為武力犯台進行軍事整備,嚴重威脅台海安全與區域和平穩定。而國際
            社會也意識到中共的擴張行徑對區域帶來的安全威脅,因此台海和平的重要性受到外界高度
            重視與廣泛討論。 美國藉由聯合演習反制中共 國防部整評司司長苗蕙芬在報告中指出,美、
            日、印、澳於今年進行2階段「馬拉巴爾(Malabar)」演習,分別於菲律賓海及孟加拉灣等
            關鍵水域演練水面和反潛作戰。 另外,美國雷根號、卡爾文森號與英國伊莉莎白女王號航母
            打擊群與日本、紐西蘭(陸譯新西蘭)、澳洲等國海軍,10月於西太平洋地區進行聯合軍演,
            展現各民主盟邦在維護印太安全上合作無間,藉由聯合防衛力量以抗衡中共。 美英加等多國
            軍艦穿越台灣海峽 苗蕙芬表示,拜登政府延續川普(特朗普)總統自由開放印太戰略,視中共
            為挑戰其國家利益的競爭者。為應對中共過度的海事主張,美國在南海執行航行自由行動
            (FONOPs),派遣驅逐艦例行性通過台海,自今年以來,已10度航經台海。另外,英國護衛艦、
            加拿大巡防艦等船艦也曾穿越台海,維護國際法航行權益。 她指出,中共不斷擴大影響力,
            直接衝擊美國主導建立的國際秩序。雙方在許多議題上針鋒相對,台美則在價值理念一致下,
            持續緊密互動。 美國聯合盟友應對中共挑戰 中共拉攏盟友與美國展開激烈競爭 北約祕書長
            史騰柏格(Jens Stoltenberg)表示,中共網絡能力、新技術與長程飛彈已帶來安全隱憂,
            將結合歐洲集體力量應對。苗蕙芬表示,美國運用美英澳成立「三方安全夥伴關係」(AUKUS)、
            「四方安全對話」(QUAD)及「五眼聯盟」(FVEY)等多邊機制,以具體行動推動自由開放的
            印太戰略。 苗蕙芬表示,面對中共在各領域挑戰美國的領導地位,美中已各自拉攏盟友展開
            激烈競爭。但美國國防部表示,希望與共軍建立一個建設性、穩定的軍事關係,美中於9月下旬
            進行「國防政策協調對話」,藉由通話、會面維持溝通機制順暢,確保雙邊競爭關係不會演變
            為軍事衝突。後續是否舉行拜習會,為重要觀察指標。 「中共向來視台灣為最重要議題,
            積極以『以戰逼和』、『以武促統』等作為,持續加大對台軍事威懾,欲迫使中華民國政府
            接受『一國兩制』。」她說。 她表示,未來台灣所承受的軍事壓力更較以往為重,國軍將
            持續充實國防,展現自我防衛決心,嚇阻中共,使其因考量承受巨大代價而不致輕啟
            戰端。 美國支持台灣強化自我防衛能力 美國國會不分黨派對台支持,她表示,從審議中的
            「2022年國防授權法案」(NDAA)與台灣有關條文即可明顯看出。法案對台措施包括邀請
            台灣參與演習、加強台灣後備力量、確保美軍能力以防止中共改變台海現狀等,美政府供售
            關鍵戰力給台灣,未來依據「台灣關係法」及「六項保證」,持續深化人員協訓、資安防護、
            情報分享等各項軍事交流合作與安全關係,台美將維持緊密友好關係。 苗蕙芬表示,面對共機
            頻繁侵擾,國軍將壓力轉化為督促戰備整備的動力,隨時有效應對突發狀況。台灣國防戰備的
            強化作為,包括強化情資交流掌握共軍動態、提升聯戰能力妥善應處共軍威脅、提升人力素質
            優化戰力、編列特別預算加速武器籌獲、精進革新後備動員機制、強化民心士氣應對中共
            認知作戰。 台國防部:捍衛國家主權 絕不在脅迫下屈服退讓 國防部說,受到中共武力擴張
            與加大對台軍事施壓的影響,台海情勢嚴峻且呈現不穩定的狀態。面對共軍機艦挑釁的行動,
            國軍將持續發展不對稱防衛戰略,強化整體防衛能量,並深化與理念相近國家的交流與合作,
            台灣不與中共軍備競賽,亦不尋求軍事對抗,期盼兩岸和平共存。 國防部表示,但面對中共
            威脅中華民國國家安全,必將竭盡全力捍衛國家主權,絕不會在脅迫下屈服退讓。「自己國家
            自己救」,國軍秉持「備戰不求戰、應戰不避戰」的信念,遏阻中共犯台的企圖與行動,有
            信心與能力達成確保國家安全的目標。
            '''
        ),
    )
    assert parsed_news.category == '台灣'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1635264000
    assert parsed_news.reporter == '鍾元台北'
    assert parsed_news.title == '台國防部分析:台海局勢緊張對美中台的影響'
    assert parsed_news.url_pattern == '21-10-27-13332627'
