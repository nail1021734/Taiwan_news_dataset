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
    url = r'https://star.ettoday.net/news/3728'
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
            「世界新七大自然奇景」網路票選11月11日即將截止,玉山在全球440個景點中脫穎而出
            ,目前東北亞中僅和濟州島進入決賽。環保團體表示,現在華人地區只剩玉山,目前受到很大
            威脅,可能會輸給韓國,因此呼籲,「全民總動員,上網投玉山」。 世界新七大自然奇景全球
            共有400多處報名參加,包括美國大峽谷、日本富士山等。玉山山國家公園在2007年以排名
            77名擠入初選名單,在2009年因獨特的自然生態與文化資產,獲得專家青睞,進入最後的28強
            。 東海大學環境科學與工程學系副教授陳炳煌陳炳煌表示,許多台灣人不知道進入決賽是要
            重新投票的,造成玉山得票率奇低。而台灣環境保護聯盟會長王俊秀也談到,韓國人口比
            台灣多,且首爾當局很早就呼籲該國人民投票,早就成為他們的全民運動,台灣如果因此輸給
            濟州島實在不甘心。 對此,網友表示,不能輸給韓國人,大家快投玉山一票;也有人談到,
            韓國也在灌票,甚至在韓劇裡面也在催票,這種需要衝票數的玩不贏他們;還有網友嘲諷
            ,濟州島是因當年的哲男敏賢照成為了一代奇景嗎?不過,也有人認為,網路投票選的是有什麼
            公信力可言?是在比誰網路比較厲害?並認為這個票選已經只剩灌票了。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1319733120
    assert parsed_news.reporter is None
    assert parsed_news.title == '世界七大奇景玉山輸濟州島 網友:韓劇也在催票'
    assert parsed_news.url_pattern == '3728'
