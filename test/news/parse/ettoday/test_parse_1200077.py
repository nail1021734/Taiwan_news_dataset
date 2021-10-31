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
    url = r'https://star.ettoday.net/news/1200077'
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
            說好的驚喜包呢?新北市板橋的飼主李緒娟日前在臉書分享一則貼文,內容是她在整理照片
            的時候,發現愛犬妹妹這7個月來怎麼都長一模一樣,讓她忍不住笑說,「別人是驚喜包,我們
            是灌風包。」貼文一出瞬間累積2千多個按讚數,而妹妹超萌的模樣也融化了網友們。 馬麻
            透露,自從去年走了一隻黃金女兒後,本來不打算再養了,但無意中在網路上看到了模樣可憐
            的妹妹,一眼就非常喜歡,最後經過許多嚴格的審核後,終於領養到牠。李緒娟說,「擁有妹妹
            感覺更幸福了,黑色的毛孩浪浪太多,但對許多人來說似乎不怎麼討喜,希望大家可以多多
            領養黑色毛孩。」 自從妹妹進到家的第一天,馬麻就常常為寶貝拍攝每日生活點滴,不過
            一個月又一個月的過去後,她發現妹妹每個階段都沒什麼變化。李緒娟表示,「因為常看到
            網友貼文說,米克斯都是大驚喜包,後來回頭看看,為什麼我家的一點都不驚喜?不過網友後來
            說不驚喜其實也是一種驚喜,我想想好像也是吼哈哈!」 馬麻將妹妹2個月的照片和7個月時
            的照片,分享到臉書寵物社團後,不到一日就有2千多個按讚數,網友們看了紛紛笑說,「真的
            都沒變!只是放大了好萌」、「好可愛呀,那眼神一模一樣」、「臉還是一樣萌」、「眼神都
            一樣溫柔」、「怎麼連姿勢也一樣阿XDD」。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530100140
    assert parsed_news.reporter == '吳鎮良'
    assert parsed_news.title == '照了放大燈~黑美人7個月來「都長一樣」 媽笑:養到灌風包'
    assert parsed_news.url_pattern == '1200077'
