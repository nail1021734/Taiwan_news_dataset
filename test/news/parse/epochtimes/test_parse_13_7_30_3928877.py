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
    url = r'https://www.epochtimes.com/b5/13/7/30/n3928877.htm'
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
            《星期日泰晤士報》的報道指出,英國一名安全情報學術機構的教授被告知,不能在一項有
            來自中國安全部門官員參與的座談會上提出人權議題之後,已拒絕出席這項座談會。 據《
            星期日泰晤士報》星期日的報道,這是一個具教育性質的慈善機構「商業和公眾領域道德中
            心」所舉辦的研討會,預計會有24名來自中國公安部的官員代表團到英國劍橋大學的三一堂
            學院參與這項研討會,不過組織座談會的機構和劍橋大學無關。 英國白金漢大學的安全情
            報研究中心的主任葛利茲教授受邀演講,但是組織會議的機構向葛利茲教授表示座談會不可
            以提出人權的議題,葛利茲教授原先同意出席演講,但是現在已經拒絕出席。 他在《星期日
            泰晤士報》表示,他和其他學術界人士一樣,也非常樂意對任何方面講述英國情報界成功的
            方式。但是他指出,如果不顧道德的告訴這些秘密警察是非常令人憤怒的事情,他說必須讓
            他們知道他們在中國和西藏所做的事是對人權的侵犯,以及對中國網民進行的大量
            監控。 研討會的主辦人否認到英國參加座談會的中國代表是秘密警察,但是《星期日
            泰晤士報》表示,負責人也不願解釋為什麼座談會不允許學術界提出人權問題。 《星期日
            泰晤士報》在報道中表示,這一批到英國的中國官員並不是尋常的和犯罪事務有關的
            官員。其中包括來自單位和被指稱攻擊西方的軍方網絡軍事基地61398單位一起的官員,也有
            一名電腦界的管理人士,他的企業負責遼寧省安全部門提供電腦訊息管理,在和朝鮮接壤的
            邊界。此外代表團也有兩名來自新疆的資深安全官員,報道說在新疆當局經常進行大幅逮捕
            異議維族人士。 英國前軍事情報官保守黨議員沃裡斯也表示,像這樣的座談會必須非常的
            謹慎。薩利大學的網絡安全教授伍沃德也警告指出,這樣的座談會將讓參與者對英國情報安全
            工作有相當大的瞭解。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1375113600
    assert parsed_news.reporter == '辛民'
    assert parsed_news.title == '研討會設禁區 英教授拒出席指中共侵犯人權'
    assert parsed_news.url_pattern == '13-7-30-3928877'
