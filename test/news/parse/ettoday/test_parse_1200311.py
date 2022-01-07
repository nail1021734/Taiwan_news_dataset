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
    url = r'https://star.ettoday.net/news/1200311'
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
            露伊莎蕊薇拉(Luisa Rivera)是位定居於英國倫敦的智利插畫師。蕊薇拉的世界經常充滿
            對女性、大自然、神話與民俗風的幻想,筆下的彩繪國度也飽富魔幻而靜謐的憧憬世界,讓
            人過目難忘,沉醉腦海。 善於水彩創作的蕊薇拉,畫面中的每個色塊或輪廓都力求完美的精雕
            細琢。蕊薇拉對於人與自然間的微妙連結感興趣,希望透過作品啟發更多人發現自我與環境間
            的神秘連結與奧祕。 已出版三本繪本專著的蕊薇拉,長期與世界知名的雜誌或出版商合作
            書籍、雜誌、報刊與展覽等設計案,並與加拿大航空、蘭登書屋、紐約時報、綜藝雜誌等客戶
            合作。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530245040
    assert parsed_news.reporter is None
    assert parsed_news.title == '掉進智利插畫家 Luisa Rivera 的魔幻夢境裡'
    assert parsed_news.url_pattern == '1200311'
