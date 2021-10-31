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
    url = r'https://star.ettoday.net/news/1200165'
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
            貓咪平常看起來很威風,但其實超膽小的!飼主黃唯爾27日在《有點毛毛的》社團分享一則
            搞笑片,內容是主子被小小音樂盒給嚇歪,當場「慢動作」跌落桌邊,不禁讓媽媽偷笑說,「
            平常的威風消失殆盡XD」。 影片中,繫著項圈的貓星人站在桌子上,仔細盯著音樂盒看,忽
            然間,盒子自動開蓋,把主子嚇了一跳!只見阿喵屁股沒坐穩,整隻摔到桌底下,剛好整起意外
            被媽媽給錄下,PO至社團給其它飼主觀看。 媽媽貼文笑說「是嚇到腿軟嗎?!平常的威風消
            失殆盡...」,網友則紛紛留言,「超好笑XDD」、「哈哈哈哈」、「哈哈哈這太好笑」、「
            嚇死本喵了」、「終於認清,原來貓這麼膽小。」、「嚇得不要不要」。 小提醒,平常沒事
            不要隨便亂嚇貓喔!可能會造成牠們心裡陰影和健康負擔。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530074700
    assert parsed_news.reporter is None
    assert parsed_news.title == '音樂盒緩慢彈開...貓嚇到腿軟跌落 媽笑:平常的威風呢?'
    assert parsed_news.url_pattern == '1200165'
