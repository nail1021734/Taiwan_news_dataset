r"""Positive case."""

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
    url = r'https://www.cna.com.tw/news/aipl/201812310197.aspx'
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
            「週日電訊報」(Sunday Telegraph)報導,英國國防大臣威廉森(Gavin Williamson)
            接受訪問時表示,英國正研究在加勒比海地區和東南亞建立2座新的軍事基地。 威廉森
            表示,這項計畫是為了讓英國在退出歐洲聯盟後提高在國際舞台的分量,成為
            「真正的全球參與者」。他還說,這也意味英國自1968年實施的所謂蘇伊士運河以東
            策略的轉變,當年英國撤離在東南亞和波斯灣的軍事基地。 他說:
            「我們必須表明這項政策已被撕毀,英國再度成為全球性國家。」英國在賽普勒斯、直布羅陀、
            福克蘭群島和狄耶戈加西亞(Diego Garcia)等地已有軍事基地。 威廉森預測英國脫歐後,
            「政治焦點會有重大轉變」,英國必須「不僅要與澳洲、加拿大、紐西蘭、加勒比海國家,
            還要與非洲各國建立更深層的關係」。 他受訪時也說,英國政府的無協議脫歐應變計畫
            相當明智。此計畫涉及調派3500名軍人隨時待命,以防英國3月退出歐盟時
            發生混亂情況。 他說:「我們總是在計劃如何因應突發狀況,以確保不論有無協議脫歐,
            一切都能平順運作。」
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1546185600
    assert parsed_news.reporter == '倫敦'
    assert parsed_news.title == '因應脫歐 英國擬在加勒比海和東南亞設軍事基地'
    assert parsed_news.url_pattern == '201812310197'
