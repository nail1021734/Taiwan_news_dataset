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
    url = r'https://www.epochtimes.com/b5/14/1/1/n4048450.htm'
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
            從雪梨、倫敦到舊金山,慶祝跨年的群眾以奢華煙火秀、大型街頭派對與創新的水果口味
            煙火霧迎接2014年來臨。杜拜更打破世界紀錄,舉辦史上最大跨年煙火秀,施放50多萬發
            煙火。 紐約市知名的水晶球今天在跨年倒數時刻降落,迎接2014年來臨時,時報廣場
            (Times Square)陷入一陣歡聲雷動,漫天五彩紙花從天而降。 從創下紀錄的杜拜煙火秀
            到雪梨與里約熱內盧,一波波壯觀的煙火秀相繼在全球各地綻放,絢爛奪目的煙火照亮黑夜,
            歡迎新的一年。 在紐約,有約100萬人冒著刺骨寒風外出,有些人甚至從清晨就開始紮營
            卡位,跟著大家一起倒數、迎接2014年。 美國最高法院大法官、土生土長的紐約客索托瑪約
            (Sonia Sotomayor)啟動機制,讓「大蘋果」紐約市重達5500公斤的知名閃亮水晶球降下,
            宣示2014新年伊始。 2014年才開端,擴音器便播放法蘭克辛納屈(Frank Sinatra)的招牌
            名曲「紐約,紐約」(New York, New York),國際太空站
            (International Space Station)3名太空人出現在巨型電視螢幕,祝大家
            新年快樂。 國家氣象局(National Weather Service)氣象專家愛德華茲
            (Roger Edwards)說,美國北部各地民眾是頂著大雪與天寒地凍外出,參加
            跨年活動。 愛德華茲說:「最大條的新聞就是天寒地凍」,他指出,北達科他
            (North Dakota)、明尼蘇達(Minnesota)與威斯康辛(Wisconsin)昨晚出現攝氏零下
            40度的低溫。 在舊金山,全球最後一批看到時針走到午夜的大城市之一,數千民眾看著
            岸邊煙火照亮金門大橋(GoldenGate Bridge)。 在更北邊多霧的西雅圖,大批群眾聚集,
            欣賞自太空針塔(Space Needle)燃放的煙火秀。 在英國,數萬人群集倫敦跨年,桃子雪與
            草莓霧隨著午夜煙火凌空而降,民眾張嘴一嚐新年「滋味」。 約5萬人親身參與了號稱
            「全球首見的多感官煙火秀」,伸出舌頭捕捉如雪飄降的各色各味煙火。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter is None
    assert parsed_news.title == '煙火秀水果煙霧 全球喜迎2014'
    assert parsed_news.url_pattern == '14-1-1-4048450'
