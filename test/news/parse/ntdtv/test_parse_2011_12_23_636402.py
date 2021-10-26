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
    url = r'https://www.ntdtv.com/b5/2011/12/23/a636402.html'
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
            英國尋寶獵人達倫.韋伯斯特(Darren Webster)在蘭開夏郡錫爾弗代爾的一片田地上發現
            了維京海盜1000多年前埋葬的寶藏,目前,這批包括大量銀幣和珠寶飾品的寶藏在大英博物館
            展出。 這批寶藏中有27枚銀幣,其中一枚是此前從未記錄過的類型,專家們認為銀幣上的
            名字指的是英格蘭北部一位未知的維京領袖。這個名字是“埃爾德考納特”(Airdeconut),
            據信代表斯堪的納維亞的名字“哈薩克努特”(Harthacnut)。还有一枚銀幣上面鑄有
            “Alwaldus”(阿爾瓦杜斯)這個名字,可能是指阿爾弗雷德大帝(King Alfred)的
            侄子。 這枚銀幣的發現駁斥了一種頗爲流行的想法,認爲維京海盜都是憎恨基督教幷搶劫
            修道院的异教徒。銀幣的一面鑄有“DNSREX”(DNS代表Dominus,意爲上帝),說明很多
            維京海盜在英國定居後不久皈依基督教。 據悉,這批寶藏是公元900年左右埋入地下的,當時
            維京海盜正與盎格魯撒克遜人作戰,企圖控制英格蘭北部地區。大英博物館表示,這是近年來
            發現的最重要的維京海盜寶藏之一。基於此前的發現,這些財寶的價值達到50萬英鎊
            (約合77萬美元)。不過,據大英博物館中世紀早期錢幣館負責人加雷斯-威廉斯博士估計,
            如果按照當時的價值計算,這批寶藏只能買下一小片土地,一大群綿羊或者一小群牛。 這批
            寶藏將交到大英博物館或者當地博物館手上,並將由獨立專家委員會對寶藏價值進行評估,
            如果希望收藏這批寶藏,博物館需要按照市價支付給發現者和土地擁有者,如果放棄收藏,寶藏
            將歸發現者和土地擁有者所有。據悉,蘭開斯特博物館已决定買下這批寶藏,達成交易後,所
            支付的款項將由韋伯斯特和土地擁有者平分。
            '''
        ),
    )
    assert parsed_news.category == '海外華人,歐洲'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324569600
    assert parsed_news.reporter is None
    assert parsed_news.title == '千年維京海盜寶藏 驚現英國農田'
    assert parsed_news.url_pattern == '2011-12-23-636402'
