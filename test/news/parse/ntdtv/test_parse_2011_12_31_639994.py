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
    url = r'https://www.ntdtv.com/b5/2011/12/31/a639994.html'
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
            美國積極重返亞洲,抑制中國大陸海上力量擴張,菲律賓基於地理位置及國力現況,成為美國
            的重要切入點及戰略棋子,可以預見,2012年美菲互動會更加頻繁,特別是在軍事領域。 地理
            關係所致,菲律賓與中國大陸有著深遠的歷史淵源,許多菲律賓人包括總統艾奎諾三世在內,
            也有華人血統,但是再悠久的淵源、再濃郁的血緣,只要碰觸到主權爭議,就得先擺到
            一邊。 2011年6月,菲律賓總統艾奎諾三世親上火線,向媒體聲稱中國大陸船艦、戰機自2月
            以來,侵入南海菲國領域6次至7次,其中1次中國戰艦還向菲律賓漁船開火。 自此,菲律賓與
            中國大陸之間因南海主權爭議而起的摩擦逐日加劇,菲方多次提出抗議,並譴責中國大陸
            違反「東協-中國南海行為準則」,破壞地區和平。 軍事分析家推斷,中國大陸船艦、戰機
            侵入南海的情況由來已久,只是菲律賓因國防力量薄弱,鞭長莫及,只好抱著睜一隻眼閉一隻眼
            的態度,但是2011年適逢美國意欲「重返亞洲」,立即抓住機會高調處理爭議,以便從中獲取
            利益。 911恐怖攻擊後,美國忙於中東及中亞戰場,難以兼顧亞太事務,而這段期間中國大陸
            在區內的影響力急速上升,成為週邊國家在貿易及其他領域的重要合作夥伴,使美國心生警覺,
            意識到重返亞洲和「平衡地區力量」的必要性。 菲律賓做為中國大陸近鄰,和越南等國
            扼守中國大陸南向出海口,戰略地位一躍而升,成為中國大陸及美國都要拉攏的對象。2011年
            中國大陸就對菲律賓提供180萬美元的軍事及執法援助,雖然金額和美國、澳洲所提供的援助
            相去甚遠,但對美國軍事盟友提供軍事援助,這個動作的涵義不言而喻。 在南海主權爭議上,
            菲陸雙方雖然「相互諒解」,但也「各持己見」,菲律賓國力薄弱,只好轉向簽有相互防禦協定
            的美國求助,而美國也十分慷慨地伸出援手,包括移交1艘「韓密爾頓級」巡邏艦。菲方已將
            這艘軍艦派往南海服役,雖然對實際防禦力量助益不大,但象徵性的意義十分明確。 基於
            相互利益,菲美一拍即合,利用南海主權爭議,菲律賓可以在美國的支持下提升國防力量,而
            美國也能以菲律賓為據點,配合日本等其他盟友,監控或抑制中國大陸海上力量的擴張。 菲律賓
            外交部在長達13頁的2011年終成果報告中說,菲律賓「將強化與美國的堅固國防夥伴關係,
            且與中國、印度、日本等其他地區夥伴,諸如南韓、澳洲、新西蘭和印尼等交往,進行互惠的
            保安及防禦對話」。 報告也提到,華盛頓2011年為馬尼拉提供了5300萬美元,做為架設海岸
            監控雷達系統之用,此外,奧巴馬政府承諾為菲律賓提供的建議撥款,更自2011年的1億2327萬
            美元增至2012年的1億4466萬美元,增幅達17%。 這顯示出菲律賓的外交政策雖是與週邊
            國家廣結善緣,但也凸顯出美國才是菲律賓在2012年主要依賴的對象,特別是在國防
            事務上。 菲律賓外交部長羅沙里歐(Albert del Rosario)日前向媒體透露,他和國防部長
            2012年首季訪問美國時,會與美方對等官員討論地區安全議題。他並宣布,美國提供的第2艘
            「韓密爾頓級」巡邏艦即將到來,同時美國正考慮為菲律賓提供12架F-16戰機。 假如美國的
            承諾全都兌現,以菲律賓目前的財政實力與軍事技術,怎麼養得起這些相對先進的武器?美國
            曾在菲律賓呂宋島中部的克拉克區和蘇比克灣設有空軍及海軍基地,直到1991年及1992年才
            極不情願地先後撤離,觀察家認為,美國這次只是假援助之名,恢復在菲律賓的軍事基地。 不管
            事實是否如此,可以確定的是,菲律賓與美國之間的軍事互動將更加頻繁,在地區安全事務的
            參與上也會愈來愈積極。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1325260800
    assert parsed_news.reporter is None
    assert parsed_news.title == '美重返亞洲 菲成戰略棋'
    assert parsed_news.url_pattern == '2011-12-31-639994'
