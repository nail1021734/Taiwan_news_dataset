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
    url = r'https://www.storm.mg/article/604783?mode=whole'
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
            舊金山巨人在今日正式聘請洛杉磯道奇總經理薩伊迪(Farhan Zaidi)擔任球團棒球營運
            總裁,41歲的薩伊迪在道奇棒球營運總裁弗里曼(Andrew Friedman)所帶領的團隊底下
            工作了4年,也正式告一個段落。 道奇在過去兩個賽季皆闖進了世界大賽,這也成為了
            薩伊迪成績單上最亮眼的數據,果不其然,巨人,看見了,巨人執行長貝爾(Larry Baer)
            在聲明中指出:「我們開始在尋找棒球界中最優秀的人才之一,而薩伊迪的許多成就和專業
            知識都完全超越我們的預期,薩伊迪總是被認為是在我們行業中的高級管理人員之一,我們
            也很期待看見有他加入的巨人。」 薩伊迪再回到北加州後,對於自己即將擔任巨人球團棒
            球營運總裁,薩伊迪表示:「我很高興回到灣區,加入一支最具傳奇色彩的球隊,我總是遠遠
            地看著巨人這支球隊,對於他們球隊的文化和成就感到相當敬佩,而我已經等不及要
            上班了。」 巨人在今年9月解僱了原先的總經理伊凡斯(Bobby Evans),上個賽季累積
            拿下73勝89敗,其中在9月份更是本季最慘的5勝21敗,而巨人在先前5個賽季拿下3次世界
            大賽冠軍後,已經連續2年未能闖進季後賽,薩伊迪的挑戰這時才正要開始。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541545320
    assert parsed_news.reporter == '陳耿閔'
    assert parsed_news.title == '巨人挖角道奇總經理薩伊迪 成為新任棒球營運總裁'
    assert parsed_news.url_pattern == '604783'
