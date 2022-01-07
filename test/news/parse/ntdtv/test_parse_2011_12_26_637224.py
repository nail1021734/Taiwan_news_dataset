import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/26/a637224.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            聖誕節的顏色以紅綠為主,五顏六色。但我們常常在聖誕節期間聽到白色聖誕這個說法,這是
            怎麼回事呢,讓我們一塊兒來了解詳情。 人們嚮往白皚皚的聖誕節 聖誕節的傳統就是音樂
            瀰漫在空氣中,彩色燈光在窗前閃耀,孩子們興奮地打開家人和朋友贈送的禮物。 另一個
            傳統可以說就是下雪了,至少是在世界的北部,在冬季來臨不久之後就迎來聖誕節了。世界
            很多地方在聖誕節這一天會趕上雪花飄飄,白雪就像一塊地毯覆蓋大地。這就是人們所說的
            「白色聖誕」。當然很多地方聖誕節期間不下雪,而且有些地方在這個季節氣候還挺炎熱
            的呢。喜歡白雪皚皚,但生活在溫暖地帶的人們只能在夢中享受白色聖誕了。 美國歌曲作者
            歐文.柏林在他的歌曲中抓住了人們的這種情感,歌頌了「白色聖誕」,成為經久不衰的最受
            歡迎的歌曲之一。 歌詞出自猶太作者之手 歌曲一開始,解釋了為什麼歌者夢想經歷一次
            白色聖誕。很多人從來沒有聽過這首曲子的歌詞,因此不了解歌曲的真實意義。這首歌是
            這樣開始的: 「太陽光明溫暖,草地碧綠新鮮,桔樹椰樹隨風搖動,我在加州比佛利山莊
            從沒有見到過那種景象。聖誕前夜這一天,我渴望北上,看看寒冷多雪的北方,而不是溫暖而
            陽光明媚的南方。」 多年來,數百名歌手和樂隊都錄製過「白色聖誕」這首曲子,但是很多人
            最了解的是賓.克羅斯比演唱的這首歌。 歌曲作者歐文.柏林1888年生於俄羅斯,他並不把
            聖誕節作為節日慶祝,因為他是猶太人。 但是他譜寫的這首歌曲慶祝了一種和平與幸福的
            理念,使每個人,不論他生活在哪裡,不論當地是白雪皚皚還是陽光明媚,都可以分享。
            '''
        ),
    )
    assert parsed_news.category == '國際專題,聖誕節'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324828800
    assert parsed_news.reporter is None
    assert parsed_news.title == '「白色聖誕」一詞的由來'
    assert parsed_news.url_pattern == '2011-12-26-637224'
