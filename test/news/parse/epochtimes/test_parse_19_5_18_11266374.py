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
    url = r'https://www.epochtimes.com/b5/19/5/18/n11266374.htm'
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
            為慶祝世界法輪大法日,來自全球各地的萬名法輪功學員,自5月16日起在紐約舉行為期三天的
            系列活動,希望藉由集會遊行、集體煉功、排字等活動向世人傳遞法輪大法的祥和與美好。 5
            月18日,數百名來自世界各地的法輪功學員,來到曼哈頓的富利廣場(Foley Square)和砲台
            公園(Battery Park)煉功。學員們隨著煉功音樂,整齊地展示著法輪功五套功法,場面祥和
            美好,為平日裡喧囂熱絡的曼哈頓下城匯入一股清流。
            '''
        ),
    )
    assert parsed_news.category == '北美新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1558108800
    assert parsed_news.reporter is None
    assert parsed_news.title == '組圖10:各族裔紐約煉功 塵囂中帶來寧靜'
    assert parsed_news.url_pattern == '19-5-18-11266374'
