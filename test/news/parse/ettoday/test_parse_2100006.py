import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/2100006'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            台海情勢近來明顯緊張,美國國務院發言人普萊斯今天重申美國對台支持堅若磐石,會致力
            深化與台灣的關係。除一法、三公報加六項保證外,美國對台作法也會基於「台灣
            保證法」。 中國10月以來擴大共機擾台規模,1日至5日有高達150架次侵擾台灣防空識別區
            (ADIZ),引發國際高度關注。 美國國務院發言人普萊斯(Ned Price)今天召開媒體
            簡報會,會中記者詢問美國與台灣建立更緊密關係的步調,是否取決於北京對台侵略性
            作為。換句話說,中國加大對台恫嚇,是否會促使美國強化與台灣的關係。 普萊斯指出,
            美國一向清楚表明對台灣的支持是「堅若磐石」,且致力深化與台灣的關係。台灣是
            民主領頭羊,也是美國重要經濟與安全夥伴。 普萊斯表示,美國對台所有作法均以相關文件
            為基礎,包括去年12月上路的「台灣保證法」(Taiwan Assurance Act)。總統拜登
            (Joe Biden)政府已檢視對台交往準則,並在5月更新準則內容,以更好反映美國與
            台灣非官方關係的拓展與深化。 美國國會去年12月22日通過納入「台灣保證法案」的
            2021財政年度撥款法案,法案5天後獲時任總統川普(Donald Trump)簽署生效。台灣
            保證法呼籲美國政府對台軍售常態化、支持台灣有意義參與國際組織,並要求國務卿在
            法案生效180天內,檢視並重新公布對台交往準則。 時任國務卿蓬佩奧(Mike Pompeo)
            1月9日卸任前夕,取消所有美國政府對台政策自我施加的限制。拜登政府上任後重新檢視
            對台政策,4月9日公布新版對台交往準則,允許美國官員常態性在聯邦機構接待台灣官員,
            也能前往駐美代表處與台灣官員會晤。 據了解,在新準則下,美國官員也能出席雙橡園舉辦
            的活動,不過,包括像是雙十國慶等台灣重要節慶活動則不得參加。 普萊斯說,完成
            對台政策檢視後,拜登政府制定新準則,鼓勵美國政府官員以符合美台非官方關係的方式
            與台灣對口往來。自公布以來,新準則一直作為美國與台灣互動的規範。 他指出,拜登政府
            會持續美方長年作法,在各行政部門清楚說明該如何施行美國「一中政策」,也會以
            台灣關係法、美中三項聯合公報及對台六項保證做為指引,持續與台灣的非官方關係。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634091360
    assert parsed_news.reporter is None
    assert parsed_news.title == '台海愈趨緊張 美國務院重申「對台支持堅若磐石」深化與台關係'
    assert parsed_news.url_pattern == '2100006'
