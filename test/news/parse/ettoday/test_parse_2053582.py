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
    url = r'https://star.ettoday.net/news/2053582'
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
            台中市場臥虎藏龍,各地黃昏市場更有不少強手,這篇就來到大里內新市場,如果不是網友
            介紹,真沒想到這家「小食幷蔥小餅」這麼狂!下午3點開始營業,年輕小哥獨挑大樑面對
            停不住的排隊人潮,真的是用生命在煎餅,怪不得可以一賣10年生意依舊夯爆! 來台中10
            多年,現在才第一次知道大里有個內新黃昏市場,位置倒是不難找,就在大里公園附近,佔地
            大停車位算不少,不過還是要早點來,因為一過三點整個人潮湧現停車位也難求,這個市場
            攤位相當多,幾乎跟北屯新一點利黃昏市場差不多。 但這篇的目的就單純是為了這攤「
            小食幷蔥小餅」而來的,下午3點開始營業,但我們兩點半到已經不少人在排隊了。 攤位內
            只見年輕老闆一人獨挑大樑已經忙得分身乏數,從桿餅、煎餅到分切分裝、結帳然後再飛奔
            去顧煎鍋 幾乎沒有半分秒休息,問了才知道已經在這擺攤10年,然後十年如一日的這樣忙碌
            也是相當不簡單。 畢竟在旁邊看老闆煎餅是不用計時器的,一人顧兩鍋全憑感覺,所以不時
            就要翻鍋、刷油,想等餅煎好還真的要有耐心。 整大張餅可以分切、半張也能整張買,但
            別擔心你買整張不會叫你整張大餅捧著走,手會燙熟,光看到分切時那斷面蔥花爆滿就讓我
            好想直接梭哈整張餅。 如照片看到外觀就像那種「小時候大餅」,但都是現桿現煎,會灑上
            滿滿芝麻,再煎到兩面整個焦酥,起鍋冒著熱氣蒸騰!手起刀落分切開咔滋聲不絕於耳,蔥綠與
            香氣隨熱氣滿溢。 一口咬下裡面的麵糰是很有嚼勁的,100%蔥香重擊而來,微帶濕潤感的
            麵糰口感還帶有鹹香調味,吃起來其實完全不單調! 我還以為只是蔥多噱頭賣相,但一賣10年
            能排隊沒有停過,如果不是真的好吃,氣溫只有8到10度誰會專程來排隊呢? 我不確定在台中
            舊市區有幾家市場攤位賣類似蔥大餅,但真的不枉我專程前往一吃就愛上,看似簡單無奇,
            但簡單的事做到專精的職人精神排隊旁觀時就看得出來,老闆對於製餅到煎餅的每個步驟跟
            時間完全不隨便馬虎,依舊堅持自己的工作步調要讓每個人都買到剛剛好的美味,我不會說
            有到驚為天人,但確實是值得一吃的在地好味道。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1630227600
    assert parsed_news.reporter is None
    assert parsed_news.title == '爆滿蔥花熱氣蒸騰!台中超搶手「蔥小餅」 撒上芝麻餅皮厚實焦脆'
    assert parsed_news.url_pattern == '2053582'
