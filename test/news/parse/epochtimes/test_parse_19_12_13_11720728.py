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
    url = r'https://www.epochtimes.com/b5/19/12/13/n11720728.htm'
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
            加州的公司包括來自聖地亞哥的一家屋頂公司,日前在墨西哥南端的塔巴斯科州(Tabasco)
            利用三維打印技術建房,24小時建成一所房子。其長期目標是建設一個500套住房的社區。 據
            CBS8電視台,剛從墨西哥建築工地回到聖地亞哥的Resilient Roofing公司老闆
            Seth Larson表示,自己過去一直以為利用三維打印技術建房是科幻,但現在已是事實
            。 舊金山的New Story公司和位於德州奧斯汀(Austin)的ICON公司,去年在奧斯汀建了
            一個三維打印的房子。這個房子面積350平呎,造價3萬5千美元,花了48小時「打印」完成
            。 但是這次在墨西哥,New Story,Icon和Larson不僅要建房,更要建設一個社區。他們
            計劃在第一階段建成50所住房,而長期計劃是500套住房。社區內將包括教堂、超市、購物
            中心、停車處和墓地等。這將是世界上第一個由三維打印房構成的社區。 Larson表示,自己
            的目的是為無家可歸者提供住房。三維打印房用混凝土建成,花費低,速度快。他希望三維
            打印造房能在全世界發展起來,包括在難以獲得建築許可的美國,為無家可歸者提供住所和
            生活社區。Larson預計在墨西哥建的房子,造價在4千至5千美元左右。 三維打印技術的概念
            大約在1970年代形成。到1980年代末,出現了第一台商用三維打印機。至今,人們用三維打印
            技術製造各種物件,包括藝術品、食物、服裝、武器、航空元件、汽車、人體臟器等。近些
            年來,利用三維打印建造房屋、開發社區成為該技術的新應用。
            '''
        ),
    )
    assert parsed_news.category == '美國,聖地亞哥,本地新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576166400
    assert parsed_news.reporter == '田磊'
    assert parsed_news.title == '三維打印不僅建房 還要建社區'
    assert parsed_news.url_pattern == '19-12-13-11720728'
