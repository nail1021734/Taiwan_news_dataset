import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/202109220356.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)
    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            台灣已遞出加入跨太平洋夥伴全面進步協定(CPTPP)申請,中經院台灣WTO中心資深
            副執行長李淳肯定「終於走了大膽而且必要的一步」,但想拿入場券,仍必須面對日本核災區
            食品、農產品限制等2大挑戰。 CPTPP 前身為跨太平洋夥伴協定(TPP),美國在前總統川普
            時期退出,現由日本主導,中國16日正式提出書面申請加入CPTPP,引起高度關注;數天後,
            行政院高層今天晚間證實,台灣也已經正式提出加入CPTPP申請。 李淳接受中央社記者
            訪問時表示,「台灣終於走了大膽而且必要的一步,因為接下來機會之窗只會愈來愈小、處境
            愈來愈艱難,這個時機點非常對」,李淳直言,台灣有必要跨出這步,因為中國已經提出
            申請,一旦中國正式加入CPTPP,台灣就沒有空間了。 李淳說明CPTPP入會規則,台灣提出
            申請後,紐西蘭的秘書處會將申請信函交給各國,下一步則是執行委員會決定是否成立工作
            小組;但在這之前,申請國應化解各國關切的問題,也就是說,在成立工作小組前,各國會先出
            考題。 以中國為例,面臨與澳洲之間貿易制裁的問題,要讓澳洲有滿意答覆;至於台灣,
            最關鍵就是日本核災區食品禁令,以及與其他國家有些農產品檢驗、檢疫等議題。 李淳
            指出,CPTPP許多成員國是農業出口國,但台灣很多規定「只會進場、不會退場」,一旦限制
            就很難落日,使得檢驗、檢疫方面,不論是程序或是科學性不足,一直受到指責,這是台灣取得
            CPTPP入場券前必須解決的難題。 不過在考題的處理順序上,日本核災區食品最關鍵、但
            不是最優先。李淳解釋,日本首相即將換人,今年下半年並不是談判的好時機,應該要與
            日本政府溝通,說明順序考量,展現誠意;在這期間,可以先解決其他國家關切的程序、制度
            等議題。 若台灣順利解決各國關切議題,CPTPP成立工作小組後,李淳認為這是一個
            重大工程,台灣要在首次會議說明目前為止做出的努力,在達到標準做了哪些修正、盤點現
            階段成果,也必須在首次會議後一個月內,提出關稅承諾。 「時間壓力會非常大」,李淳
            表示,當台灣正式遞出申請,勢必未來會走向更開放,政府應該加速準備如何面對相關影響並
            做出調整。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1632240000
    assert parsed_news.reporter == '潘姿羽台北'
    assert parsed_news.title == '台灣申請加入CPTPP 學者:走出大膽且必要的一步'
    assert parsed_news.url_pattern == '202109220356'
