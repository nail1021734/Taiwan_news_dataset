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
    url = r'https://www.epochtimes.com/b5/13/2/27/n3810705.htm'
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
            自從德國政界刮起強勁的「學歷打假風」,先後好幾員政壇大將已經倒在「抄襲門」上,那
            麼在德國內閣中還有多少人擁有高學歷? 內政部長弗裡德裡希:法學博士 弗裡德裡希
            (Hans-Peter Friedrich)是德國政界高層的又一名法學博士,分別於1983和1986年通過兩次國家
            考試,並於1988年在奧格斯堡大學獲得博士學位。他於2011年成為德國內政部長。 勞工部
            長馮德萊恩:醫學博士 馮德萊恩(Ursula von der Leyen)曾先後在哥廷根大學和倫敦政經
            學院學習經濟學,後來又在漢諾威醫學院攻讀醫學,並於1987年通過國家考試取得從醫資格,
            1991年獲得醫學博士學位。馮德萊恩是7個孩子的母親,2005年成為聯邦家庭部長,2009年就
            任勞工部長。 交通部長拉姆紹爾:經濟學博士 拉姆紹爾(Peter Ramsauer)於1973年取得慕
            尼黑大學工商管理碩士學位,又於1980年通過磨坊廠技能考試。自1981年起,他在家族磨坊
            廠工作,並於1985年取得慕尼黑大學經濟學博士學位,2009年成為交通部長。 家庭部長施羅
            德:社會學博士 今年剛剛36歲的施羅德(Kristina Schröder) 是內閣裡的年輕一代,她曾在
            美因茨大學學習社會學、歷史、哲學和政治學,2009年獲得社會學博士學位。攻讀學位期間
            她也積極活躍在政治舞台,並於2009年接替馮德萊恩成為聯邦家庭部長。 教育部長萬卡:數
            學博士 約翰娜•萬卡(Johanna Wanka)曾在萊比錫大學學習數學專業, 1974年取得碩士學位
            後,她去洛伊納-梅澤堡應用技術大學做了學術助理,並於1980年獲得博士學位。2010年萬卡
            出任下薩克森州科學與文化部長,直至今年2月接替沙萬,成為聯邦教育部長。 司法部長施
            納倫貝格:法律碩士 施納倫貝格(Sabine Leutheusser-Schnarrenberger)是一位很有經驗
            的律師,她先後在哥廷根和比勒菲爾德攻讀法學,並於1970年取得碩士學位,隨後通過了兩次
            國家考試。1992年-1997年她曾任職過聯邦司法部長,2009年再次出任司法部長。 衛生部長
            巴爾:工商管理碩士 衛生部長巴爾(Daniel Bahr)也非常年輕,今年37歲。他曾在明斯特大
            學攻讀經濟學,2008年取得工商管理碩士學位(MBA),2009年成為聯邦衛生部長的議會秘書,
            2011年接替羅斯勒成為聯邦衛生部長。 環境部長阿爾特邁爾:法學碩士 阿爾特邁爾
            (Peter Altmaier)於1980年在薩爾州大學取得法學碩士學位後,也通過了兩次國家考試。
            但是他的強項是外語,他能流利地說英語、法語和荷蘭語。去年5月,他剛剛晉陞為聯邦環境
            部長。 發展部長尼貝爾:管理學碩士 尼貝爾(Dirk Niebel) 可謂經歷豐富,他去以色列做過志願者
            ,並當兵多年。1990年他在聯邦應用技術大學學習公共管理學,並於1993年獲得管理學碩士
            學位。1998年他進入聯邦議會,2009年成為聯邦發展援助部長。 總理府部長波法拉:社會教
            育學碩士 波法拉(Ronald Pofalla)於1981年取得杜塞爾多夫應用技術大學社會教育學碩士
            學位後,又繼續在科隆大學攻讀法學,隨後也通過了兩次國家考試,成為一名律師。1990年他
            進入聯邦議會,2009年就任總理府部長。 消費者保護部長艾格納:電氣技師 消費者保護部
            長艾格納(Ilse Aigner)並沒有大學學位,職業中學畢業後,她參加了無線電與電視技工培訓
            。1988年又進修了電氣技術專業,後來成為一名電氣技師。1994年後她積極從政,並於2008
            年成為消費者保護部長。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361894400
    assert parsed_news.reporter == '王亦笑德國,余平'
    assert parsed_news.title == '從技工到博士 曬曬德國政客都是啥文憑'
    assert parsed_news.url_pattern == '13-2-27-3810705'
