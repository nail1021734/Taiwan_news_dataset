import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/22/a635455.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            菲律賓官員周三表示,上週該國南部洪災中的死亡人數已經超過1000人。有關官員預計,死亡
            人數還會增加。 熱帶風暴上星期五夜晚橫掃菲律賓南部,在24小時降下相當於一個月的
            雨量,引發幾次嚴重的暴洪。 救難人員集中在棉蘭老島(Mindanao)北方的海域進行搜救
            任務,希望能找到更多遺體,甚至是生還者。 菲律賓民防處處長拉莫斯(Benito Ramos)
            表示,救援人員已經找到1002具屍體,許多人仍然下落不明。 受災最嚴重的地區在
            卡加延德奧羅(Cagayan de Oro)和伊里甘( Iligan)兩個城市,造成27萬5千多人
            無家可歸,難民被安置在各個疏散地區。 菲律賓民防處預估,這次洪災摧毀的公共建設、學校
            及醫院,損失近十億披索。菲律賓農業部則表示,以稻米和小麥為主的谷物,損失超過1千
            5百萬披索。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324483200
    assert parsed_news.reporter == '陳宇平'
    assert parsed_news.title == '菲律賓風災超過千人喪生'
    assert parsed_news.url_pattern == '2011-12-22-635455'
