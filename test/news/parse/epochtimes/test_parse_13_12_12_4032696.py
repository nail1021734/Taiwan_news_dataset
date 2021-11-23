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
    url = r'https://www.epochtimes.com/b5/13/12/12/n4032696.htm'
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
            連日來,巴黎街頭矗立著一個被虐待、酷似芭比娃娃的高大的「芭比女工」模型。她身穿
            藍色工作服,口被黑膠布封住,四肢被捆綁著站在一個大包裝盒裡......聖誕節快到了,
            平時漂亮的「芭比娃娃」是法國人過聖誕節最受歡迎的一件禮物,但是很多人都不知道這些
            漂亮的娃娃是在中國由那些勞工在極其惡劣的工作條件下生產出來的。法國非政府組織「人民團
            結」和「中國勞工觀察組織」借人們在忙著準備聖誕禮物之際,在街頭和商業區用展示「芭比
            女工」的模型,提醒消費者要關注被虐待的中國勞工狀況。 抗議美國玩具公司 吁保護中國
            勞工權益 作為全球第一大玩具生產商,美國玩具公司美泰兒(Mattel)在世界各地擁有70
            家工廠,其中大部份生產商分佈在中國。 「人民團結」負責人芬妮‧威爾士
            (Fanny Gallois)公開表示:「芭比娃娃」是玩具中的一個象徵性標誌。在過去的50
            多年裡,「芭比娃娃」已成為西方國家許許多多小女孩的童年夥伴。相比起來,生產這些玩具
            的中國工人,他們的工作環境卻如「地獄」。她強調,本次抗議活動並非為了阻止人們
            購買芭比系列玩具,只是想讓消費者瞭解芭比玩具的來源和背景,一起行動向美泰兒
            提出抗議,讓那裏的工人獲得正當的工作待遇。以美泰兒的影響力,那可以影響整個
            玩具行業。 要知道,美泰兒每分鐘就有152個芭比玩具在全球出售。據統計,該集團在
            2012年的營業額高達47億歐元,以5.65億歐元的純利潤,打破公司歷史性記錄。 中國勞工
            待遇違反《勞動法》18項條例 在今年的4月份至9月份期間,「人民團結」和「中國勞工
            觀察組織」專門派人深入美泰兒在中國的6家生產廠進行調查。調查人員以員工的身份,親身
            體驗工廠工人的工作條件與待遇。 10月份,這兩個民間組織作出了一份長達58頁的報告。
            報告指出,在美泰兒的工廠裡,80%的工人為女性,得到的待遇違反18項《勞動法》條例,
            例如:工人們一週7天無休息,而且每天工作13小時,超時工作亦沒有工資補償,生產使用
            化學用品沒有安全保護,沒有退休金待遇,拒絕員工休產假等等。 12月10日,「中國勞工
            觀察組織」創辦人李強參加了在巴黎舉行的「芭比女工」抗議活動。他向法國媒體講述了
            自己曾在中國大陸工廠工作的經歷,肯定該調查報告的結果是真實的。 該報告還舉
            例子說,用一個在市場上賣15歐元的芭比娃娃來計算,勞工得到的報酬僅為0.12歐元。而
            在過去的15年裡,為美泰兒工作的中國勞工的工作條件沒有得到任何改善。 「芭比女工」
            將走遍法國 除了巴黎,「人民團結」和「中國勞工觀察組織」還將在本週內,帶「芭比女工」
            到法國其它大城市如雷恩、里昂、馬賽、南錫等地展示抗議。 與此同時,他們還通過網絡
            社區發起「解放芭比女工」徵簽活動,目前已有6萬1千網民簽名支持。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386777600
    assert parsed_news.reporter == '張妮法國,德龍'
    assert parsed_news.title == '漂亮「芭比」被虐待 法國民間組織關注中國勞工前途'
    assert parsed_news.url_pattern == '13-12-12-4032696'
