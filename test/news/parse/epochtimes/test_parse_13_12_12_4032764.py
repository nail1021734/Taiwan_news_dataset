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
    url = r'https://www.epochtimes.com/b5/13/12/12/n4032764.htm'
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
            英國威廉王子與嬌妻凱特的愛兒喬治小王子打扮成1隻小馴鹿,歡度人生第1個耶誕節,王室
            四代同堂齊享天倫之樂。 英國「每日郵報」(Daily Mail)報導,喬治眼前除了笑容滿面的
            爸媽,還有扮成耶誕老人的叔叔哈利王子(Prince Harry)。 不僅如此,女王伊麗莎白二世
            (Elizabeth II)、王儲查爾斯(Prince Charles)和康瓦爾公爵夫人
            (Duchess of Cornwall)卡蜜拉也都齊聚一堂。 乍看之下,你可能會理所當然地自認為,
            私下提前偷窺到王室歡度耶誕節的照片。 事實上,這些看似在山均漢姆堡
            (Sandringham Castle)拍攝的照片,是攝影師傑克森(Alison Jackson)請來酷似
            王室成員的分身所拍成的玩笑之作。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386777600
    assert parsed_news.reporter is None
    assert parsed_news.title == '山寨皇室耶誕 英小王子分身入鏡'
    assert parsed_news.url_pattern == '13-12-12-4032764'
