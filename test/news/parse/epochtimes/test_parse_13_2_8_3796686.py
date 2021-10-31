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
    url = r'https://www.epochtimes.com/b5/13/2/8/n3796686.htm'
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
            2月8日,自由門發佈最新7.39版,增強突破封鎖能力,並且集成了網絡電視優化技術。點開主
            面上「中國頻道(150k/800k)」的頁面​​,就會啟動優化技術,得到更順暢的視頻體驗。這種視
            頻格式要求微軟的IE8或以上版本的瀏覽器,及Adobe的Flash Player 至少10.0。並且需要
            打開Javascript和ActiveX.歡迎大家繼續反饋。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞,IT 動向'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1360252800
    assert parsed_news.reporter is None
    assert parsed_news.title == '最新翻牆:自由門7.39版 順暢視頻體驗'
    assert parsed_news.url_pattern == '13-2-8-3796686'
