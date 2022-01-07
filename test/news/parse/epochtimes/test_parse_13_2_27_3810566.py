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
    url = r'https://www.epochtimes.com/b5/13/2/27/n3810566.htm'
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
            德國前教育部長沙萬因論文抄襲被取消博士頭銜後,日前已正式辭職卸任,當然她並沒有承
            認自己有抄襲行為,而是準備對她曾經就讀的杜塞爾多夫大學提起訴訟,然而無論訴訟結果
            如何,沙萬的政治生涯已經到此結束。兩年前,針對當時國防部長古籐貝格的論文抄襲事件,
            沙萬曾說,「人不會因為是博士就當部長,而是因為其在政界的能力」,可惜她自己也沒能因
            為出色的政治能力而保住其政治前途。不過沙萬的這句話倒是沒錯,在德國聯邦內閣的14位
            成員中,的確並非人人都是博士,不僅如此,有的部長乾脆連高中文憑都沒有,但是他們依然
            因為自己的政治能力而「在其位並謀其政」,看來在德國這種有「政治潔癖」的國家,要麼
            就老老實實拿個貨真價實的博士,要麼就兢兢業業幹好本職工作,兩種方式都有機會在政界
            出人頭地,但是投機取巧者卻隨時都有可能被打回原形。 德國16位內閣成員中有10位是博
            士,下面就具體曬曬他們的文憑。 總理默克爾:政界、學術界通吃 德國總理默克爾不僅是
            政界鐵娘子,在學術界也不落人後,她有一長串的學術頭銜,除了自己正式攻讀的物理學博士
            外,還有世界各地大學授予的9個榮譽博士頭銜,當然這些榮譽博士的名號跟學術無關,而是
            來自於她的政界成就,例如她因為「促進社會和平和環保」,而被韓國首爾梨花女子大學
            (Frauenuniversität Ewha in Seoul)授予榮譽博士;因其對歐洲的貢獻,而成為羅馬尼亞巴比
            甚-博雅伊大學(Babes-Bolyai-Universität)的榮譽博士等。 外交部長韋斯特韋勒:法學博
            士 德國外交部長韋斯特韋勒(Guido Westerwelle)被稱為「務實博士」,他能在同一時間完
            成多項事務。1980-1987年他在波恩大學完成法學學業後,分別於1987和1991年完成兩次國
            家法律考試,1994年他獲得哈根遠程大學(FernUniversität Hagen)的博士學位。與此同時
            他積極從政,先後成為青年自由團(Jungen Liberalen)負責人和自民黨(FDP)總秘書,並寫有
            《黨派權利和青年政治組織》一書,2009年他成為德國外長。他也有榮譽博士頭銜,2008年
            他因增強自由與參與權,成為韓國首爾漢陽大學的榮譽博士。 經濟部長羅斯勒:
            醫學博士 經濟部長羅斯勒(Philipp Rösler)是德國政界高層唯一的亞洲面孔,2002年他
            獲得漢諾威醫學院博士學位,所關注的領域是心臟手術後心律失常問題。1999年他開始在
            漢堡的聯邦空軍護校任職,2003年他在聯邦空軍內擔任眼科職業醫師,並開始專注於
            下薩克森州的政治。2009年他任職聯邦健康部長,成為德國最年輕的部長之一,2011年出任
            經濟部長。他也有「美麗」的榮譽博士頭銜,去年他成為越南河內國家經濟大學的榮譽
            博士。 國防部長德梅齊埃:唯一的榮譽教授 國防部長德梅齊埃
            (Thomas De Maiziere) 也是法學博士,1986年他在明斯特的威廉大學
            (Wilhelms-Universität)獲得博士學位,其論文是關於聯邦卡特爾局的研究。他雖然沒有
            榮譽博士頭銜,但卻是內閣中唯一一個曾擔任榮譽教授的成員,2010年他曾在德累斯頓工業
            大學教授國家法。他雖然在1982年通過了第二次國家法律考試,但卻從未做過律師,而是
            直接選擇從政。 財政部長朔伊布勒:法學博士 德國財政部長朔伊布勒(Wolfgang Sch
            äuble)也是一名法學博士,他於1971年在弗萊堡取得博士學位。他在政界擔任過很多職務,
            當過總理辦公廳主任、內政部長、聯盟黨團幹事長、聯盟黨團主席、基民盟主席等,2009年
            起任德國聯邦財政部長一職。他也有圖賓根大學授予的榮譽博士頭銜。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361894400
    assert parsed_news.reporter == '王亦笑德國,余平'
    assert parsed_news.title == '從技工到博士 曬曬德國政客都是啥文憑'
    assert parsed_news.url_pattern == '13-2-27-3810566'
