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
    url = r'https://www.epochtimes.com/b5/13/8/13/n3939870.htm'
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
            由中國鄭州直達漢堡的貨車專列正式通車,第一趟列車滿載著集裝箱,經歷了兩個星期的長
            途旅行,於8月2日到達目的地漢堡。 這條鐵路線從鄭州出發,經西安、烏魯木齊進入哈薩克
            斯坦,再經過俄羅斯、白俄羅斯、波蘭,最後到達漢堡,全程1.02萬公里,耗時15天,第一輛貨
            車裝載了51個集裝箱。德鐵計劃,今後每週往返一次。 德鐵總裁Grube表示,貨車運輸比海
            運和空運都經濟,而且所需要的時間只是海運的一半。德鐵的目標是每天都通車,但是是否
            加快列車往返頻率,要看需求情況。另外,路上的時間也還需要盡一步縮短,這包括加快各國
            的通關手續,重要的是統一鐵軌寬度。目前這趟列車在路途上需要更換幾次車輪以適應不同
            國家的鐵軌寬度。 Grube認為,開啟這趟列車只是一個開端,德國人需要發揮創造力,開闢新
            的渠道。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1376323200
    assert parsed_news.reporter == '余平德國,賈南'
    assert parsed_news.title == '中國直達漢堡貨運列車開通'
    assert parsed_news.url_pattern == '13-8-13-3939870'
