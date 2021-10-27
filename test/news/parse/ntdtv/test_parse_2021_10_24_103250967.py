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
    url = r'https://www.ntdtv.com/b5/2021/10/24/a103250967.html'
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
            面對俄羅斯核威脅的快速升級,北約盟國正在加快發展應對措施。美軍已開始積極開展戰術
            核武器在歐洲國家的部署,並得到北約同盟國的積極配合。 10月20日,俄羅斯國防部長
            謝爾蓋.紹伊古(Sergey Shoygu)在俄羅斯和白俄羅斯國防聯席會上說:「美國在北約
            同盟國的全力支持下,已經加緊了對歐洲的戰術核武器和儲存基地的現代化工作。」他透露,
            北約無核成員國的飛行員參與了練習使用戰術核武器的演習。 同一天,北約祕書長
            延斯.斯托爾滕貝格(Jens Stoltenberg)在新聞發布會上介紹了本週北約國防部長會議
            議程。部長們將就加強集體防務安全做出決定,並為明年6月在馬德里舉行的北約峰會做出
            準備。 斯托爾滕貝格認為,北約還應該加強應對俄羅斯核導彈的威脅。俄羅斯、中共及北韓
            等國都擁有核武器,而北約卻沒有。這個世界不會更安全。北約要的是一個沒有核武器的
            世界。 2018年,北約盟國確認俄羅斯開發和部署了中程導彈,這等於撕毀《中導條約》
            條約。從那時起,俄羅斯進一步增加了其導彈庫,並開發高超音速系統。這些導彈對歐洲、
            大西洋地區的安全構成了真正的威脅。 北約同盟國的防長們將召開核規劃會議,就如何保持
            北約核威懾力量的安全性、可靠性和有效性進行磋商,同時繼續致力於軍備
            控制。斯托爾滕貝格說,我們不會照搬俄羅斯的行動。但我們將保持強有力的威懾和
            防禦。 斯托爾滕貝格還表示,北約將採取措施保持聯盟的技術優勢,並評估進一步加強北約
            威懾和防禦的途徑。還將商定北約有史以來第一個人工智能戰略,在數據分析、圖像和
            網絡防禦等領域進行整合,並根據國際法,制定安全和負責任的使用原則。 斯托爾滕貝格
            表示,俄羅斯宣布關閉其駐北約代表團及北約在莫斯科的辦事處,他對此感到遺憾,因為這
            不能促進對話和相互理解。但北約的政策是一貫的:保持開放態度。 10月18日,莫斯科
            宣布將暫時關閉其駐北約使團,並要求北約組織關閉駐莫斯科辦事處。外界視為這是俄羅斯
            對北約驅逐俄羅斯駐北約布魯塞爾總部使團外交官做出的報復。 本月早些時候,北約表示
            在俄羅斯駐北約布魯塞爾總部使團工作的8名俄羅斯人是間諜並撤銷了他們的常駐資格。北約
            還把駐莫斯科辦事處的人員從20人減少到了10人。自從俄羅斯2014年吞併克里米亞以來,
            北約與俄羅斯的關係開始變得緊張。
            '''
        ),
    )
    assert parsed_news.category == '軍事觀察'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1635004800
    assert parsed_news.reporter is None
    assert parsed_news.title == '北約積極應對俄羅斯核威脅'
    assert parsed_news.url_pattern == '2021-10-24-103250967'
