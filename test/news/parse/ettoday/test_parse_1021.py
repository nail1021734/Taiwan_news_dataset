import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/1021'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            香港宅男女神周秀娜比基尼寫真曝光,照片中的她大秀酥胸纖腰,眼神勾人,讓粉絲為之瘋狂
            。她曾經表示,拍攝寫真是她喜歡的工作,性感是一種誇獎,而且自認會做到最好。 周秀娜
            除了有香港宅男女神的封號,也因樣貌與樂基兒相似,又被稱為「翻版樂基兒」。曾經有媒體
            問到,如果未來女兒也想跟她一樣拍攝寫真,為人母的她會如何看待,她表示,「一定全力支持
            。」 周秀娜憑2009年一輯纖體中心反智轉身廣告成名,隨後推出寫真集、接拍電影、廣告
            及出席活動等。她的性感身形及豐滿上,加上代言時曾經以3點式泳裝示人,成為媒體及網友
            談論的焦點人物,有些網友更將她視為性幻想對象。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1318387440
    assert parsed_news.reporter is None
    assert parsed_news.title == '港宅男女神周秀娜內衣寫真 大露酥胸纖腰眼神勾人'
    assert parsed_news.url_pattern == '1021'
