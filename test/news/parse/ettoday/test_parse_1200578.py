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
    url = r'https://star.ettoday.net/news/1200578'
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
            「我想將電影從非常現實的三次元瞬間轉換成虛擬的二次元,混搭各種不同的幽默。」導演
            自嘲作品深受法國漫畫的影響,《我的抓狂(女)友》在喜劇節奏或是人物表現充滿了四格漫
            畫的趣味,像是速食般迎合年輕觀眾的口味,電影靈感則來自導演年輕時的「同居」
            經驗。 為了安慰剛剛失戀的文森,娜菲莉決定邀文森一起同住,他們約法三章「要性不要愛,
            一夜情至上」,誰也不許再談戀愛。他們天天一起開趴慶祝,久違單身的文森展開好多好多
            個「一夜情」,娜菲莉也不遑多讓,胖瘦不挑,最好是「三人行」。夜夜夜狂,各玩各的他們
            堪稱最佳室友,直到有一天,文森遇上了真命天女茱莉,當文森陷入熱戀,娜菲莉會如何懲罰
            違反誓言的文森呢?當史上最性感、最熱情、最赤裸裸的女室友抓狂了,文森即將陷入
            萬劫不復的桃色危機......
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1531463400
    assert parsed_news.reporter is None
    assert parsed_news.title == '火辣床伴和真愛女友選邊站!《我的抓狂友》爆發警戒'
    assert parsed_news.url_pattern == '1200578'
