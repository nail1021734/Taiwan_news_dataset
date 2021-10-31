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
    url = r'https://star.ettoday.net/news/1200158'
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
            6月27日凌晨,阿根廷與奈及利亞進入殊死戰,雙方戰至最後關頭才分出勝負,上半場梅西
            (Lionel Messi)為球隊打入一個世界波,然而下半場阿根廷禁區犯規,遭判12碼,莫塞斯
            (Victor Moses)順利點進讓奈及利亞扳平了比分。眼看阿根廷可能因踢和遭淘汰,曼聯後衛
            羅霍(Marcos Rojo)在12碼處接獲隊友傳球,起腳射門,右下角入網,羅霍拯救了
            阿根廷。 羅霍的表現,無疑是整場球的致勝英雄,他在第86分鐘站了出來,梅爾卡多
            (Gabriel Mercado)右路傳中,曼聯後衛羅霍12碼處第一時間凌空墊射右下角入網,比分
            變成2比1,羅霍拯救了球隊,阿根廷頓時活了過來,羅霍奔跑吶喊慶祝,有意思的是,梅西此時
            跑了過來,他一下跳到了羅霍身上,而羅霍也揹著梅西繼續奔跑慶祝,情緒相當激動。 這場
            勝利,阿根廷全隊以及球迷的激情都被點燃,羅霍這一腳價值千金,他幫助阿根廷死裡逃生,
            進入淘汰賽。 阿根廷《奧萊報》表示,「對奈及利亞比賽承受的痛苦已經成為過去。羅霍的
            進球引發了瘋狂,也證明了球隊對進入淘汰賽是何等渴望。」 羅霍身背梅西慶祝的畫面,最好
            地反映了阿根廷上演奇蹟、死裡逃生的困難過程。 不過在勝利大逃亡後,阿根廷接下去將
            對陣強大的法國,梅西和他的隊友們是否又會再次拿出好表現,全世界都在看。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530069540
    assert parsed_news.reporter is None
    assert parsed_news.title == '羅霍近絕殺破門 扛起了梅西和阿根廷'
    assert parsed_news.url_pattern == '1200158'
