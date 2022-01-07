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
    url = r'https://star.ettoday.net/news/2086055'
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
            民眾若在中國大陸接種1劑科興或國藥疫苗,回台後第2劑該如何接種。指揮中心發言人莊人祥
            今天表示,只要距離第1劑滿4週,就能登記混打國內現有疫苗,但須依規定登記、排隊。 中國
            大陸為防範COVID-19(2019冠狀病毒疾病)疫情,許多台商、台灣學生在當地必須接種中國
            國藥或科興疫苗並取得健康碼,才能出入不同城市。 根據中國規定,科興、國藥疫苗均須接種
            2劑才具完整保護力。若民眾曾在當地接種1劑疫苗便回台,第2劑該怎麼接種、又有哪些廠牌
            能選,令許多人霧煞煞。 中央流行疫情指揮中心發言人莊人祥今天告訴中央社記者,由於
            科興、國藥疫苗都是獲世界衛生組織(WHO)緊急使用授權(EUA)的疫苗廠牌,若已經完整接種
            2劑疫苗,回台後可不用補打疫苗。 莊人祥指出,若民眾只打了1劑中國COVID-19疫苗,回台
            後可持接種紀錄到地方衛生所登記先前在國外接種的疫苗廠牌,並於間隔4週、28天後,登記
            接種第2劑疫苗。 莊人祥說,由於國內並沒有中國COVID-19疫苗可施打,因此這類民眾第2劑
            疫苗可自選國內現有廠牌,但同樣要到疫苗平台登記意願,並和其他尚未接種第1劑疫苗的民眾
            一起排隊,根據指揮中心開放的接種順序、年齡等,依序接種。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1632410880
    assert parsed_news.reporter is None
    assert parsed_news.title == '打1劑中國疫苗回台「第2劑怎解?」 莊人祥給答案'
    assert parsed_news.url_pattern == '2086055'
