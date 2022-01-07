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
    url = r'https://star.ettoday.net/news/1200039'
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
            馬來西亞沙巴州的亞庇市立清真寺有著美麗的建築,近日卻有2名國外女遊客攀上清真寺的
            圍牆大跳K-POP熱舞,她們穿著清涼的短褲秀出舞技,完全沒想到此舉不尊重當地風俗。
            清真寺主席拿督嘉馬沙卡蘭表示,為了維持伊斯蘭教的神聖性,將暫時禁止遊客前來
            參觀。 根據社群媒體瘋傳的影片,這兩名女遊客穿著短版上衣,隱約可看見纖細腰部,下半身
            則是快露出屁股的短褲,她們舞步一致,圍牆下方似乎還有朋友在替她們拍攝。然而,亞庇
            市立清真寺是個莊嚴的場所,當地居民以及伊斯蘭團體都痛批,女遊客根本不尊重他們的
            信仰。 除了清真寺主席下令暫時禁止遊客來參觀。馬來西亞旅遊、文化及環境部也已找到
            跳舞的這兩名遊客,但不會對她們採取任何法律行動;部長劉靜芝表示,兩名旅客並不知道行為
            的嚴重性,但她們需要了解自己的作為不尊重宗教場所。 該國旅遊、文化及環境部說明,之後
            也會與觀光業者合作,確保帶來的遊客遵守規範。據了解,這並非首次有旅客惹議,回到2015
            年,曾有4名國外遊客在馬來西亞的京那巴魯山裸體拍照,隨後遭逮捕。 兩名熱褲女脫序行為
            引發撻伐,沙巴州副首席部長兼旅遊、文化及環境部長劉靜芝指出,已對2名外國女遊客跟
            相關旅行社罰款,不會對她們採取後續法律行動。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530152820
    assert parsed_news.reporter is None
    assert parsed_news.title == '無腦熱褲女攀上圍牆跳K-POP 清真寺怒禁遊客'
    assert parsed_news.url_pattern == '1200039'
