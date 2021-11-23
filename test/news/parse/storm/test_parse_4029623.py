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
    url = r'https://www.storm.mg/article/4029623?mode=whole'
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
            總統盃黑客松今年邁入第四屆,開跑之初就遇到疫情升溫。作為政府和公民的重要協作平台,
            團隊彈性應變、調整參賽方式:第一次工作坊採用全遠端,第二次工作坊則運用「共享實境
            (Shared Reality)」概念舉辦,不因疫情而中斷。 縱使現在疫情趨緩,但在我看來,
            這段虛實整合的體驗和成果,仍然值得大家參考。 第一、第二屆的總統盃黑客松工作坊,
            都是沿用傳統黑客松的流程,所有人聚集起來,在同一個實體地點分組發想和討論,評審則在
            固定時間聽取各組簡報、提供各組成員諮詢。2020 全球疫情爆發後,第三屆將每個團隊分別
            安排在獨立空間,與評審的簡報諮詢也改為視訊舉辦。 去年的經驗讓我們發現:全線上的
            做法,雖然可以有效降低接觸、確保防疫成效,卻難以點燃實體交流激盪出的火花。固定時間
            的參與和連線品質,所形成的限制並不下於實體場域;而傳統的全實體作法,不僅有防疫上的
            顧慮,更有諸如各桌聲音互相干擾、展示簡報時可能看不清楚等等物理限制。 有鑑於此,
            今年在「g0v 揪松團」協助下,我們採取混合模式,除了實體空間進行的簡報和討論,團隊
            也在線上平台 Gather Town 開設了黑客松專屬大廳,評審和團隊都有虛擬分身。團隊在
            實體討論時如果需要補充,或找不在此地的專家討論,可以隨時揪團上線;在虛擬空間中討論到
            一個階段、想要展示初步成果時,也可以隨時實體集結在一起。 如此一來,今年各個團隊的
            問題分析果然更具深度,不只「解釋問題」,例如哪些開放資料欠缺整合,更能「解決問題」,
            協力找出使用者參與資料治理的具體方案。 總統盃黑客松的主軸,是透過公民社群的投入,
            面對既有的難題,激盪出新的創意,最終成為增進公共服務效能的具體方案。在我看來,這次
            的總統盃黑客松,除了參賽團隊的斐然成果,協作過程本身更是為了虛實整合工作模式,提出
            了開創的示範。 我認為「共享實境」真正的精神,是讓每個人都可以超越物理和時間的限制,
            結合虛擬和實體,創造出適合彼此的空間。唯有如此,我們才能充份體驗共同在場的感受,
            進而共創未來,成為自主又能互相連結的「多元宇宙(Multiverse)」。
            '''
        ),
    )
    assert parsed_news.category == '評論,國內,財經,專欄,科技'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1636033200
    assert parsed_news.reporter == '唐鳳'
    assert parsed_news.title == '唐鳳專欄:虛實整合,突破疫情限制'
    assert parsed_news.url_pattern == '4029623'