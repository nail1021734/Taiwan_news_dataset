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
    url = r'https://star.ettoday.net/news/1200085'
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
            美國紐約北部農場的小牛Bonnie才4個月大就被迫與母親分離,去年夏天牠被再去賣掉,途中
            逮到機會幸運逃進森林裡,而農場人員無論如何都找不到牠。動物救援機構Farm Sanctuary
            發現,小牛竟然出現在森林的監視畫面裡,更令人驚訝的是小牛已是「鹿家族」的
            一員。 Farm Sanctuary的動保員Meredith Turner-Smith表示,「整個冬天森
            林裡都被3英尺高的厚雪覆蓋住,偶爾能看見Bonnie的蹤影,由於太小就被迫和牛群分離,逃
            亡後遇到這群鹿了,所以習性與鹿越來越接近,只要一見到人,就會警戒地立刻躲避。」 僅
            管Bonnie幸運在森林生存下來,但牠不適合在這片酷寒森林中生活,好險好心居民Becky願意
            幫助牠。Becky知道牛不易穿越有厚厚積雪的樹林,所以一路協助並提供水、食物還有乾淨
            的棉被,總算慢慢贏得了信任。後來Becky向Farm Sanctuary請求幫忙,但Bonnie已經把森林
            當作家,要說服牠離開森林是相當困難的挑戰。 經過3次努力,Bonnie終於被引到達樹林裡,
            救援人員在牠的周圍建立一個圍欄,並在食物裡摻了微量鎮定劑,才順利將這頭被鹿養大的
            牛帶回Farm Sanctuary的牛舍。Bonnie在農場醒來,發現身處舒適的牧場和穀倉,馬上就知
            道這裡才是對的地方。雖然不得不離開鹿族群,但是牠很快就交到了許多新朋友,而
            Meredith Turner-Smith也說,「Bonnie順利從樹林來到救援中心,辛苦通過這項艱鉅
            挑戰,現在有好多人關懷與愛護牠。」
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530093600
    assert parsed_news.reporter is None
    assert parsed_news.title == '4月小牛跳「屠宰車」逃進森林 被「鹿家族」收養帶大'
    assert parsed_news.url_pattern == '1200085'
