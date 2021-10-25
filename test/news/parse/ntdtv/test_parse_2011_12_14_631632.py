import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/14/a631632.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            緬甸變了, 中國呢? 安妮:您好!觀衆朋友,歡迎收看禁聞論壇。 11月30日,美國國務卿
            希拉里抵達緬甸首都內比都,開啓了美國50年來首次派遣國務卿到緬甸的"歷史性訪問"。到
            訪期間,希拉里會晤了緬甸總統吳登盛和諾貝爾和平獎獲得者翁山蘇姬。 伍凡先生 ,有評論
            說希拉里訪問緬甸是冬天裏的一把火,不但點亮了緬甸,也燒到了中共的後院 。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1323792000
    assert parsed_news.reporter is None
    assert parsed_news.title == '緬甸變了,中國呢?'
    assert parsed_news.url_pattern == '2011-12-14-631632'
