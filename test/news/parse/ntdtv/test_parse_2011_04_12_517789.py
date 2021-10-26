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
    url = r'https://www.ntdtv.com/b5/2011/04/12/a517789.html'
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
            白俄羅斯首都明斯克(Minsk)昨日發生地鐵站爆炸事件,死亡人數至今已增至12人。該地鐵
            站距離白俄羅斯總統魯卡申柯(AlexanderLukashenko)的總部不遠,官方認為這是一起
            恐怖攻擊事件。 國際傳真社(Interfax)引述白俄羅斯國家安全局發佈的消息表示:「
            死亡人數已攀升至12人,其中6人身份已確定。」 該消息指出,該爆炸事件還造成149人受傷,
            其中22 人傷勢嚴重,情況危急,30人須接受治療,不過無生命危險。 這起爆炸事件發生在
            明斯克人潮擁擠的地鐵大站,白俄羅斯檢方已將其定調為恐怖攻擊事件,這是該國繼蘇聯解體
            後,所遭遇到最嚴重的攻擊事件。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302537600
    assert parsed_news.reporter is None
    assert parsed_news.title == '白俄爆炸案死亡人數增至12人'
    assert parsed_news.url_pattern == '2011-04-12-517789'
