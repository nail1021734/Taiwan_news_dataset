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
    url = r'https://star.ettoday.net/news/2104412'
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
            YouTuber小玉(朱玉宸)去年因母乳爭議,頻道停止更新近1年,前陣子受訪時,他還自爆
            靠股票獲利超過500萬,怎料如今再傳近況,竟是因操盤製作換臉謎片販售牟利,遭到警方
            逮捕,對此,其中的受害者一隻阿圓、愛莉莎莎都陸續回應了。 一隻阿圓曾是其中一名
            受害者,18日得知小玉被逮捕後,她在限時動態PO全黑圖表示:「對於完全不懂尊重女性的人,
            真的覺得你心態很可悲。」沒想到,她隔天看到有網友在自己的YouTube影片留下不禮貌的
            言論,讓她再度怒火中燒。 該網友用看好戲的語氣說:「發表下當上女優感覺如何?小圓?」
            對此,一隻阿圓表示就是有這種搧風點火的人,「他可惡,但我知道也有你這種人,
            一點都不在乎別人的感受」,她最後附上一個噁心嘔吐的表情符號開罵:
            「你跟他都一樣!」 此外,愛莉莎莎19日凌晨在Instagram坦言,直到小玉遭逮才
            發現自己有被換臉,她附上截圖和3個笑到哭的表情符號說「原來也有我」,心情似乎
            沒有受到太大影響。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634610360
    assert parsed_news.reporter == '潘慧中'
    assert parsed_news.title == '被小玉換臉還遭嗆「當上女優感覺如何」 一隻阿圓PO全黑圖爆氣發聲'
    assert parsed_news.url_pattern == '2104412'
