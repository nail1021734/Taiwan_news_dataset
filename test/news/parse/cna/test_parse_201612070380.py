import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201612070380.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            罹難人數截至7日晚間10時,已增至97人。 印尼蘇門答臘島北部亞齊省(Aceh)外海今天發生
            規模6.5強震。死亡人數已超過54人,預料還會持續攀升。中華民國駐印尼代表處表示,根據
            目前掌握的資料,沒有台灣人傷亡。 中華民國駐印尼代表處表示,截止目前為止,這場地震
            沒有造成在印尼的台灣人傷亡。 美國地質調查所指出,這起淺層地震於5時3分發生,震央
            在魯勒特鎮(Reuleuet)北方約10公里處。 印尼國家災害應變總署稍早表示,地震造成
            54人喪生,78人受重傷。105家店舖、125間屋舍及14座清真寺倒塌。 從印尼當地電視台的
            畫面中可以看到,位於震央附近、災情最慘重的畢迪賈雅縣(Pidie Jaya)到處是殘垣斷瓦
            、滿目瘡痍的景象,許多房屋傾頹崩塌,連當地人精神寄託的若干座清真寺也在強震中倒下。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1481040000
    assert parsed_news.reporter == '周永捷雅加達'
    assert parsed_news.title == '印尼6.5地震97死 代表處:無台人傷亡'
    assert parsed_news.url_pattern == '201612070380'
