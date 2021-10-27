import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/202110210003.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            菲律賓外交部今天表示,中國船隻在南海以警報器、喇叭和無線電通訊挑戰菲國船隻,菲方
            為此提出外交抗議。 路透社報導,菲律賓外交部推文指出:「這些挑釁行為對南海的
            和平、良好秩序及安全構成威脅,有背於中國基於國際法應守的義務。」 菲律賓外交部
            指稱,當菲方在領域及海域及其周邊進行例行性巡邏時,已發生逾200次這類挑戰。但菲國
            外交部未闡明這些挑戰發生在什麼期間。 針對上述情況,中國駐馬尼拉大使館未在上班
            時間外立即作出回應。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1634745600
    assert parsed_news.reporter == '馬尼拉'
    assert parsed_news.title == '菲律賓提出外交抗議 控中國在南海從事挑釁行為'
    assert parsed_news.url_pattern == '202110210003'
