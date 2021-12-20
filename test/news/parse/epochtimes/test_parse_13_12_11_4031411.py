import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/13/12/11/n4031411.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            泰國反對黨民主黨領袖、前副總理蘇德(Suthep Thaugsuban)宣佈成立未經選舉的「人民
            議會」遭質疑。 目前泰軍方尚未表態。 據中央社報導,蘇德星期一(9日) 晚要求英祿在
            24 小時內辭職。 而泰國總理英祿(Yingluck Shinawatra)亦於星期一( 9 日)晚宣
            佈解除國會眾議院,並在60天內( 明年2 月2 日)舉行大選。 泰國示威團體領袖蘇德
            隨後表示,選舉並非他們的目標, 他於星期二(10日)晚又以「英祿政府不清廉
            ,人們無法忍受英祿和其看守政府為由」,宣佈他們將成立人民政府。 按照蘇德的說法, 他
            們這個由各方指定的代表組成的「人民政府」將自行上台,並用8 -15 個月的時間進行國家
            改革,等改革完成後,再進行選舉。他還呼籲政府官員向「人民政府」效力。 但蘇德所屬的
            在野民主黨已經20 多年沒贏過大選,而2011年的上次大選之中,泰國前總理他信的妹妹英祿
            所屬的泰黨(Puea Thai Party)則以壓倒性票數大勝。蘇德也知道,就算提前大選,該黨勝出
            的可能性不大,因此持續呼籲成立這個未經民選的「 人民政府」,並要求設立「 人民議會
            」取代國會。 泰國的很多專家對此舉動表示質疑,他們認為應該使用民主方式控制他信前
            政府和英祿現政府的貪腐,並進行政治改革, 不支持這種鼓動精英中產階級示威抗議來取代
            民選政府的方式, 認為這種方式會導致流血和衝突。 目前泰軍方的態度看似中立,泰陸軍
            發言人溫泰(Winthai Suvaree)表示,泰陸軍司令帕拉育(Prayut Chan-O-Cha)正嚐試
            儘快找出解決問題的方法。英祿當政兩年半來一直在積極拉攏軍方,但如果泰國又出現
            數十萬人上街抗議事件, 軍方或有可能再次重演2006年驅除前泰國總理他信的軍事政變。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386691200
    assert parsed_news.reporter == '馬穎慧,李緣'
    assert parsed_news.title == '泰反對黨擬自行上台 軍方未表態'
    assert parsed_news.url_pattern == '13-12-11-4031411'
