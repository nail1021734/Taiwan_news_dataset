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
    url = r'https://www.epochtimes.com/b5/13/2/27/n3810619.htm'
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
            天主教教宗本篤十六世今天搭乘座駕,最後一次繞行聖伯多祿廣場,向聚集的數以萬計信徒
            致意,隨後開始退位前最後的公開接見。教宗明天將由這個領導全球12億天主教徒的職位退
            位。 信徒湧進聖伯多祿廣場(St Peter’s Square),向年老體衰的85歲教宗道別。本篤十六
            世(Pope Benedict XVI)任職8年後突然宣布退位,表示他身心俱疲,無法跟上現代世界。 阿
            布魯佐區(Abruzzo)的67歲神父朱里歐(Giulio)說:「我來到這裡,是要感謝他過去8年來所
            做的每一件事。」 他說:「對每位天主教徒來說,教宗退位都是非常強烈的訊息。他不是痛
            苦的退位,而是心平氣和的遜位。」 一群信徒舉著標語,上頭寫著:「本篤十六世,我們將想
            念你。」另一幅標語寫著:「教宗是這座城市的核心!」 這將是教宗最後一次大型公開活動
            。 梵蒂岡著名的聖伯多祿廣場與周圍有超過10萬人聚集,當局安置金屬探測器並在梵蒂岡
            屋頂部署狙擊手,並搭建臨時診所。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361894400
    assert parsed_news.reporter is None
    assert parsed_news.title == '退位前夕 教宗最後接見信徒'
    assert parsed_news.url_pattern == '13-2-27-3810619'
