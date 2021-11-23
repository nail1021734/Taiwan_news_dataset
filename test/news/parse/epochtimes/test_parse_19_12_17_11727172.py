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
    url = r'https://www.epochtimes.com/b5/19/12/17/n11727172.htm'
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
            退出曾經加入的少先隊 在國內的時候就已經認識到了中共的邪惡,但是由於小學加入少先隊
            是必須的,所以也沒有辦法。但是每一次看到所謂的少先隊活動都會很惡行,還好後來沒有加入
            共青團。我在此聲明我退出曾經加入過的少先隊,並與之劃清界限! 三退 看透中共邪教了。
            法輪功學員根本就沒做錯什麼啊,就這麼對待別人。看到整個共產邪教根本就是想著如何滅掉
            別人的自由,很邪惡,決定在這裡公開退出共匪黨團隊。 退出黨組織 本人杭州某銀行工作者
            ,今天明白中共對人民自身權利自由–特別是對法輪功的迫害,決定退出黨組織。
            '''
        ),
    )
    assert parsed_news.category == '大陸新聞,社會萬象'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576512000
    assert parsed_news.reporter is None
    assert parsed_news.title == '每日三退聲明精選'
    assert parsed_news.url_pattern == '19-12-17-11727172'
