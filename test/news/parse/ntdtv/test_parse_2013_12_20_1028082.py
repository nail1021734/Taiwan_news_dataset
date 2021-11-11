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
    url = r'https://www.ntdtv.com/b5/2013/12/20/a1028082.html'
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
            歐巴馬12月18日提名參議院財政委員會主席鮑卡斯(Max Baucus)為下一任美國駐華大使。
            鮑卡斯背景如何,如果通過任命,他會給中美關係帶來甚麼? 美東時間今晚9點半到10點,熱點
            互動熱線直播節目將邀請專家介紹分析,敬請收看,並撥打熱線參與討論或提問。
            '''
        ),
    )
    assert parsed_news.category == '美國'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1387468800
    assert parsed_news.reporter is None
    assert parsed_news.title == '熱點互動:鮑卡斯將給中美關係帶來甚麼?'
    assert parsed_news.url_pattern == '2013-12-20-1028082'
