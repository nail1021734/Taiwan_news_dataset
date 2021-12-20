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
    url = r'https://star.ettoday.net/news/2000174'
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
            這待遇根本是蛇生勝利組了!網友蔡佩君家中有隻非常愛撒嬌的黃金蟒「皮皮」,親人的
            牠常常被飼主笑說個性像狗一樣,沒想到牠卻還很懂得「享受蛇生」,這天蔡佩君的媽媽
            看完皮皮就笑著跟女兒說,「你的蛇很會過日子喔!」怎料她親自上樓開門一看,發現孩子
            竟然獨自爽躺在大沙發上,超粗大的腰圍全被看光光! 蔡佩君笑說,當天她的媽媽看完皮皮
            後,就下樓跟她開玩笑說,「你的蛇很會過日子喔!」讓她滿頭問號,超不解媽媽在說什麼,
            直到她親自上樓一看,才剛打開門就看見一坨黃色物體像個大爺一樣攤在沙發上,看到主人
            靠近還吐舌賣萌討摸摸,讓她哭笑不得直呼,「正常的蛇蛇不是應該躲在陰暗角落嗎,
            你給我光明正大躺沙發!」完全就是一隻超懂享受的無毛寶貝。 飼主將這段影片PO到
            臉書社團「有點毛毛的」後,網友看了也紛紛被萌翻表示,「皮皮也太爽」、「牠那個臉,
            一副“你吵我幹嘛”,可愛」、「皮皮:幹嘛沒看過蛇躺沙發嗎」、「這個腰圍比上次粗的感覺
            」、「怎麼感覺有點可愛啦」、「少了一台電視」、「皮皮可以代言最佳防疫天使了」、「
            為什麼皮皮真的可以可愛到完全沒有蟒蛇該有的煞氣,而且還超級萌的!」、「雖然我
            怕蛇,但不得說牠其實蠻可愛的」。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1622957280
    assert parsed_news.reporter == '陳靜'
    assert parsed_news.title == '媽進屋傻眼「你的蛇很會過日子喔」 牠爽躺大沙發網笑:那個腰圍'
    assert parsed_news.url_pattern == '2000174'
