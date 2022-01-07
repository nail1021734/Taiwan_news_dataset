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
    url = r'https://www.epochtimes.com/b5/19/4/22/n11205994.htm'
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
            在美國總統川普(特朗普)2016年競選期間擔任其專屬攝影師的金‧何(Gene Ho)說,川普
            善良、親切、尊重他人。 何先生的一本著作集結這段歷史未曾曝光的照片,通過他的鏡頭及
            敏銳的雙眼,使讀者看到川普一路走來,成為白宮主人的珍貴鏡頭。 華裔何先生意外獲聘為
            川普攝影師 身為中國移民第一代的何先生,2015年1月在一次茶黨(Tea Party)的活動中
            首次與川普相遇,他記得當時有意參選總統的本‧卡森(Ben Carson)和泰德‧克魯茲
            (Ted Cruz)也出席了那次活動。 同樣來自紐約的何先生在電話中告訴英文大紀元記者,
            他很欣賞川普,因此當天拍了很多他的照片,並在活動結束後將這些照片寄給川普競選團隊
            。 沒想到大約一個月後,何收到了川普親自簽名的手寫便條,說他很喜歡這些照片,並邀請
            何擔任他在南卡羅萊納州默特爾比奇市(Myrtle Beach, South Carolina)競選集會的
            攝影師。 何回憶說,那是一個只有大約50人參加的小型活動。活動結束時,他無意間得知兩天
            後川普在南卡州的另一個城市查爾斯頓(Charleston)也有一場活動,但是他並沒有被邀請
            參加。 不過,具有華人勤奮工作精神的何先生,決定去參加。活動當天,他在凌晨4點起床,
            穿上了正式的西裝,開車4個小時去參加活動。當天他太太很疑惑地問:「你要去工作的嗎?」
            他回答:「不是,但我必須這麼做。」 「我們在美國的華人不需要任何特別的待遇,我們只是
            希望能夠努力工作,因為我們相信,只有勤奮才有收穫。」何說。 在那天之後,川普正式聘請
            何先生擔任競選活動的攝影師。此後,何一直工作到2016年競選活動結束的最後一天。 何說
            ,他很讚賞美國的自由,鄙視社會主義和共產主義,因為他知道這些意識形態在實踐中會對人類
            帶來很大的破壞。 何先生眼中的川普:善良親切 與川普近距離接觸一年多,何先生看到了
            真實的川普,與主流媒體的報導完全相反。 「他非常善良、親切,而且尊重他人。」何說,
            「當他看到我的兒子時,一直稱讚:『太美了,太美了』。」 身為在紐約長大的少數族裔,
            何先生說他在成長過程曾經歷了許多歧視,特別是在1970年代。 「我對那些有種族歧視及
            偏見的人特別敏感,但是我很肯定,川普不是種族主義者。」何先生用堅定的語氣說道。 他說
            川普是「非常善良的人」,儘管有時候會因為希望事情能夠快速完成而顯得有些強硬。 他
            還說川普私底下和一般人沒有什麼兩樣,「喜歡吃麥當勞以及喝可樂」。 在他的著作《川普
            圖集:聖經原則如何為這位美國總統鋪平道路》(Trumpography: How Biblical Princ
            iples Paved the Way to the American Presidency)中,何先生分享了許多從未公
            開過的川普照片及其幕後故事,用耶穌12位門徒的故事以及他的鏡頭,分享他對川普的觀察
            。 何先生說,他喜歡川普的原因是,川普和中國人一樣勤勞,每天工作的時間很長,但是從來
            沒有顯現出疲憊不堪的樣子。 「我們在美國的華人努力工作,中國人不會偷懶,這就是我喜歡
            川普的原因。」他說,「我們不希望依靠政府福利,我們不會支持社會主義,我們摒棄社會主義
            。」 話鋒一轉,何先生對宣布角逐2020年民主黨總統提名的台灣移民第二代楊安澤(Andre
            w Yang)的主張表示不敢苟同。 楊安澤提出「全民基本收入」(Universal Basic Inco
            me)制度的想法,稱當選後會給18歲到64歲的美國公民,每人每月1,000美元的福利,以及採取
            社會信用評分制度。 「楊先生讓我們在美國的華人感到很尷尬,如果(楊)想要這樣做,他可以
            搬到中國去住。」何說,「我們希望的是宗教自由,我們不要政府給我們錢,也拒絕社會信用
            評分制度。」
            '''
        ),
    )
    assert parsed_news.category == '北美新聞,美國華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1555862400
    assert parsed_news.reporter == 'Nathan,Su'
    assert parsed_news.title == '用鏡頭捕捉川普 華裔攝影師:總統善良親切'
    assert parsed_news.url_pattern == '19-4-22-11205994'
