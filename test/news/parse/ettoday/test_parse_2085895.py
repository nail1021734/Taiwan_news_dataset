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
    url = r'https://star.ettoday.net/news/2085895'
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
            雲林縣因財政困難未跟進其他縣市普發現金,四湖鄉參天宮關聖帝君廟為鼓勵學生努力向學,
            決定普發全鄉國中小學生約900多人每人1000元助學金,預計於9月25日發放,由各校
            指派人員直接到廟領回,許多家長得知消息均歡喜表示一千元不無小補,未來孩子出社會有
            能力也要回饋家鄉善循環。 今年疫情期間,許多民眾到參天宮參拜,透露疫情影響收入,
            不僅生活困難,連孩子的教育費都出現問題,廟方得知後,覺得應該為鄉內孩子做些事,
            鼓勵孩子不要灰心、努力向學。參天宮主委吳孟宗表示,經廟方開會討論,決定針對鄉內
            國中小所有學生,每人發給1000元助學金,經統計,全鄉共11所公立國小、兩所公立國中、
            一所私立高中,符合領取助學金者983名。 吳孟宗說,再窮也不能窮教育,四湖鄉與其他
            雲林沿海鄉鎮一樣,面臨缺乏就業機會、人口不斷外流困境,但關聖帝君非常重視孩子的教育,
            疫情讓不少家庭經濟陷入困境,孩子的教育多少受到影響,一千元助學金雖不多,卻是充滿
            關聖帝君的愛心,讓孩子知道愛心無所不在,大家會互相扶助度過疫情難關。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1632391860
    assert parsed_news.reporter == '蔡佩旻'
    assert parsed_news.title == '雲林四湖鄉國中小學生每人發1千 參天宮霸氣發助學金'
    assert parsed_news.url_pattern == '2085895'
