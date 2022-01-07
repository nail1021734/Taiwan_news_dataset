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
    url = r'https://www.epochtimes.com/b5/13/7/21/n3921942.htm'
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
            當地時間7月20日下午16點,來自歐洲27個國家的法輪大法學員及多个人權組織代表聚集在
            丹麥首都哥本哈根市政廳廣場,舉行大型反迫害14週年的集會。要求解體中共,立即停止迫
            害法輪功,同時聲援一億四千萬中國民眾退出中共和相關組織。 歐洲法輪大法協會主席
            Manyan NG發言開啟集會序幕,隨後國際 「醫生反對強制摘取器官」組織成員李會戈(音)教授
            揭露中共「活摘法輪功學員器官」的殘忍暴行;西班牙律師卡洛斯.伊格雷西雅斯
            (Carlos Iglesia)介紹該國剛剛出爐的一項新法律,禁止本國公民去中國作器官移植的簽證;
            丹麥議員索倫‧艾斯普森(Søren Espersen)和托姆•本克(Tom Behnke)給歐洲
            法輪大法協會發來致詞表示支持與慰問。 丹麥議員:一直在關注法輪功學員被活摘
            器官 丹麥國會議員、人民黨副主席及國會外交政策委員會副主席索倫‧艾斯普森
            (Søren Espersen)發來聲援歐洲法輪大法學員的電文: 「因為個人的原因,今天我不能夠
            來到現場面對你們講話,但是不管怎樣,我很感謝你們給我這個機會得以向你們寄出這封
            信件。在此我向歐洲法輪大法協會致以熱烈的問候。同時,希望你們的聚會以及遊行圓滿
            成功!在中國以外以及在中國本國內的法輪大法學員是勇敢而值得尊敬的人們,他們理應
            得到支持, 並使他們所有的人知道,當他們強烈要求一個沒有共產黨專制的中國時,我們在
            自由世界裡的人,與他們在一起分享他們的願望, 讓偉大的中國人民因而能使他們天然的
            國度屹立於世界文明而民主的國家之中。」 之前,索倫•艾斯普森(Søren Espersen)
            曾經表示過,他一直在關注法輪大法學員被活摘器官這件
            事情,他曾在幾年前美國的《國際先驅論壇報》上看到過相關文章,難以想像世界上竟然還
            有如此的罪惡存在。艾斯普森先生認為:「我相信有了這麼多的證據,這種活體摘取器官的
            事情一定是真實的,那麼中共當局犯的就是國際人權罪行。」 「丹麥的另一位國會議員托
            姆·本克也向與會者发來了致意:“我以最美好的希望祝願大家遊行與聚會圓滿成功!」 李會
            革博士揭露中共摘取器官的罪惡 國際醫生反對強制摘取器官組織(DAFOH)成員李慧戈(音)
            醫學博士曾經向二十多位英國各政黨派的議員、議員代表、外交部、內政部部門的代表介
            紹了中共政權系統屠殺摘取器官的罪惡。 李慧戈先生在會上提出為甚麼在中國會發生這樣
            的罪惡。他表示,中共建政以來,發起各種運動殘酷對待社會各類人群。先是地主,然後是資
            本家,再是右派。文革時人人自危,「六‧四」屠殺學生,現在是殘酷鎮壓法輪功。中共政權
            對生命的漠然震驚世界,使整個社會道德崩潰。為了強徵土地,可以把帶頭反抗的人碾死,殺
            一儆百;18個人路過躺在血泊中的孩子卻視而不見,人心盡喪。 出逃芬蘭 朱洛新呼籲西方
            社會幫助停止迫害 朱洛新一年前剛從中國大陸逃出來,與在芬蘭的丈夫團聚。她從1994年
            開始修煉法輪功,煉功使她當時所患皮膚絕症紅斑狼瘡痊癒。1999年迫害開始,她多次到北
            京為法輪功上訪,試圖用親身經歷向政府說明法輪功對百姓健康和社會都有無限好處,但也
            正因為如此她被多次關押。 2001年冬天,她在家鄉被便衣跟蹤逮捕,這一次警察連續14天24
            小時不分晝夜的審訊,不讓睡覺。後來被不合法的判了10年監獄徒刑。在這期間獄警曾用
            30-40斤的腳鐐把她釘在牢房的地上14天,當她再卸下腳鐐時已不能走路。2003年朱洛新從韶
            關監獄轉押到廣東省女子監獄,受到更殘酷地迫害。例如在冬天零下2-3度的時候,只穿一件
            襯衣,被關在一個2-3平米的禁閉倉裡40天,如此等等。 朱洛新在集會上發言說:「我和我家
            的經歷是中國千百萬法輪功家庭的一個縮影。我和我丈夫分離多年後畢竟還重逢了,我今天
            還能幸運地站在這裡,但是有多少中國大陸的法輪功學員們,他們或者被迫害得家破人亡,或
            者正在經歷著同樣得遭遇,他們沒有機會站在這裡講話,所以,今天我在這裡,想要代表他們
            呼籲西方社會,請你們做一切可能做的事情,幫助立即停止這場人類歷史上最黑暗的
            迫害。 丹麥人權青年協會代表:每人一小點行動改變迫害發生 阿隆‧ 穆勒 ‧漢森
            (Aron Møller-Hansen )來自丹麥人權青年協會,他在會上發言稱:「我代表我們協會對
            今天的這個反迫害集會表示支持,對正在中國發生的人權迫害表示譴責。」 「歷史告訴
            我們,有些人可以非常殘酷的去對待另一群人,中國正在發生的「迫害法輪功」就是其中一個
            典型例子。在世界其他各個國家和角落,人權組織都評估法輪功學員是一群
            平和的人。」 「每個人與生俱來就應擁有自由和人權。今天,我們在這裡想喚醒人們關注對
            正在中國發生的對法輪功迫害的這個嚴酷事實。歷史也曾告訴我們,每一個人的行動都可以
            改變一點我們生存的這個世界,我希望我們的行動也在改變「迫害法輪功」在中國的持續發生。」
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1374336000
    assert parsed_news.reporter == '哥本哈根,林銳'
    assert parsed_news.title == '歐洲7.20反迫害14週年集會 聚焦中共活摘暴行'
    assert parsed_news.url_pattern == '13-7-21-3921942'
