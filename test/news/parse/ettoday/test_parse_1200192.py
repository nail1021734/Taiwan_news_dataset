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
    url = r'https://star.ettoday.net/news/1200192'
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
            「2018東石海之夏祭」將於7月7日至15日熱鬧登場,嘉義縣長張花冠為了宣傳活動,特別拍了
            一支「假直播」短片,片中聲稱自己才25歲,最會飆車、飆人和飆中央,還搭上最夯話題
            「香蕉皮沾醬油」和「川金會」,讓網友大讚「縣長好幽默!」 從影片中顯示,張花冠的
            「直播房間」名叫「小花縣長張花冠」,大頭貼還用了超強美肌修圖和可愛動物鬍鬚,接著
            畫面立刻跳轉到張花冠本人在補妝,背後還有「墨鏡隨扈」。 由於背景音樂播著黃明志的
            「飆高音」,張花冠還大嗆「飆什麼高音啊飆!我今天是來開直播的,我根本不會飆高音,我
            只會飆車、飆人、飆中央!」。對於底下一名假網友「天仁中醫診所」的「脫肛請打
            080009200」回應,小花表示「脫肛就要去看醫生啊!嘉義的醫療設備很~好,而且海之夏祭
            前面會經過長庚醫院,我們有直腸外科,非常有名,順便去掛號啊!」。 由於墨鏡隨扈稱呼她
            為「縣長」,張花冠皺眉罵對方「不要隨便把我縣長身份暴露出來嘛!你不知道現在公務人員
            兼差是多麼敏感地事情嗎?害我將來都不能去大陸兼課了!」巧妙將年金改革和台大管中閔
            事件結合在一起。 不光是台灣時事,張花冠這支短片連世紀峰會「川金會」議題都有,直播
            觀眾來了北韓領導人金正恩(片中稱為金小胖),還大方「斗內」她「一顆核彈」,以及美國
            總統川普(川噗)詢問她是否20歲?今年63歲的張花冠還靦腆微笑回答說「沒有啦!我怎麼會是
            20歲~我都已經25歲啦!」。 除了金正恩和川普外,仔細一瞧,影片下方的觀眾還包括藝人
            林俊傑(JJ Lin)、韓國女團Twice台籍成員周子瑜(周紫瑜)、女神卡卡(Lady gaba)。
            最後小花轉頭看見墨鏡隨扈在吃香蕉皮,她還提到「你腦袋是不是灌了貓尿啊?吃香蕉皮,一定
            要清水煮過,再沾醬油才好吃!」。 張花冠為了宣傳「海之夏祭」的假直播影片,獲得許多
            網友的回應「哈哈會笑死」、「沒有湯豪~」、「無限支持小花縣長轉職當網紅」、「我剛看
            新聞後面那位男生很好笑」、「我到底看了什麼」,甚至還有人貼出「派出所嗎?友人拐我
            按讚」圖片。 小花還幽默回答上述網友「你怎麼還活著?」、「他帥到不來」、「你要
            斗內嗎?」、「你不要打我隨扈的主意」、「你看了FB」,以及「都這麼大把年紀了,還被
            壞人拐,我好同情你。」
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530094980
    assert parsed_news.reporter == '袁茵'
    assert parsed_news.title == '快斗內!張花冠「超強美肌」開直播 嬌羞回:人家才25歲~'
    assert parsed_news.url_pattern == '1200192'
