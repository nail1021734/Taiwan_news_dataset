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
    url = r'https://www.ntdtv.com/b5/2011/03/30/a512271.html'
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
            本次利比亞動亂之初,中國企業大舉撤離,導致許多在建工程被迫中斷,3月25日,利比亞銀行
            卻向這些企業提出了提前歸還貸款以及巨額的索賠要求。據《二十一世紀經濟報導》的消息,
            目前,利比亞撒哈拉銀行已經向這些中國企業發出了“預付款保函索賠函”,對每家企業的
            索賠額度均達到了數億美元之多。 有業內人士表示,該銀行已經向葛洲壩集團、中國水利
            水電建設,以及宏福建工等中國公司提出了索賠要求,並且規定在5天之內必須給其以明確
            答复。 據台灣旺報的報導,這位人士拒絕透露索賠的具體金額,僅表示葛洲壩集團的索賠
            額度是目前這些被索賠企業中最高的,他還抱怨說,“預付款保函還有半年才到期呢,現在銀行
            就提前要求索賠,這完全是惡意索賠!”而北京宏福建工集團國際工程部副總經理廖麗英則透露,
            這次利比亞撒哈拉銀行向宏福建工的索賠額度約為4億美元。據悉,這些企業目前已經向
            中國商務部求助,希望利比亞的銀行能夠中止預付款保函。不過,有分析人士認為,即使銀行
            停止索賠,這些中國企業海外投資的信用記錄將有可能被抹黑,無論如何,這都是一件傷透
            腦筋的事情。 此外,利比亞項目中斷後,承包商從利比亞以外國家採購的原料費無法按期
            支付,加上很多工程採用的分包模式,也凸顯出三角債的問題。據統計,大陸在利比亞在建
            大型項目共50個,涉及合同總金額達188億美元,主要集中在基礎建設領域,以宏福建工、
            北京建工和中國建築3家公司的施工進度最快,都已超過30%;但施工進度愈快,損失也愈
            大。這些人士指出,“在撤僑後,我們最擔心的就是這個事情。對企業來說,等於是雪上加霜。
            ”中資企業主要在利比亞基建領域投資,對於這些基建承包商來說,在建項目未完成的合同
            金額越小,經濟損失就越大,亦即“幹得越多,損失越大”。 對此,有評論寫道,這些中資企業
            的投資損失包括穩定收益損失、合同餘款損失,以及當地儲蓄和固定資產損失等。留下的
            設備、房屋、車輛能否保全,已經簽訂的合同是否持續有效,均不得而知。中方如何挽回
            損失,尚在未定之天。如今中國有力量在世界各國投資,卻沒有力量保護這些投資,顯示中國
            政府應對地區動亂的能力不足,這是值得我們反思的。...... 從目前的情況看來,大多數
            中資企業在國外競標項目時,主要依靠以壓低成本的方式贏得合同,卻很少對相應的安全風險
            成本作出周全的評估。眾所周知,這些中資企業萬里迢迢去北非做生意,其宗旨無非是為了賺錢,
            至少也不能賠錢。可到頭來,不僅錢沒有賺到,卻飽嚐風險,甚至還要賠上大錢,這不是
            得不償失嗎?對此,有覌察人士注意到,這家銀行或許已經落入“叛軍”之手,否則的話,至今為止,
            中國官方宣傳機器一直在為困境之中的卡扎菲拼命搖旗吶喊,怎麼就連這點面子都不給啊
            '''
        ),
    )
    assert parsed_news.category == '國際專題,敘利亞局勢'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1301414400
    assert parsed_news.reporter is None
    assert parsed_news.title == '中國企業匆忙撤離 遭利比亞巨額索賠'
    assert parsed_news.url_pattern == '2011-03-30-512271'
