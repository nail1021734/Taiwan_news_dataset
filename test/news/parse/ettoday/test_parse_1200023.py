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
    url = r'https://star.ettoday.net/news/1200023'
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
            根據《鏡周刊》報導,曾出過《黑道狀元》《壞到剛剛好》2本書的討債專家董念台,終於將
            告別單身。讓眾多男人羨慕的是,他的未婚妻是35歲的美女上班族,並且在6月30日
            宴客。 董念台表示,其實他在5月18日就已經跟妻子登記,2人從認識、戀愛到結婚不到半年。
            為何這麼迅速?董念台透露因為兩人都想要有個家,而且緣分到了就會成為夫妻。 董念台也
            透露與妻子相識的過程。他說有次在朋友那邊碰到,覺得漂亮所以留了臉書,變成「臉友」。
            2人透過臉書互動一陣子後,便開始約會、進而相戀。 不過董念台說,岳母的年紀比她還要
            小6、7歲,岳母原本希望女兒能夠嫁給一個稍微正常的人,但最後董念台透露,她都叫岳母
            「大娘」,並說「我想要告訴她,我會當她的接班人,當個稱職的『二娘』,我會好好照顧她的
            女兒,不會讓她失望。」岳母這才點頭答應。 董念台最有名的事蹟之一,是曾向前副總統
            呂秀蓮求婚。2001年12月,董念台大陣仗找來24輛凱迪拉克豪華禮車,身穿燕尾服,往總統府
            前進,大張旗鼓地向當時的副總統呂秀蓮求婚。 董念台並當場發表1封給呂秀蓮的公開信,
            信中說,呂秀蓮曾形容自己進入總統府的500多個日子是在「坐心牢」,而他開討債公司被
            警方打壓則是在「坐壓力牢」,2人同是天涯淪落人,何不攜手共創人生? 回憶往事,董念台
            笑說:「我現在結婚了,最難過的應該是呂秀蓮吧!因為她失戀了。」
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530053880
    assert parsed_news.reporter == '葉國吏'
    assert parsed_news.title == '父女戀! 68歲討債天王娶35歲美女OL'
    assert parsed_news.url_pattern == '1200023'
