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
    url = r'https://star.ettoday.net/news/1200312'
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
            聯電創辦人曹興誠發表一段「兩岸和平程序」視頻,具體建議兩岸和平共處的方案,認為應該
            從台北、北京、華府三方關係中,找到「和平的等號」。影片中他特別推崇民進黨的「台灣
            前途決議文」,因為該份文件開宗明義提出「台灣(即中華民國)是一主權獨立國家,任何有關
            獨立現狀的更動,必須經由台灣全體住民以公民投票的方式決定。」 可以見到影片一開始
            寫著,「曹興誠:以科學和宗教智慧化解藍綠內鬥擊兩岸危機」,首先他質疑,「兩岸問題的
            解決,非得靠政客或是政黨嗎」、「如果政客或政黨只想挑撥群眾,惡化問題,大家該怎麼辦?
            」緊接著,又寫到「曹興誠,過去台灣科技界的要角,現在是創新型的佛教徒,提出一個簡單
            有力的解答,聽過的人都感到振奮。」然後呼籲大家,請勿錯過這個人人可以參與的
            創新。 曹興誠表示,現在住在台灣的人可能都覺得煩悶,因為藍綠不斷的惡鬥,台灣與大陸
            關係更是陷入低潮,面對陸方的武力威嚇似乎毫無頭緒,然而這一切並不是沒有解決辦法,而是
            要依靠網路傳播的方式,還有科學與宗教所給予的智慧,有了這些都可以找到一切的
            答案。 「台灣前途決議文」明確指出,台灣就是主權獨的國家,沒有獨立的問題,但是民進黨
            卻認為,決定國家的是全體住民不是民進黨,所以不排除藉由公投來決定是否統一。反觀大陸
            的「反分裂國家法中」,第五條寫到「以和平方式實現祖國統一,最符合台灣海峽兩岸同胞的
            根本利益」,而所謂的「和平方式」沒有明確定義根本很籠統,所謂和平方式,要台灣同胞接受
            的方式,才能稱之為「和平方式」。 此外,曹興誠也不諱言台海兩岸問題,美國有重要影響力,
            除非以經排除任何和平統一的可能性,大陸才有動用武力的必要。同樣的問題曾經與民視
            創辦人蔡同榮討論時,蔡同榮當時也說「統一」這種字眼,自己根本說不出來,包括民進黨也
            只是用「獨立現狀的改變」來替代。 而國民黨所謂的「一中各表」在邏輯上就有問題,所謂
            「一中」是就一種內戰的概念,既然是內部問題何來各自表述,加上國民黨的模糊策略讓人
            失望,因為只有強者才有資格談模糊,通常弱者更應該把規則訂立明確,舉來來說,通常是貓在
            玩弄老鼠,沒有老鼠在玩弄的。 最後他呼籲,希望大家可以多傳送給朋友,在將來的各種選舉,
            不論是立委、縣市長等,都要「要求訂立兩岸和平程序、落實台灣前途決議文的主張、修訂
            公投法16條」,只要做到這些,我們就可以聯合改變台灣的藍綠對抗,改變對大陸的關係,還
            強調只要做到這樣,像是美國、日本或其他國家,就不能拿台灣成為對抗中國棋子,希望大家
            能夠仔細了解、認真思考,贊成這個方案並且傳播出去。 所以在Youtuber留言出現了像是
            「曹先生不是入籍新加坡了 這麼愛統一怎麼不入籍中國,老實說兩岸是不是統一跟新加坡人
            什麼關係」、「新加坡人你怎麼不叫你們新加坡去和中國統一?」較為偏激性的言論。
            '''
        ),
    )
    assert parsed_news.category == '大陸'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530086220
    assert parsed_news.reporter is None
    assert parsed_news.title == '曹新誠:科學與宗教可以化解兩岸危機 台灣也可以統一大陸'
    assert parsed_news.url_pattern == '1200312'
