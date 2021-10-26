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
    url = r'https://www.ntdtv.com/b5/2011/04/09/a516789.html'
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
            荷蘭西部城鎮阿爾芬(Alphen aan den Rijn)的官員表示,1名男子今天在鎮上購物商場
            開槍,擊斃5人並槍傷至少13人,而後掉轉槍口自殺。 阿爾芬鎮的代理鎮長尹荷恩
            (Bas Eenhoorn)在記者會表示:「1名持自動武器的男子開槍濫射,殺死5人後飲彈自盡。
            我們不便透露他的身分。另有4人受重傷,7人受較輕的傷,2人受輕傷。」 尹荷恩表示,
            這次事件發生在利得荷購物中心(Ridderhof),「1名持自動武器的男子對民眾開火,當時
            商場內滿是全家一起光顧的顧客,有不少孩子」。 他說犯案男子是單獨行凶,但他並未透露
            凶嫌身分。目擊者說,凶手大約20來歲。 這起槍擊案令商場裡的民眾大為恐慌,許多人害怕
            犯案槍手不只一人。警方抵達現場後立即疏散民眾。 目擊者告訴國營NOS電台,犯案男子
            手持機槍,似乎是隨意濫射。 荷蘭國家通訊社(ANP)報導,據商場內一家寵物店的老板表示,
            凶手以自動武器對身邊民眾開火,子彈要打完時,舉槍轟自己的頭部自盡。 阿爾芬位於大城
            阿姆斯特丹(Amsterdam)南方約46公里,有7萬2000人口。
            '''
        ),
    )
    assert parsed_news.category == '海外華人,歐洲'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302278400
    assert parsed_news.reporter is None
    assert parsed_news.title == '荷蘭男子商場濫殺 6死13傷'
    assert parsed_news.url_pattern == '2011-04-09-516789'
