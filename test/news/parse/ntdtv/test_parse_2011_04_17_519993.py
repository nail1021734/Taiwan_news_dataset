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
    url = r'https://www.ntdtv.com/b5/2011/04/17/a519993.html'
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
            澳洲聯邦政府目前已經查獲多名隱瞞收入、騙取福利金進行賭博的欺詐者,部份已被定罪並
            判家庭拘留,其餘也將面臨起訴。政府要求行騙者償還在賭場中揮霍的,總額超過900萬澳元
            的全部福利金。 據快遞報報導,福利部(Centrelink)在過去3年中共對1052例有大額賭博
            嫌疑的福利金領取者進行了調查,已查獲確認521名行騙者,有關部門還發現部份人員有為
            犯罪團夥洗錢的嫌疑。 其中,昆省發現32名欺詐者,騙款總額接近50萬元,紐省查獲128名
            欺詐者,騙款額超過220萬元,而維省的279名欺詐者共騙取了500萬元福利金。聯邦檢控專員
            已收到對15名福利金領取者欺詐罪的起訴,所有的人都會被強迫向納稅人償還欺詐
            所得。 這些人對福利部宣稱他們等著福利金維持生活,但實際上卻過著奢侈的生活,僅每年
            在賭場上的揮霍就高達10萬澳元。其中,紐省的一名百萬富翁向福利部瞞報收入,在短短幾年
            中騙取的養老金高達9.6萬元。 聯邦立法部門要求各賭場向執法部門提供進行大數額賭博的
            常客的信息。公共事業部長普利波塞克(Tanya Plibersek)解釋說,福利部通過和賭場
            核對大額賭博者的信息,就能發現誰可能隱藏了資產和收入,騙取社會福利,甚至洗錢。 她
            還表示,如果福利金領取者衹是在某一天運氣好贏得一筆錢,福利部不會將其認定為收入。但是,
            那些一邊領著政府福利,一邊不斷光顧賭場進行大額賭博的人,必須能夠證明他們沒有向政府
            隱瞞資產和收入。 聯邦政府的此次調查正值全國對老虎機改革的激烈爭論之際。政府計劃在
            老虎機中采用強制性預先承諾系統,限制賭博者的賭注額。聯邦獨立議員謝諾芬
            (Nick Xenophon)認為老虎機改革有助於執法,他說犯罪份子每年都通過老虎機洗錢,而
            通過在老虎機上設置預先承諾系統,讓賭博者在行賭前預先決定並承諾輸錢的上限,能夠制止
            洗錢行為。 另據悉尼晨鋒報報導,老虎機改革設想最早由塔省獨立議員威爾基
            (Andrew Wilkie)提出,吉拉德政府正在徵求各省和行政區的支持,並將提交國會討論通過,
            但遭到了俱樂部的強烈反對。澳大利亞俱樂部協會和澳大利亞酒店聯合會已發起20萬澳元的
            廣告運動試圖阻止強制立法,稱這樣做不符合澳洲文化。 協會會長博爾(Anthony Ball)
            表示,該做法在去年昆省和南澳的自願試行中,70%的人表示反對將其立法成為強制性要求。但
            承擔該調研的阿德雷德韋斯利聯合養老中心(UCWA)首席執行官斯格拉伯
            (Simon Schrapel) 提醒政府要警惕所謂的這不是「澳洲人想要的」的言論,因為民意
            調研的結果恰恰相反。 澳大利亞社會經濟研究所對1411人的調研顯示,絕大多數受訪者,
            無論收入水平、教育背景、所在省份還是支持聯盟黨或工黨,都表示支持,其中年薪4萬以下
            的低收入人群支持率最高,達到70%,中高收入人群支持率為64%。從地區分佈來看,塔省
            支持者比例最高,為74%,紐省和昆省略低,但也達到了64%。 據悉,由工業、學術界和社會
            專家組成的,由捨爾戈德教授(Peter Shergold)領銜,為政府部長級提供賭博諮詢的智囊團將
            在週一拿出實施預先承諾系統的最佳方案。
            '''
        ),
    )
    assert parsed_news.category == '海外華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302969600
    assert parsed_news.reporter is None
    assert parsed_news.title == '數百名澳人騙福利金豪賭'
    assert parsed_news.url_pattern == '2011-04-17-519993'
