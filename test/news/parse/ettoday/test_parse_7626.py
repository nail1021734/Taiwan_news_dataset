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
    url = r'https://star.ettoday.net/news/7626'
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
            蕭敬騰出道才短短四年,商演和代言接不停,去年賺超過1億台幣,花大錢買房不手軟,名下
            房產的總值高達8000萬。但可能因為有點高調說溜嘴,被國稅局盯上,查稅以外還要蕭敬騰
            把收入來源說分明。 蕭敬騰被媒體稱為「省話一哥」,先前卻不小心說溜嘴,透露自己名下
            有3間房子,《蘋果日報》報導他去年花3000萬買房,今年年初又花5000萬購入兩戶預售屋
            ,未料被國稅局盯上。 依內規,25歲以前就擁有過多房產者,較受到國稅局關切,蕭敬騰因而
            被稅官盯上,清查他名下的房子是不是親人所贈與,是否有涉及「贈與稅」的問題,經紀公司
            二個月前收到查稅信函,希望蕭敬騰將買房資金、所得稅帳目說清楚。 經紀公司提出蕭敬騰
            相關的收入與繳稅證明後,已經還給蕭敬騰一個清白。經紀人Summer透露蕭敬騰是知名人物
            ,不可能因小失大違反稅法相關規定,所以他雖然被查稅但他不擔心。經紀人也表示日前會對
            25歲以下的藝人特別管理,以免理財理出問題。 此外,據稅務人員的說法,目前蕭敬騰的
            財產狀況並無爭議,證明省話一哥很老實。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1321585320
    assert parsed_news.reporter is None
    assert parsed_news.title == '蕭敬騰高調買房被抓包 國稅局要他說分明'
    assert parsed_news.url_pattern == '7626'
