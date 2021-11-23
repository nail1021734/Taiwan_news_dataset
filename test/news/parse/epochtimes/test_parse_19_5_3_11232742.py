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
    url = r'https://www.epochtimes.com/b5/19/5/3/n11232743.htm'
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
            為進一步改善衛星電視播放質量,新唐人電視台與衛星公司協定,近期新唐人電視在亞洲韓星
            5A衛星上的節目將改為MPEG-4 (DVB-S2 ) /SD標清制式播放。屆時我們將通過新唐人
            、大紀元、天地行論壇及明慧網等平台及時公布具體升級日期及各項電視接收參數的變化
            ,請電視觀眾及技術人員提前做好準備。 本次調整屬於播放系統更新,儘管我們的衛視播放
            節目依然沒有鎖碼,但是用戶需要使用能支持DVB-S2/MP4解碼的衛星電視接收機接收升級
            制式後的衛星節目。 如果您現有的接收機已經具備此解碼功能,屆時請您重新搜索接收機以
            確保您可以接收到升級制式後的節目;如果您現有的接收機只具備老式DVB-S/MPEG-2的
            解碼功能,請及時更新您的接收機後才能收看到升級制式後的節目。
            '''
        ),
    )
    assert parsed_news.category == '北美新聞,美國華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1556812800
    assert parsed_news.reporter is None
    assert parsed_news.title == '新唐人電視台紐約工程技術部公告'
    assert parsed_news.url_pattern == '19-5-3-11232743'
