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
    url = r'https://www.ntdtv.com/b5/2013/04/17/a882078.html'
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
            伊朗昨天發生地震,造成巴基斯坦至少40人死亡,巴國調動士兵參與救災。美國表示
            願意援助伊朗及巴基斯坦。 伊朗東南部發生規模7.8強震,但目前只有巴基斯坦偏遠
            的俾路支省(Baluchistan)傳出有人喪命,俾路支省數百棟泥造房舍被震毀。 美國
            國務卿凱瑞(John Kerry)表示:「我們已經準備好在如此艱困的時期提供
            協助。」 巴基斯坦官員表示,俾路支省瑪許卡爾地區(Mashkail)的房舍因地震倒塌
            後,已出動正規軍及邊防軍等準軍事部隊協助救災。 官員表示,2架軍用直升機載著
            醫療團隊前進瑪許卡爾地區,準軍事部隊也支援救災。 地方政府官員說:「瑪許卡爾
            地區至少40人喪命,另外有80人受傷。」
            '''
        ),
    )
    assert parsed_news.category == '國際,社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1366128000
    assert parsed_news.reporter is None
    assert parsed_news.title == '伊朗強震巴國40死 美伸援'
    assert parsed_news.url_pattern == '2013-04-17-882078'
