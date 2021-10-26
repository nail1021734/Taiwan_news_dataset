import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201802070327.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            花蓮雲門翠堤大樓因強震嚴重傾斜,下午約3時左右,在10分鐘內明顯位移4公分,現場人員為
            安全起見暫停搜救。在經過派遣人員確認過現場狀況後,在晚間6時10分左右恢復搜救作業,
            爭取黃金72小時救援時間。 現場前進指揮所表示,大樓今天下午3時多,10分鐘內明顯
            位移4公分,為安全起見暫停搜救。下午5時50分多,在派遣人員確認過現場的狀況後,
            在6時10分恢復搜救作業。 來自各縣市的搜救隊員也陸續進入大樓進行搜救工作,不過目前
            天空下雨,天色也開始昏暗,將增加搜救的難度。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1517932800
    assert parsed_news.reporter == '沈如峰花蓮'
    assert parsed_news.title == '花蓮地震 雲門翠堤恢復搜救爭取黃金72小時'
    assert parsed_news.url_pattern == '201802070327'
