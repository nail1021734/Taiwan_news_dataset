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
    url = r'https://www.epochtimes.com/b5/19/4/25/n11212947.htm'
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
            4月25日,「應對中共當前危險委員會」(Committee on the Present Danger:China)
            在紐約召開研討會,主題為「中國共產黨對美國發動的超限經濟戰」(THE CHINESE COMMU
            NIST PARTY’S UNRESTRICTED ECONOMIC WARFARE AGAINST AMERICA)。 發言人
            包括「應對中共當前危險委員會」副主席加夫尼(Frank Gaffney);前白宮首席戰略師班農
            (Stephen K. Bannon);著名對沖基金Hayman Capital Management創始人巴斯
            (Kyle Bass);中國問題專家及美國知名學者章家敦( Gordon Chang )等。 時間:4月
            25日 早上8點至10點30。地點位於The St. Regis New York。
            '''
        ),
    )
    assert parsed_news.category == '北美新聞,美國政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1556121600
    assert parsed_news.reporter is None
    assert parsed_news.title == '英文直播:紐約研討會聚焦中共對美經濟戰'
    assert parsed_news.url_pattern == '19-4-25-11212947'
