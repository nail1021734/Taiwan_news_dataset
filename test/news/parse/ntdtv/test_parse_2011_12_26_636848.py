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
    url = r'https://www.ntdtv.com/b5/2011/12/26/a636848.html'
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
            英國倫敦虹妮舞蹈學院(Honeys Dance Academy)是一所寶萊塢表演藝術學院。12月17日
            晚,該學校舉行了聖誕聯歡晚會,暨年度頒獎典禮。優美歡快的寶萊塢舞蹈讓來賓體驗到了
            節慶氣氛。下面請看本臺記者來自倫敦的報導。 12月17日晚,在北倫敦哈羅市的嘉華中心
            禮堂(KPS Center),來自虹妮舞蹈學院的學生,家人和包括當地市政府官員,社區領袖等
            特別來賓共200人參加了這次名為寶萊塢聖誕晚會的活動。 虹妮舞蹈學院的創建人,著名的
            寶萊塢舞蹈家和編舞家虹妮-卡拉婭(Honey Kalaria),13歲就成為職業舞蹈演員,現在她
            熱心的致力於教授年輕人舞蹈。她表示,商業的成功只是她全力服務年輕人的「副產品」:
            我們不只是教他們個人的發展和舞蹈技能,我們還教他們身心的結合。而精神方面我們教他們
            打坐。那是我在十幾年來一直在做的,我教所有的學生打坐。通過日常的打坐練習,我感到
            有助於讓年輕人或任何人成為更加平衡的個人,內心變得更加平和。 當天晚上的活動中還
            宣佈了由她設立的慈善機構,虹妮-卡拉婭基金會,並舉行了一項特殊的頒獎儀式,為該學院的
            學生授予被認可的寶萊塢舞蹈資格證書,這也是歷史的首次。卡拉婭曾與著名的印度明星同臺
            在皇家大匯演(Royal Variety Show)中為女王表演。她經常被稱為「英國寶萊塢大使」
            和「寶萊塢舞蹈女王」。她還是英國最傑出的三位亞裔女企業家之一,由她編導的減肥舞蹈
            《寶萊塢測試(Bollywood Workout)》風靡全球。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324828800
    assert parsed_news.reporter == '文沁,冠齊英國倫敦'
    assert parsed_news.title == '英倫敦虹妮寶萊塢舞蹈學院聖誕晚會'
    assert parsed_news.url_pattern == '2011-12-26-636848'
