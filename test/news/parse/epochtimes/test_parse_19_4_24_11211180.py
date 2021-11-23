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
    url = r'https://www.epochtimes.com/b5/19/4/24/n11211180.htm'
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
            享譽盛名的加拿大王室馬戲團(Royal Canadian Family Circus)「奇觀2019」
            (SPECTAC!2019)將從5月9日~8月18日在卑詩省、阿爾伯塔省和安省的10個城市巡演,總計
            演出108場;帶來一套「全新的、充滿了爆炸性的節目。」 加拿大王室馬戲團擁有52年的
            歷史。「奇觀2019」將捕捉你童年時代的所有馬戲團的懷舊情緒,讓你感受現代的曲折和迷人
            的刺激。在大頂之下,看著驚人的飛行家和驚險的空中飛人,敏捷的雜技演員和令人眼花繚亂
            的雜耍者,你將感到驚心動魄、心曠神怡、和流連忘返! 「奇觀2019」將為觀眾奉獻傳統及
            現代馬戲節目,如驚險的命運之輪、高空鞦韆、中國雜技表演、空中摩托車特技等,非常適合
            全家老少觀看。 加拿大王室馬戲團由著名的馬戲團班主約瑟夫‧多米尼克‧鮑爾
            (Joseph Dominik Bauer)領隊,彙集了全球身懷絕技的頂級馬戲演員。 來自馬戲表演
            世家,至今已是第九代馬戲世家的約瑟夫‧鮑爾在馬戲表演界享有盛望。他還將表演他的拿手
            好戲——高難度、險象環生的命運之輪(Wheel of Destiny),令人歎為觀止。 來自南美
            哥倫比亞的空中雜技絕活(THE FLYING CORTES FAMILY),由Robinson Cortes,他的
            妻子和家人,在空中精心運作、難以置信的雜技雙人、三人和四人動作。著名的Cortes一家
            曾在世界各大馬戲團中演出,獲得了國際馬戲團獎,曾多次在國家電視台播出。 中國雜技團將
            給觀眾表演高難的中國傳統的平衡、雜技等。他們超越極限的椅子平衡、花瓶平衡,扭曲、
            空竹等特技將給觀眾帶來難忘的記憶。 您還將欣賞獨特的平衡表演
            (The ROLA BOLA ARISTOV)。來自俄羅斯的喬治‧阿裡斯托夫在懸浮在空中時執行各種
            手部平衡運動技能,令人難以置信的旋轉和旋轉錯覺是通過快速和激烈的精確手眼協調來完成
            的! 您還將見證激動人心的多明格斯摩托車環球(XTREME DOMINGUEZ Family Motor
            cycle Globe)的技能和勇敢的壯舉。這些飛速、勇敢的表演,沒有絲毫瑕疵的餘地,來自
            哥倫比亞的第8代馬戲世家繼續將其演出推向極限。 精采馬戲的普通票只有25元。
            '''
        ),
    )
    assert parsed_news.category == '加拿大,溫哥華,新聞,社區活動預告'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1556035200
    assert parsed_news.reporter is None
    assert parsed_news.title == '「奇觀2019」加拿大王室馬戲團將在加拿大巡演'
    assert parsed_news.url_pattern == '19-4-24-11211180'
