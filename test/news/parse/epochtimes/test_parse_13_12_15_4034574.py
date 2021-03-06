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
    url = r'https://www.epochtimes.com/b5/13/12/15/n4034574.htm'
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
            執政的為泰黨積極推動總括式特赦案,目的之一是為流亡海外的前總理戴克辛解套。然而特
            赦案不僅在野黨反對,連支持執政黨與戴克辛的紅衫軍也不領情。 泰國前總理戴克辛2006
            年9月19日軍事政變後流亡海外,2008年2月28日返國為自己遭受的指控辯白,他走出機場後
            跪拜土地並磕頭的身影,在他同一年8月出席北京奧運並再度流亡之後,許多泰國人可能已不
            太記得。 然而,執政的為泰黨(Pheu Thai Party)10月積極推動總括式特赦案,戴克辛的返
            國之路彷彿將讓部分泰國人的夢魘成真。 特赦案「人人有獎」 執政黨兩面不討好 為泰黨
            提出的特赦案經下議院修改通過,幾乎變成「人人有獎」的特赦案,涵蓋範圍從2004年1月1
            日到2013年8月8日期間,因政治罪行遭起訴的人可望獲得特赦,包括在2010年紅衫軍示威期
            間的抗議領袖、軍人,以及下令鎮壓紅衫軍的執政者。(編註:泰國紅衫軍「反獨裁民主聯合
            陣線」(UDD),支持前總理戴克辛。在2010年民主黨執政期間,紅衫軍認為政府有軍方介入,
            發起多次抗議活動,訴求解散國會下議院,重新進行大選,隨後時任總理艾比希下令軍方鎮壓
            ,造成80人以上死亡。) 民主黨黨主席艾比希2010年擔任總理期間,下令鎮壓紅衫軍造成許
            多傷亡,但為泰黨的特赦案,他不願買單。包括艾比希在內,反政府陣營認為,這個特赦案只
            不過是給戴克辛無罪返國的門票。 泰國最高法院2008年10月判處戴克辛兩年徒刑並扣押部
            分資產,罪名是他利用職權協助妻子以折扣價買地。 而這張以紅衫軍為民主奮鬥犧牲者的
            鮮血,為戴克辛換來的返國「門票」,部分紅衫軍也不買單。 2010年5月19日,紅衫軍遭鎮壓
            當天,最後離開現場的護士普莎蒂(Phusadee Ngamkham),以及當晚遭意外射殺身亡的25歲護
            士志工卡摩凱(Kamolkate)之母帕瑤(Payao Akkahad),都公開抨擊。 普莎蒂指控,「泰國已
            有多少次看到謀殺犯沒有因犯下的罪刑受罰?投票給為泰黨,希望他們不要再擁抱這已經腐
            敗的免罪制度,但他們現在卻為自己的利益向粉飾太平屈膝?」 盈拉暫時挺住反政府
            風波 民主黨10月底發動反特赦集會示威,獲得反戴克辛陣營包括雜衫軍、黃衫軍、白面具等
            團體支持,數萬人走上街頭吹著哨子,他們多半是曼谷的上班族、商人、學者,要求上議院駁回特
            赦案。 各界壓力迫使戴克辛的妹妹、現任總理盈拉與為泰黨多次喊話,上議院駁回特赦案
            後,他們不會再推動這項法案,希望平息眾怒。 上議院11月11日終於全數議員通過駁回特赦
            案,但集會示威已演變成「推翻盈拉政府」、「終結戴克辛政權」。這股反戴克辛的勢力又
            重新再聚集,從示威現場免費提供的伙食觀察,集會領袖蘇德彷彿得到有力人士的財力奧援
            。 蘇德是艾比希執政時的副總理,是鎮壓紅衫軍示威活動的重要決策者。為免拖累民主黨
            有任何被解散的風險,他辭掉議員,全力領軍反政府集會。 11月11日上議院駁回特赦案當天
            ,國際法庭正好宣判泰國與柬埔寨的邊界爭議案,國際法庭判定,兩國邊界的普里維希神廟周
            圍地區屬柬埔寨,泰軍警部隊必須撤離。 反政府陣營原本想藉由這樁判決借力使力,對執政
            黨施壓,但泰國政府堅持泰方未因判決失去領土,當地媒體也多以雙贏解讀,讓盈拉政府暫時
            挺過抗爭風波。 街頭示威拖長 不排除提早大選 雖然盈拉暫時度過反特赦示威,但反政府
            陣營已打算拉長戰線,複製過去黃衫軍、紅衫軍長期街頭抗爭、最終讓政府倒台的
            計策。 黃衫軍長期示威曾讓戴克辛或其支持的政府倒台,包括2006年9月政變、2008年12月
            為泰黨的前身人民力量黨,被憲法法庭判決在選舉中舞弊而遭解散,使得民主黨聯合過去挺戴克辛
            的其他小黨成功執政。 為了抗衡反政府示威,執政黨為泰黨修補與主流紅衫軍的關係,紅衫
            軍也發動支持者到曼谷集會,展示支持政府人氣與為泰黨提出的修憲案。 為泰黨提出的修
            憲案,要將上議院議員改為全部經由選舉產生,不再有部分指定名額,反對這項修憲案的民主
            黨則向憲法法庭上訴,認為這項修憲案違憲。11月20日憲法法庭宣判,修憲案違憲,但並不會
            因此解散為泰黨,或開除提出修憲案的為泰黨議員。 反政府陣營雖然接受判決,但表示會持
            續集會,要終結「戴克辛政權」。紅衫軍陣營則表示,反對當前憲法的立場不變,因為這部憲
            法是2006年的政變者所訂定的,紅衫軍會繼續要求為泰黨修改憲法。 修憲案宣判後,暫時緩
            和緊張的政治氣氛,不過,泰國社會的對立並未因此結束。 盈拉2011年8月大選上台,多項民
            粹政策備受批評,包括財政嚴重損失的大米典押計畫、汽車首購補助、治水計畫等,現在特
            赦案又鬧得滿城風雨。 泰國政治學者蒂提南(Thitinan Pongsudhirak)曾在「曼谷郵報」
            撰文指出,盈拉若能挺過這次反政府抗爭到明年8月任滿三年(到2015年任期屆滿),她可以考
            慮宣布解散國會、提早全國大選以示負責。 但迫於反政府的示威壓力,盈拉已於9日宣布解
            散國會,明年提前大選。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1387036800
    assert parsed_news.reporter is None
    assert parsed_news.title == '泰國特赦案 連紅衫軍都不挺'
    assert parsed_news.url_pattern == '13-12-15-4034574'
