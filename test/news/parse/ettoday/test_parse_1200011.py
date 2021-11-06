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
    url = r'https://star.ettoday.net/news/1200011'
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
            美麗華大直影城因家族、股東內鬥,22日起停業1個月。前董事長黃世杰所屬公司「美麗新
            娛樂」21日晚間召開記者會,重申先前帶領大直影城期間從無異狀,紅了之後被政治家族覬
            覦,卻不重視專業,造成影廳癱瘓。這起風波的產生,據傳都是因為一位神秘女子。 根據《
            周刊王》報導,美麗華集團內有一位尤姓女董事,近年因與黃世杰關係匪淺,不僅氣走美麗華
            開國元老,還推薦自己人進入工作。根據報導指出,尤女原本是美麗華門市其中一個櫃位的
            店員,因緣際會下被黃世杰重用、展開長達10多年的情誼。 尤女陸續接下美麗華旗下多家
            公司的董事職,深獲黃世杰信任,但也因此讓黃世杰身邊許多幹部不滿離職,其中黃世杰長女
            、擔任特助的黃亦杰也憤而求去。 對於尤女的行為已經讓家族成為不滿,屢次對黃世杰「
            規勸」,要他別對尤女過於聽從。「美麗華娛樂」董事會也希望黃世杰約束尤女,但未獲採
            納,所以才會拔掉黃世杰董事長一職,由姊姊黃秋香接手。 對於爆料,尤女說「完全不是事
            實」、「不可能我一個人能做決定、「我沒這個大的權力。」
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530058380
    assert parsed_news.reporter == '葉國吏'
    assert parsed_news.title == '美麗華家族內鬥元兇就是她! 黃世杰櫃姐女密友曝光'
    assert parsed_news.url_pattern == '1200011'
