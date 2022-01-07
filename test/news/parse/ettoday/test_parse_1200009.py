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
    url = r'https://star.ettoday.net/news/1200009'
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
            才剛在台灣上市的 LG G7+,稍早韓國版本加入新的全新的影像錄製格式 4K@60 fps,最長可
            達 5~6 分鐘的錄製時間。據了解目前這項更新僅在南韓推送,台灣與美國等其他上市地區
            將於未來更新。 Phonearena 記者實測,啟用這個影片錄製格式跟一般路影音一樣,打開相
            機、進入設定,然後選擇影像解析度,就可以選擇“UHD 16:9(60fps)”選項。 除此之外,這次
            更新之後將提升自動拍攝時的清晰度,另外還有「超級明亮」模式啟動時,如果使用閃光燈
            拍攝將透過改善紅色和綠色的渲染以提供更好的照片。 目前這項更新將在未來幾週內在其
            他地區推出。
            '''
        ),
    )
    assert parsed_news.category == '3C家電'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530050280
    assert parsed_news.reporter == '洪聖壹'
    assert parsed_news.title == 'LG G7+將透過相機韌體更新提升錄影品質到 4K@60 fps'
    assert parsed_news.url_pattern == '1200009'
