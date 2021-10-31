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
    url = r'https://star.ettoday.net/news/1200115'
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
            總統蔡英文29日將出席國防部三軍六校聯合畢業典禮,卻因維安考量而讓鄰近的文化國小一度
            停課,引發批評。對此,前民進黨立委林濁水表示,去年「柔過頭」,遭反年改團體突襲闖入
            總統車隊,但今年又「剛硬過頭」,這就有如當局決策時沒有準則,更糟的是還舉旗不定,
            「什麼時候才能脫離執政困境?」 民進黨執政後推動多項爭議改革,街頭抗議四起。去年
            蔡英文主持三軍六校院聯合畢業典禮,引來大批反年改民眾前往抗議,甚至衝破維安封鎖,擋下
            總統車隊,而今面對蔡英文再次到訪,轄區的北投分區不敢大意,協調鄰近的文化國小29日
            結業式當天停課,遭家長砲轟,北市教育局才又緊急宣布恢復正常上下課。 林濁水指出,去年
            維安上「柔性處理」,卻遭突破,但今年警方拉起封鎖線,管制人車,連學校都停課,這又是
            「剛硬過頭」,這就像現在當局決策沒有準則,更糟的是還常常剛柔舉旗不定,部屬不知道要
            怎麼做。 林濁水舉例,民進黨選對會共同召集人陳明文向主席報告提名姚文智,蔡英文卻回
            「一定要這樣嗎?」而這樣心想禮讓又不敢講清楚的心態,就造成今天台北市選災,更向新北及
            其他各地漫延的不幸現象,「什麼時候脫離中心價值觀拿捏不定,政策非過則不及甚至模糊
            不淸的決策模式,什麼時候才能脫離執政困境?」
            '''
        ),
    )
    assert parsed_news.category == '政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530072720
    assert parsed_news.reporter is None
    assert parsed_news.title == '蔡英文執政 林濁水:沒有準則還舉旗不定'
    assert parsed_news.url_pattern == '1200115'
