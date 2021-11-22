import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/21314?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            人類的太空觀光旅遊夢想,離實現越來越近了。英國大亨布蘭森(Sir Richard Branson)
            的維珍銀河公司(Virgin Galactic)研發的「太空船2號」(SpaceShipTwo,SS2)5日
            進行試飛,一舉突破音障(超音速),並且創下6萬9千英呎(2萬1千公尺)的飛行高度
            記錄。 這項試飛任務5日上午8點在美國加州莫哈維沙漠(Mojave Desert)進行,
            SS2由母船「白騎士2號」(WhiteKnightTwo,WK2)搭載,先來到4萬6千英呎的高空,
            之後兩者分離,SS2點燃火箭發動機,直上6萬9千英呎,而且速度一舉突破音障,達到1.43
            馬赫(Mach),單飛約30分鐘後平安返回基地。 維珍銀河希望今年後續的試飛,能夠讓SS2
            真正進入外太空。如果一切順利,SS2的飛行高度可以達到4000公里,讓乘客從外太空觀賞
            全人類的家園──地球,並且體驗真正的無重力狀態。 SS2由兩人駕駛,可搭載6位乘客,
            票價當然是天價:2萬5千美元(新台幣75萬元)。維珍銀河透露,目前已有630位貴客預定
            太空之旅,總共繳交8000萬美元的訂金,最快明年就可以成行。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1378428360
    assert parsed_news.reporter == '閻紀宇'
    assert parsed_news.title == '觀光太空船突破音障 再創新高點'
    assert parsed_news.url_pattern == '21314'
