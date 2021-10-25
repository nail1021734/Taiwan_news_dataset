import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/23/a636434.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            全球領導人今天齊集布拉格,參加捷克天鵝絨革命英雄哈維爾(Vaclav Havel)的喪禮。
            哈維爾18日逝世,享壽75歲。 法國總統沙柯吉(Nicolas Sarkozy)、英國首相卡麥隆
            (David Cameron)與美國國務卿希拉蕊(Hillary Clinton)和前總統丈夫柯林頓,與
            數十國領導人齊聚在歷史悠久的聖維特大教堂(St Vitus’ Cathedral)。 捷克全國
            1050萬民眾中午默哀一分鐘,許多地區的交通與工作停擺。鄰國斯洛伐克也宣布今天為
            全國哀悼日。 哈維爾領導捷克走過1989年無流血衝突的絲絨革命,這場革命在當時捷克
            斯拉夫時期推翻共產主義。 先前布拉格市中心1座教堂,成千上萬民眾列隊走過哈維爾的
            靈柩,表達內心的追思。哈維爾的遺體安置在教堂供人瞻仰,21日才在莊嚴的送葬行列運往
            布拉格城堡的瓦拉迪斯拉夫廳(Vladislav Hall)。 捷克哀悼者持續湧入,當局昨天持續
            讓瓦拉迪斯拉夫廳開放至將近午夜。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324569600
    assert parsed_news.reporter is None
    assert parsed_news.title == '哈維爾喪禮 全球領袖出席'
    assert parsed_news.url_pattern == '2011-12-23-636434'
