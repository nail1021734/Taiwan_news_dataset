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
    url = r'https://star.ettoday.net/news/1200534'
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
            美圖公司稍早在北京頤和園聽鸝館召開新品發佈會,正式發表已經提前公開過的美圖T9標準
            版,甚至還結合「頤和園」跨界合作推出了美圖T9頤和園限量版,這也是智慧型手機發展歷
            史當中,首次有手機品牌與「頤和園」進行雙品牌結合。 這款「美圖T9頤和園限量版」,機
            身圖案靈感源自中國傳統色彩——「黛綠」與「碧綠」,然後以「朱砂」點綴。 配件方面,美
            圖T9江崖鸞鳳手機保護殼的設計靈感源於頤和園經典藏品—粵繡屏風《百鳥朝鳳》,寓意吉
            祥如意;而補光燈上採用的「江崖海水」紋飾是中國的一種傳統紋樣,這個紋路讀者也很熟
            悉,就是古代龍袍上的紋路。 美圖表示,此次頤和園×美圖手機IP跨界合作,是中國皇家園林
            文化美學傳承與延續的體現,傳統藝術理念在以手機為載體的現代材質和工藝上「綻放」,
            亦是頤和園為代表的傳統歷史積澱和美圖手機所代表的現代科技的融合,彰顯了傳統精髓,
            也展現著現代年輕人表達個性張揚的潮流姿態。 這款「美圖T9頤和園限量版」確認將於8
            月上市,頤和園也宣佈將收藏這款美圖T9頤和園限量版。
            '''
        ),
    )
    assert parsed_news.category == '3C家電'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530098700
    assert parsed_news.reporter == '洪聖壹'
    assert parsed_news.title == '「美圖T9頤和園限量版」動眼看:首款為皇族御花園收藏的手機'
    assert parsed_news.url_pattern == '1200534'
