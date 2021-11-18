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
    url = r'https://star.ettoday.net/news/2100299'
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
            2020年立法委員上任前,筆者曾擔任新聞記者、主播,從事媒體業20年,十分瞭解台灣媒體
            環境越來越艱難,不僅紙媒被網路媒體取代,近年來Facebook及Google等網路平台轉載
            新聞造成廣告收益被稀釋,讓新聞產製成本越來越單薄,嚴重影響內容產製品質,純網媒、
            紙媒跨足網媒與影視業跨足網媒等產業受害至深。 今(2021)年2月澳洲通過「新聞媒體
            與數位平台強制議價法」
            (News Media and Digital Platforms Mandatory Bargaining Code),
            筆者認為,台灣有其立法之必要性,數位平台免費轉載媒體辛苦產製的內容,瓜分媒體業者
            高比例的廣告收益,政府不能繼續坐視其搭便車,應遵循「使用者付費」原則,對Facebook及
            Google要求分潤,合理共享商業分潤。 分潤機制很複雜 媒體產業也有分不同規模,對
            數位平台依著度各異,通常大型媒體是平台主動尋求合作,規模較小媒體則需要平台的一方,
            可見分潤機制將會是一套複雜的機制,政府要當公道伯為平台及媒體提供協商管道。 自澳洲
            成功推動媒體議價法以來,筆者數次舉辦或參與產、官、學界會議,到院會總質詢、委員會
            質詢,瞭解政府研議進度、學者就適法性的討論及媒體界的訴求。現政院規劃,媒體議價機制
            將交由郭耀煌政務委員主持之「數位發展部」主導,但此主管單位最快明(2022)年第二季
            才掛牌上路。 日前總質詢時,NCC主委陳耀祥回應,媒體議價機制責目前由NCC、文化部與
            公平會先做產業調查,希望建立類似澳洲模型的分潤機制,有助媒體產業發展。從澳洲的例子
            來看,筆者認為,澳洲2月通過媒體議價法,7月才授權媒體與數位平台談判,以現在政院
            規劃進度,再送來立院立法,實屬緩不濟急,要引進台版媒體議價機制應該修法、協商
            「雙軌並行」。 基金分潤vs商業機制 從修法的角度,現行公平交易法第15條第8款但
            書明定,為促進產業發展的聯合行為所必要的共同行為,主管機關可允許內容產製業者要求
            數位平台回饋利潤,但是筆者擔心Facebook及Google協商誠意有多少?平台業者派出的代表
            層級是否足夠在協商制中有決定權? 巨型跨國數位平台經營台灣市場以廣告招攬為主,涉及
            營運利潤分配的協議兩家平台在台灣的辦公室高層恐無決策權,我認為應修法施以強制力,
            要求數位平台決策高層上談判桌。 然而,徒法不足以自行,協商也是必要的,巨型跨國數位
            平台在談判上擁有絕對優勢,所以台灣媒體與之協商必須握有足夠籌碼,而政府應協助
            產業調查與數據蒐集,媒體才有足夠籌碼進行有效談判。 有學者建議將以基金模式運作分潤
            ,藉此鼓勵優秀媒體,但筆者認為廣告分潤應該由商業機制決定,平台與媒體間所制定的分潤
            比例,是依照雙方在內容產製成本以及使用量所決定,若再由另外設置的「分潤基金」進行
            二次分配,完全破壞推動「媒體議價法」的本意。 除了澳洲的媒體議價法,丹麥在今年6月
            也與跨國數位平台集體協商要求付費,法國競爭管理局在今年7月更因Google未遵守
            「著作鄰接權」規範,重罰Google公司5億歐元。當國際都在著手規畫的同時,期待政府能
            加速爭取合理分潤,讓媒體與平台在平等的商業模式下共好、共享,協助台灣打造更優質的
            媒體產業,讓新聞人與媒體人的待遇能一併提升。
            '''
        ),
    )
    assert parsed_news.category == '雲論'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634109600
    assert parsed_news.reporter == '林楚茵'
    assert parsed_news.title == '媒體與網路平台議價 政府能扮演什麼角色?'
    assert parsed_news.url_pattern == '2100299'
