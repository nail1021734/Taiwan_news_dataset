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
    url = r'https://www.epochtimes.com/b5/19/12/19/n11733207.htm'
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
            中華民國第15任副總統候選人電視政見發表會將於12月20日晚間7點舉行。新唐人電視台和
            《大紀元時報》將進行網絡直播, 這場副總統電視政見發表會將在台北
            時間12月20日晚間7時(美東時間20日早上6時)舉行,由公視轉播。 台灣第15任總統、副
            總統選舉候選人包括,民進黨蔡英文及賴清德、國民黨韓國瑜及張善政、親民黨宋楚瑜及余湘
            等3組參選人。 此前,台灣首場總統參選人電視政見發表會已經在18日晚間7時在華視登場;
            每一候選人發表政見時間共為30分鐘,分3輪發表政見,每一輪時間10分鐘,沒有交叉詰問。
            中央社說,蔡韓宋砲火猛烈,猶如另類辯論會,韓蔡在會後接受媒體訪問時,繼續隔空交火
            。 另外兩場總統參選人電視政見發表會將分別在25日下午2時由中視轉播、和27日晚間7時
            由台視轉播。
            '''
        ),
    )
    assert parsed_news.category == '台灣'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576684800
    assert parsed_news.reporter is None
    assert parsed_news.title == '台灣副總統候選人電視政見會'
    assert parsed_news.url_pattern == '19-12-19-11733207'
