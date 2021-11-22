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
    url = r'https://www.storm.mg/article/604069?mode=whole'
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
            今(2018)年,司法院為了推廣司法,舉行「司法影展x與社會對話」活動,精選優秀片單,
            讓民眾透過觀影,了解法律背後動人的故事。 「司法影展」共有北中南三場,播放七部精采
            電影:《殺了七個人之前》、《判決》、《他叫簡單,他是我兄弟》、《檢方的罪人》、
            《你只欠我一個道歉》、《當愛不見了》、《七罪追緝令》,劇情真摯動人,並呈現法律中
            會遇到的多種議題。 一般民眾對司法相當陌生,認為法律與人民距離遙遠、內容艱深難懂,
            因此不願意多了解法律。事實上,司法是保障人民權益的手段,與生活息息相關,人民應多加
            了解。因此,司法院盼藉電影劇情跳脫教條式內容,推動「有感司法」,使民眾願意親近
            司法。 「司法影展」觀影活動費用全免,鼓勵民眾踴躍參與,並選擇部分場次舉行映後座
            談會,與民眾更進一步交流。
            '''
        ),
    )
    assert parsed_news.category == '品味生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541531460
    assert parsed_news.reporter == '上晴Talk編'
    assert parsed_news.title == '推廣有感司法 「司法影展」讓民眾更有感'
    assert parsed_news.url_pattern == '604069'
