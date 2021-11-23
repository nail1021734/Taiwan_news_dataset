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
    url = r'https://www.epochtimes.com/b5/19/4/23/n11206720.htm'
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
            我代表追查迫害法輪功國際組織,來這裡紀念4.25這一偉大的日子,同時祝賀三億三千多萬
            中國同胞退出共產邪惡組織!人類歷史上1999年4月25日,是中國法輪功學員為追求真理、不
            畏強權的光輝見證! 20年後的三億三千多萬中國人退出共產邪惡組織,是中國民眾全面覺醒、
            解體共產邪靈的一個偉大的歷史豐碑! 20年前中國法輪功學員,懷著大善大忍之心上訪,也是
            給中共,包括高層決策者一次糾正錯誤,贖罪自新的機會。不幸的是,卻迎來了更加殘酷的迫害
            。 事實證明,中共是人類有史以來最邪惡的國家恐怖主義、超級犯罪集團,是人類的公敵。
            中共就是邪魔!是變異的魔鬼。不能對中共報任何幻想。解體中共,產除共產邪靈,是人類共同
            的責任!當人們真的了解了中共的邪惡,才能知道與共產邪靈同在一個星球上是多麼的危險!
            解體中共是多麼的重要。 一、對法輪功的迫害,是中共幾十年殺人歷史的延續 自中共成立
            以來,從來沒有停止過對中國人的殺戮。據估計,中國有一半以上的人曾受到過中共的迫害,
            大約6,000萬到8,000萬人非正常死亡。超過了兩次世界大戰死亡人數的總和。 這次對
            法輪功學員的迫害,是中共幾十年殺人歷史的延續。據明慧網不完整統計,至少有4287名有名
            有姓的法輪功學員被迫害致死。近4年來,每年都有大量的法輪功學員被中共當局構陷判刑,僅
            今年中國新年前後的3個月,就有227位法輪功學員被構陷判刑。 二、中共大量活摘法輪功
            學員器官國家犯罪還在繼續 2018年10月19日至12月2日,追查國際的調查員以四川省政法委
            維穩辦主任副主任的身份,為親屬聯繫器官移植手術的事由,對北京、天津、上海等11個省市
            涉嫌活摘法輪功學員器官的12所大醫院的院長、主任、醫生等責任人電話調查取證,獲得17個
            錄音證據。 調查結果再次顯示:中共現在仍舊在活摘法輪功學員器官進行移植。對“你們是還
            在用法輪功學員器官對吧?”的問題,有11名被調查者(涉及9家醫院)做了肯定回答:“對對對”
            、“對對,沒錯沒錯,你說的對”、“對,這肯定的”、“沒問題”、“你來了再說吧”,其它人的回答
            雖然含糊其辭,答非所問,但卻無一人矢口否認他們在用法輪功學員器官。 三、中共也危害著
            全世界,清除共產邪靈是人類共同的責任 中共不僅迫害中國人,也禍及全世界。通過共產意識
            滲透、謊言洗腦,經濟貿易侵略等,把災難輸出到海外,清除共產邪靈是人類共同的責任。 我
            們呼籲全世界各國政府、組織和一切正義人士立即行動起來,充分認清共產邪靈的終極目的,
            全面追查和懲治中共的反人類罪惡!刻不容緩!這不僅僅是因為此等罪行必須懲處,更因為是
            拯救人類最後的道德良知!天地之間正與邪的較量,構成了對每個人、每個組織、每個國家政府
            道德良知的全面檢驗!願人們在這歷史關頭,選擇正義良知,共同清除邪惡! 我們告誡參與迫害
            法輪功的人們:中共正在解體,全面清算即將到來。迫害法輪功是群體滅絕罪、反人類罪!任何
            執行命令的托詞不能作為豁免的理由,所有參與者必須承擔個人責任。自首坦白、揭露黑幕、
            爭取立功贖罪,是唯一的出路! 追查迫查國際以如繼往,徹底追查迫害法輪功的一切罪行以及
            相關的機構、組織和個人,無論天涯海角,無論時日長短,必將追查到底,行天理,再現公道,
            匡扶人間正義。這就是我們對國際社會的承諾。我們永不放棄。
            '''
        ),
    )
    assert parsed_news.category == '美國,紐約生活網,紐約新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1555948800
    assert parsed_news.reporter is None
    assert parsed_news.title == '追查國際主席汪志遠:共產邪靈是人類的公敵'
    assert parsed_news.url_pattern == '19-4-23-11206720'
