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
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640096.html'
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
            越南瘋跨年,從河內還劍湖的迎接2012年新年倒數計時,及台商與代表處共同舉辦的年冬終
            尾牙餐會,大家一起迎接新的一年。 河內知名景點還劍湖的大舞台五光十色,主持人與現場
            民眾共同倒數計時,「5、4、3、2、1,新年快樂」歡迎2012年到來,現場民眾陷入狂熱,與
            舞台上的節奏一同舞動。這是河內民眾最high的一刻。 河內市政府並在還劍湖畔街道舉辦
            第3屆花卉節,許多民眾在傍晚時分就到達現場賞花,並且等待倒數迎接新年的到來。還劍湖
            街道上人潮擠得水洩不通、萬頭攢動。 另外,今年河內台灣商會年終尾牙餐會,由駐越南代表
            處和河內台灣商會主辦、海防台灣商會和太平台灣商會協辦,以「慶祝中華民國開國一百
            週年暨河內台灣商會年終尾牙餐會」為名擴大舉辦。 現場有來自胡志明市、平陽、蜆港、
            頭頓等地的台商與會,大家互道新年快樂,並交換對於來年越南市場商機。越南官員和越南
            留學台灣學生多人也參加餐會,主辦單位並準備豐富抽獎禮品,使得今年的餐會格外
            熱鬧。 在越南許多地方,民眾與三五好友在餐廳、公園等地一同喝茶或喝酒,歡迎新年的
            到來,大家一同互祝來年健康幸福,國泰民安。
            '''
        ),
    )
    assert parsed_news.category == '法輪功,各界恭賀李洪志先生新年好'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325347200
    assert parsed_news.reporter is None
    assert parsed_news.title == '越南瘋跨年 台商熱鬧聚會'
    assert parsed_news.url_pattern == '2012-01-01-640096'
