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
    url = r'https://star.ettoday.net/news/3186'
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
            台北時間23日晚間土耳其東北部接壤伊朗地區,發生芮氏地震儀規模7.3之強烈地震。位於
            震央附近的凡城(Van),目前已知有10餘棟建築倒塌,周圍地區則有約30棟建築在地震中受到
            損傷;截至目前已造成264人死亡,人數還在攀升中,依土耳其地質機構的預計,此次強震將
            造成超過1000人喪命。 土耳其發生地震後,外交部及我駐土耳其代表處已於第一時間掌握
            狀況,初步瞭解無我國僑民居住於地震發生區域,亦無我國籍旅行團於災區附近遊覽。外交部
            已請我駐土耳其代表處向土國政府表達關切之意,並瞭解我國派遣救援隊前往協助之可行性
            。 外交部將持續密切注意土國災情,隨時告知國人作為旅遊參考,並提醒國人赴土耳其商旅
            時,應事前掌握當地災情最新情形,提高警覺並注意自身安全。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1319461380
    assert parsed_news.reporter is None
    assert parsed_news.title == '土耳其發生7.3級強震 死亡人數恐逾千'
    assert parsed_news.url_pattern == '3186'
