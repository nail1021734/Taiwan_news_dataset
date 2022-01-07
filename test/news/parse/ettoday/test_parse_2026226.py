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
    url = r'https://star.ettoday.net/news/2026226'
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
            前台灣運彩操盤手、運彩貓顧問、「PS178 運彩一起發」主持人馬大偉,個人完整注單
            請搜尋「馬大偉」。 7月8日密爾瓦基公鹿對鳳凰城太陽,目前大小分盤口219.5分,推薦
            買小分。 字母哥(Giannis Antetokounmpo)首戰出小招,賽前30%會打,結果真上,
            但膝傷多少有影響,上場時間明顯有控制,動作也不敢太大,以免傷勢加劇。 在前兩戰僅
            隔1天情況下,個人認為很難有太大改善,70%的字母哥,平均應該就是25分水準。少了這
            最大威脅,公鹿首戰44%的3分命中率不低,第2戰攻擊效率上漲空間有限。 另外,
            首戰結束後,全世界都在唸公鹿隊的爛防守,第2戰勢必列為頭號改善目標,加上現雙方更熟悉
            ,很難想像太陽3巨頭保羅(Chris Paul)、布克(Devin Booker)、艾頓
            (Deandre Ayton)能再拿81分,首戰太陽118分下修機率很高,構成今日我選小分的
            第2要件。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1625749200
    assert parsed_news.reporter is None
    assert parsed_news.title == 'NBA總冠軍第2戰 續押小分'
    assert parsed_news.url_pattern == '2026226'
