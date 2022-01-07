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
    url = r'https://www.ntdtv.com/b5/2011/04/02/a513571.html'
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
            中華民國駐越南代表黃志鵬,4月1日率越南台灣商會聯合總會總會長廖育珠和林同省台灣
            商會會長呂佳真等人拜會林同省省政府,受到副省長阮文淵的熱情歡迎。 黃志鵬和阮文淵就
            台商在當地投資遇到的困難、台越高等教育的合作,林同省如何協助台商等議題廣泛意見交換,
            台商代表並表達在林同省投資遇到有關稅務上的困擾,希望省府能解決。 黃志鵬特別感謝
            林同省給予台商良好的投資環境,以及善待台商;阮文淵高度肯定台商對當地的貢獻,特別是
            所佔投資比率之高和對當地就業率的協助。 阮文淵期盼台商能繼續遵守越南法律,希望台商
            能 在越南創造更多的財富,和協助林同省的發展。阮文淵 並期望台灣能在當地進行高等教育
            和科技產業的投資。 黃志鵬並表達,台灣各界希望能和林同省進行更深 入交流;與會台商
            表達,稅收方面,希望省政府方面能多與台商溝通,阮文淵同意,當場表示將在4月間與台商
            舉辦一場研討會,邀請稅務單位與會,向台商說明省方在稅收上的立場和做法。 會面是在
            林同省省政府進行,雙方交談愉快,過程約1小時。黃志鵬和阮文淵都認為,這是一次具有
            建設性的會面。 駐胡志明市台北經濟文化辦事處處長楊司恭、林同省台灣商會副會長
            黃啟峰等人都參與拜會。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1301673600
    assert parsed_news.reporter is None
    assert parsed_news.title == '黃志鵬率台商拜會越南林同省'
    assert parsed_news.url_pattern == '2011-04-02-513571'
