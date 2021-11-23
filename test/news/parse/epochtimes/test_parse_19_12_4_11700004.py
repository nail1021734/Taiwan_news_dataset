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
    url = r'https://www.epochtimes.com/b5/19/12/4/n11700004.htm'
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
            面對越來越多的美國大學申請者,在大學申請的激烈競爭中,如何讓自己
            脫穎而出?專家建議,學生應列出目標學校的簡短清單,表現出對所選學校的興趣,率先搜索
            相關信息,並做真實的自己。 對學習的熱情和積極主動,以及對申請的學校有濃厚的興趣,
            這些是學生能否進入大學的關鍵。但在日益競爭激烈的環境下,這只是大學看重申請者的一部
            分。 國際學生增加 錄取率降低 根據美國新聞與世界報導,全國大學招生諮詢協會(Nati
            onal Association for College Admission Counseling)2018年的一份報告顯示
            ,如今大學正在收到更多的申請。根據該報告,從2016年秋季到2017年秋季,學校的新生申請
            數量增加了4%,潛在轉學生的申請增加了3%,潛在國際學生的申請增加了8%。 最重要的是,
            這些趨勢對接受率產生了影響。例如,在哈佛大學和斯坦福大學,2017年秋季錄取率不到5%,
            而其它高選擇性大學的錄取率也低於10%。 根據美國新聞(U.S. News),從排名靠前的1,2
            68所學校蒐集的數據顯示,在2017年秋季,平均下來,大學的接受率為66%。 丹佛的Grea
            t College Advice的創始人兼首席執行官Mark Montgomery表示:「對於大多數孩子
            來說,只要做正確的事就不難上大學。」至於什麼是正確的事?美國新聞訪問了獨立的大學
            顧問,和高中指導顧問,找出大學申請者可以通過以下6種方式脫穎而出: 制定學校名單 考慮
            早期決定 表現出對大學的興趣 注意細節 率先做事 要真實 1. 制定學校名單 挑選大學
            需要長時間的了解自己,以及研究這些學校的網站。休斯頓的教育顧問朱迪・繆爾(Judy M
            uir)建議,學生要評估自己是誰?擅長做什麼?之後,考慮你的學習方式和其它偏好,以便與
            找到相匹配的大學。 在波士頓和華盛頓特區設有辦事處的Green Apple College Guid
            ance&Education的所有者兼首席顧問凱利・弗雷澤(Kelly Fraser)說,時間安排很重要
            ,學生應在高中低年級就準備一個簡短的大學清單。因為學生在之後會有標準化考試,然後
            知道他們的高中GPA處於哪個水平,並且簡歷上可能會有一些AP課程。 紐約教育諮詢公司
            IvyWise的首席大學顧問Christine Chu鼓勵學生,選出多達15所大學,並將它們平均分為
            三類:可以去的大學、目標大學和高錄取率的大學(對於那些首要選擇沒成功的學生)。她補充
            說,如果學生們已經對他們的選擇進行了充分的研究,這也許是沒有必要的。但她警告,清單中
            不能很多都是低錄取率的學校。 2. 考慮早期決定 越來越多的大學也通過早期決策過程招收
            學生。根據NACAC,21%的大學提供早期決策計畫。在2016年秋季至2017年秋季之間,大學
            報告稱,被錄取的早期決策申請人數量平均增加了5%。早做出決定具有約束力,意味著如果
            學生被接受,就要去那所大學。 專家說,選擇早期決定的學生應該確信該大學是適合他們的,
            尤其是涉及到經濟援助,因為接受具有約束力的早期決策錄取,意味著學生將無法比較學校
            之間的援助方案。 Chu表示:提早作出有約束力的承諾,一個最大的缺點是,學生只會收到
            一份經濟援助計畫。如果學生想考慮它們提供的最佳經濟援助,則早期決定可能不是最佳的
            選擇。 但是有約束力的協議還有一些迴旋餘地。弗雷澤(Fraser)表示,該協議基於榮譽準則
            (Honor Code),通常不具有法律約束力。不過她也指出,有些學校共享早期決策申請人的
            名單,這意味著如果一個學生接受了多個大學的早期決策,這很可能會被發現。
            '''
        ),
    )
    assert parsed_news.category == '美國,舊金山,生活嚮導,教育,學生園地'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1575388800
    assert parsed_news.reporter == '艾薇'
    assert parsed_news.title == '美國大學尋找的人才:6種脫穎而出的方法'
    assert parsed_news.url_pattern == '19-12-4-11700004'
