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
    url = r'https://star.ettoday.net/news/1200025'
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
            新竹一名張姓美魔女人妻想玩3P援交,以各2萬5000元的價碼找上蔡姓男子和另名男子,被
            尾隨在後的老公抓姦在床。但檢方認為,張女告知蔡男自己單身,隱瞞已是人妻的身分,因此
            通姦部分對蔡做出不起訴處分。 《自由時報》報導,張女的丈夫指控,蔡男2017年4月在約砲
            網站認識妻子,明知她已婚,還約去飯店發生關係;他發現妻子為何半夜還要出門,於是一路
            跟蹤,驚見妻子和蔡開房。他控訴,用手機拍下兩人的畫面,結果遭蔡搶手機、動粗,控告對方
            傷害、通姦和強盜。 張女坦承,因想玩3P,在網路上認識蔡男,告訴對方自己是單身,並以
            每人2萬5000元的價錢,約蔡及另名男子一起開房間。蔡男說,自稱單身的張女主動傳訊息
            給他,才會談好價錢約在飯店;當時是張女丈夫一直拉扯,所以才會受傷;他見對方錄影,是
            想要撥掉他的手機,並無強盜意圖。 新竹地檢署認為,由於張女跟蔡男說單身,因此通姦部分
            對蔡不起訴;且林男未說明,蔡以何種方式動粗,自己傷到哪部位,因此傷害不起訴。檢方說,
            蔡對林的手機沒有不法所有意圖,強盜部分也不起訴。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530067440
    assert parsed_news.reporter is None
    assert parsed_news.title == '「每人2萬5」約2男3P!美魔女人妻半夜溜出門援交 夫跟蹤抓姦'
    assert parsed_news.url_pattern == '1200025'
