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
    url = r'https://www.epochtimes.com/b5/13/12/30/n4046768.htm'
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
            俄羅斯南部的伏爾加格勒、昨天才發生火車站炸彈恐怖攻擊,造成17人喪命,今天又傳出一起
            路面電車的爆炸,至少有14人死亡28人受傷,由於索奇冬運明年2月就要登場,連續2天的2起
            恐怖攻擊,不免讓外界對俄羅斯的維安感到憂心。 整輛電車被炸到玻璃全碎,就連車頂也都
            全空,現場只遺留乘客的包包,俄羅斯南部的伏爾加格勒、星期天才發生火車站自殺炸彈攻擊,
            30日又傳出路面電車遭自殺炸彈攻擊,由於事發地點就在熱鬧的市場附近,而且又是上班的
            尖峰時刻,因此死傷相當慘重,目前當局鎖定一名男性嫌犯,強大的爆炸威力,不只炸毀電車,
            就連附近住家,也都被炸到門窗全碎,趕到現場的警方封鎖街道,救難人員在雪中搶救
            傷患。 29日同樣在伏爾加格勒,也發生一起嚴重的爆炸攻擊,地點是在熙來攘往的火車站,
            爆炸發生瞬間,被對面的監視器拍下整個過程,由於威力強大,連攝影機都跟著晃動,車站爆炸
            發生當時,因為火車大誤點,所以擠滿許多等車的乘客,俄國當局表示,這是一起預謀的恐怖
            攻擊,初步判定,火車站炸彈犯是去年被俄國通緝的黑寡婦亞斯娜諾娃,她曾2度與恐怖份子
            結婚,2任丈夫都被圍剿。 雖然目前沒有組織坦承犯案,但車臣叛軍領袖烏馬羅夫幾個月前
            曾揚言,要對俄國平民百姓發動攻擊,其中也包括索奇冬季奧運,事實上,這已經不是
            伏爾加格勒第一次發生炸彈攻擊,10月21日,也有一名女性炸彈犯在公車上發動攻擊,造成
            7人死亡,總統蒲亭已經下令,各地火車站和機場加強維安,希望2月7日索奇冬運能夠平安登場。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388332800
    assert parsed_news.reporter is None
    assert parsed_news.title == '俄羅斯恐怖攻擊 電車爆炸14死'
    assert parsed_news.url_pattern == '13-12-30-4046768'
