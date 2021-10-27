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
    url = r'https://www.epochtimes.com/b5/13/12/26/n4043823.htm'
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
            俄羅斯各新聞社報導,俄羅斯今天說,已故巴勒斯坦領袖阿拉法特是自然死亡,而非死於輻射
            中毒;但巴勒斯坦駐俄大使說,相關調查仍將持續。 在半島電視台(Al-Jazeera)紀錄片宣稱
            阿拉法特(Yasser Arafat)衣服上有高劑量致命元素釙210後,瑞士、法國和俄羅斯等國鑑識
            專家去年自阿拉法特屍身採集檢體進行研究。 瑞士專家上月說,檢體檢驗結果符合釙中毒,
            但這無法絕對證明死因。而俄國的發現與法國科學家本月稍早做出的評估一致,即阿拉法特
            並非死於放射性元素釙。 國營俄羅斯新聞社(RIA)報導,巴勒斯坦駐俄大使穆斯塔法
            (Faed Mustafa)說,俄國的認定不會使調查阿拉法特死因的努力中止。 俄羅斯新聞社引述
            穆斯塔法說:「我只能說,我們已決定繼續(調查)。我們尊重他們的立場,對他們的工作給予高度
            評價,但我方已做出繼續調查的決定。」 阿拉法特遺孀蘇哈(Suha Arafat)認為,阿拉法特是
            遭到1名親信的政治謀殺。許多巴勒斯坦人認為,是以色列殺了阿拉法特,但以色列否認這項指控。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1387987200
    assert parsed_news.reporter is None
    assert parsed_news.title == '阿拉法特死因 調查繼續'
    assert parsed_news.url_pattern == '13-12-26-4043823'
