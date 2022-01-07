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
    url = r'https://www.epochtimes.com/b5/13/3/12/n3820892.htm'
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
            荷蘭檢察部門近日表示,前南斯拉夫內戰期間駐紮斯雷佈雷尼察
            地區,荷蘭維和部隊負責人將不會面臨種族滅絕罪和戰爭罪的指控。 道姆∙卡勒曼斯
            (Thom Karremans),現年64歲,在前南斯拉夫內戰期間,曾擔任駐紮
            斯雷佈雷尼察飛地荷蘭維和部隊司令員。但卻未能阻止斯雷佈雷尼察大屠殺,導致超過
            8000名男人和男孩被殺害。經過調查,荷蘭檢察部門認為卡勒曼斯上校並沒有涉及
            波斯尼亞塞族軍隊所犯下的戰爭罪行。 然而,3名斯雷佈雷尼察大屠殺受害者的親屬則呼籲
            應將卡勒曼斯和其他2名荷蘭維和部隊軍官送上戰爭法庭。他們認為得到聯合國授權的
            荷蘭維和部隊沒有盡一切努力,保護他們的親人避免受到傷害。 2011年,海牙上訴法庭裁定,
            荷蘭政府承擔這3名受害者死亡的責任。這一裁決為卡勒曼斯免受戰爭罪行起訴掃清了
            障礙。但目前受害者親屬計劃採取其它法律途徑進行控訴。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1363017600
    assert parsed_news.reporter == '琮瑜荷蘭,李雲帆'
    assert parsed_news.title == '荷蘭陸軍上校將不會面臨前南戰爭罪指控'
    assert parsed_news.url_pattern == '13-3-12-3820892'
