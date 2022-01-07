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
    url = r'https://www.epochtimes.com/b5/13/12/15/n4034530.htm'
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
            俄羅斯MiG-31戰鬥機於週六起飛後不久,墜毀在俄羅斯遠東地區,飛行員開動彈射座椅脫離
            機艙,落在海參崴以北大約50英里的加油站附近的公路上。 《捷克新聞》(NOVINKY.cz)12
            月14日消息,俄羅斯MiG-31戰機從Knviči一個軍用機場起飛後不久墜毀。來自俄羅斯國防
            部的報告稱,MiG-31戰機沒有攜帶任何武器。這是在測試飛行中發生的意外。飛機殘骸沒有
            對地面任何人造成傷害,也未造成任何損失。 這是在過去三年來第四次發生戰鬥機墜機的
            類似事故。上一次MiG-31戰機發生事故是2011年9月份在彼爾姆地區(Permsk kraj),當時在
            惡劣的天氣條件下,機上的兩名飛行員因迷失方向而喪生。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1387036800
    assert parsed_news.reporter == '李天韻'
    assert parsed_news.title == '俄羅斯MiG-31戰機在遠東墜毀'
    assert parsed_news.url_pattern == '13-12-15-4034530'
