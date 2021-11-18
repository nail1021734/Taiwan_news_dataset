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
    url = r'https://star.ettoday.net/news/5043'
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
            Selina(任家萱)日前終於和阿中(張承中)完婚,她的母親(任媽)3日談到,「早知道就不要
            生她,就不用遭受這場劫難。」因為被火紋身的女兒曾有輕生念頭,「好幾次想死」。另外
            ,任爸還透露,Selina因為復健期間吃了很多藥,因此2、3年恐怕不適合懷孕,對此,阿中則
            不願回應。 任爸出席新書《用愛守候》記者會時,談到Selina這一年來所受的煎熬,數次
            哽咽掉淚。任爸也談到,感謝上蒼沒有奪走女兒的美貌和生育能力,不過,因為每天要吃
            很多藥,要等到2、3年後皮膚更穩定才適合懷孕,但一切還是尊重小倆口的想法。 根據
            《蘋果日報》報導,任爸還表示,Selina似乎已經接受火吻傷疤,在穿結婚禮服時,手臂露出
            大片紅疤,曾建議出場時可站她左邊幫忙遮掩,沒想到女兒竟然說不用,「這個我已經接受」
            。 任爸更說,先前問過Selina,當時拍爆破戲時,為何不找替身?善良的女兒卻回答,還好
            不是替身,不然會「愧疚一輩子」,因為如果受傷的不是自己,別人可能無法接受如此完善的
            治療。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1320368160
    assert parsed_news.reporter is None
    assert parsed_news.title == '遭火吻Selina好幾次想死 任爸:3年內不宜懷孕'
    assert parsed_news.url_pattern == '5043'
