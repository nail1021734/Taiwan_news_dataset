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
    url = r'https://star.ettoday.net/news/1200000'
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
            開車上路最怕遇到三寶!黃姓駕駛26日行經新北市汐止中興路與工建路口時,一名機車騎士
            突然從左側逆向超車,原本想帥氣地滑向車道右側,沒想到才2秒就撞上路邊違停的計程車,
            當場摔飛落地,嚇得目睹整個過程的他連飆髒話,「嚇一跳,XX的是在衝三小!」 影片中,
            只見騎士逆向超車後先是騎在雙黃線上,接著屁股一歪想從左邊快速切到
            右邊,試圖超過前方的藍色小貨車,沒想到路邊竟然停著一輛計程車,他雖然立即反應扭動龍
            頭想切進兩車之間的縫隙,無奈車頭閃開車身卻來不及調正,直接正面撞上小黃的左後車尾,
            整個人在空中翻了半圈才摔倒在路中央。 開在後方的黃男被這突如其來的車禍嚇了一跳,
            除了放慢速度閃過外,還連飆一連串髒話,事後他將這段13秒的驚險影片上傳到個人臉書及
            「爆料公社」並表示,「哥(騎士)你想死自己去,不要害我差點輾過去,閃一個翻車險些撞到
            對向公車,遇到這種想煞車也來不及,還好公車還沒來才能閃過。」 其他網友看到PO文特地
            跑到黃男的臉書看無消音的版本,還不忘留言調侃,「原PO罵得好流利」、「這完美的滿分
            」、「小黃雖然是違停,但這也太衰」、「怎麼感覺摔得有點華麗」、「看起來像在打保齡
            球」、「死角也敢這樣騎,三寶果然是地球最強的生物」;他則自嘲回應,「嚇到髒話一堆,
            差點變成殺人凶手,還好沒事不然賠不完。」
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530059940
    assert parsed_news.reporter is None
    assert parsed_news.title == '逆向超車一個扭屁move 騎士帥2秒遭小黃擊落倒栽摔飛'
    assert parsed_news.url_pattern == '1200000'
