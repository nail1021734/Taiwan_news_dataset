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
    url = r'https://www.epochtimes.com/b5/13/12/30/n4046025.htm'
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
            據聯合國及國際化學武器監察組織最新消息,敘利亞可能無法完成在年底前銷毀其大部份
            化學武器的計劃。 《紐約時報》消息,根據美國和俄國在9月達成的協議,敘利亞需在
            2014年中前,銷毀其全部的化武。為完成這項時間表,敘利亞必須在今年底前銷毀500噸
            的化武,在明年2月底前再銷毀700噸化武。 聯合國官員說,從現階段看,將大部份化武運離敘利亞
            的工作不大可能在12月31日前完成。官員說,敘利亞的國內局勢持續動盪,加上後勤問題和天氣原
            因等,為運出化武的計劃帶來困難。 27日,來自美國、俄羅斯、中國、敘利亞、丹麥、挪威等國以
            及聯合國、禁止化學武器組織的專家在莫斯科會晤,討論銷毀敘利亞化學武器有關事宜。 俄羅斯
            外交部安全與裁軍問題司司長烏裡揚諾夫的說,多邊晤商順利進行,各方同意就從拉塔基亞向公海
            安全運送化學武器行動加強合作。 不過,烏裡揚諾夫也表示,從敘利亞化學武器存放處向拉塔基亞
            運送化學武器的行動尚未展開。此外,同安全運送有關的問題尚待解決。 根據禁止化學武器組織
            制定的敘利亞化學武器銷毀時間表,確定在敘境外銷毀的化學武器應於12月31日之前運出敘利亞。
            從目前看,這項工作進展滯緩。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388332800
    assert parsed_news.reporter == '柳芳'
    assert parsed_news.title == '年底前大量銷毀化武 敘利亞恐難達成'
    assert parsed_news.url_pattern == '13-12-30-4046025'
