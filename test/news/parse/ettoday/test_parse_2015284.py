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
    url = r'https://star.ettoday.net/news/2015284'
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
            「誰都束縛不了本汪自由的靈...沒事!」高山犬「萬金」這天和飼主Emily Teng對視一眼,
            發現自己要被上鍊子就開始衝刺逃亡,任憑媽媽怎麼呼喊也不回頭,直到聽見她大喊一聲,
            「等下讓我抓到你就死定了,我扒了你的皮!」狗狗才突然乖乖停下,回頭用害怕的眼神求饒,
            超人性化的行為讓網友紛紛笑翻。 萬金是個大醋桶,平時對路邊的狗狗都很友善,但只要
            對方接近媽媽就會非常生氣。Emily Teng解釋,「其實當天有狗崽來日托,安全起見,
            幼犬出來吃飯前,我就讓金金先上鏈,因為日托的小朋友被我抱上抱下一整天了,
            醋桶金非常不高興。」但萬金又覺得還沒玩夠,所以發現要上鍊就開始狂奔
            。 有趣的故事分享到臉書社團「有點毛毛的」,網友紛紛笑翻表示,
            「阿母的獅吼功果然名不虛傳」、「媽媽好恐怖,虎姑婆來了」、「
            金金表示:能一個打十個的麻麻不能惹」、「扒皮太痛了!還是識時務的停下來好了
            」、「牠當時害怕極了」、「阿金本來就很乖,不想讓老木扯破喉嚨而已啦。」、「
            媽媽是不是在牠的面前扒過誰的皮?」
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1624716300
    assert parsed_news.reporter == '魏筱芸'
    assert parsed_news.title == '高山犬爆衝拒上鏈! 聽到「扒了你的皮」秒煞車回頭求饒'
    assert parsed_news.url_pattern == '2015284'
