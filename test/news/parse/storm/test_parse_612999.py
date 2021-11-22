import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/612999?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            出國旅行,機票往往就佔了旅行預算的一大半,要怎樣才可以搶到超便宜機票?另外不想
            花時間規劃行程的朋友,可能會選擇跟團,但原來跟團旅遊也隱藏了不少地雷!不想美好
            的旅行,最後卻玩得不開心?旅遊作家謝哲青、機票達人布萊N、藝人李懿,還有主播張佳如,
            教您如何避免旅遊陷阱! 想買便宜機票卻總是抱怨搶不到?其實搶機票並非想像中的那麼難!
            機票達人布萊N大方公開搶票五大守則,只有跟達人一樣花點功夫,保證再也不會錯過
            平價機票! 然而不少便宜機票背後,其實都隱藏著一定的風險,一不小心不但會讓你浪費時間,
            甚至還會損失了機票錢。不想因為機票而影響到你的出遊心情,達人教你避開三大機票地雷,
            讓你真正省錢出國! 有些朋友為了節省規劃行程的時間,或是跟長輩出遊時,都會選擇跟團
            去旅行。然而跟團旅遊就可以讓你安枕無憂嗎?一不小心可能還是會落入旅行社的陷阱中!
            要如何避免不肖業者的不當行銷手法,在國外跟團時遇到狀況,又要如何自保?
            '''
        ),
    )
    assert parsed_news.category == '風生活,國內,財經,影音,人物,風影音'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541964600
    assert parsed_news.reporter == '下班經濟學'
    assert parsed_news.title == '出國必看!坐頭等艙竟這麼簡單?旅遊達人揭航空公司、旅行社不告訴你的內幕!'
    assert parsed_news.url_pattern == '612999'
