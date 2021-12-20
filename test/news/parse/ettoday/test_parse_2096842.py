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
    url = r'https://star.ettoday.net/news/2096842'
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
            「虎尾糖廠鐵橋」是我們虎尾一日遊最後的一個景點,其實我是在IG上面無意發現的,
            後來才知道它已經有百年歷史,而且已經被列為縣定古蹟了。我覺得虎尾糖廠鐵橋很適合傍晚
            的時候來走走,還可以同時欣賞日落,很悠閒慢活的一個景點。 虎尾糖廠鐵橋位於雲林虎尾,
            最近的青埔落羽松秘境也在附近,這裡應該沒有詳細的地址,我們也是用導航直接過來,附近
            雖然沒有大型停車場,但是因為觀光客不多,而且大多是從橋的另外一頭走過來比較多,所以
            反而停車處還滿多的。 導航可以設定:同心公園或虎尾糖廠,停好車再走路到虎尾鐵橋,
            距離並不遠。 其實堤防邊都有觀景台,很多人會在觀景台上面拍拍照欣賞風景。 虎尾鐵橋
            歷史 虎尾糖廠鐵橋,又被稱作虎尾鐵橋,舊名番薯莊板仔橋,虎尾鐵橋原本是一座木造的
            橋樑,在日治時期為了方便火車運輸甘蔗至虎尾糖廠,由大日本製糖株式會社出資於1907年
            興建,除了運輸甘蔗外,也曾經同時辦理客運業務。 1931年於原木造橋下游側改建新橋,由
            3孔鋼構桁梁及7孔鈑梁連結而成,長約300.6公尺,國民政府時代1960年將虎尾鐵橋延長至
            437公尺。(以上資料取自維基百科。) 因為糖廠的沒落所以現在的虎尾鐵橋已經不做
            運輸之用,留下來的鐵橋轉而做為觀光用途,這天傍晚時分很多人來這裡拍照走走。 因外
            外婆家住西螺的關係,對於小時候常回外婆家的我們來說,虎尾並不陌生,因為對南西螺人
            來說,虎尾就是他們的家鄉,有時候反而比到西螺市區還近。 現在才知道原來虎尾是「糖都」
            ,我一直以為虎尾只有黃俊雄布袋戲! 虎尾鐵橋全長437公尺,這天導航把我們帶到對岸,
            想想也ok,這邊感覺比較寧靜,可以走過去再走回來,大概1公里左右,如果沒有拍照的話,大概
            半個小時可以來回。 這樣邊走邊拍照覺得還滿愜意的,而且因為空氣好風景也好,讓人覺得
            很舒服,看小櫻桃還這麼嫩就知道這篇照片放的有點久了! 虎尾糖廠鐵橋曾經經過倒塌過,在
            2015年4月才有重建恢復,這也是台灣產業重要的文化遺產,更是給下一代最經典的自然教學
            。 默默地走著走著就走到底了!這裡可以連接著虎尾糖廠和同心公園,此外這附近也有很多
            美食景點! 和虎尾吉祥物來張合照。 在鐵橋的兩邊都還有裝置藝術! 好不容易等到人少一點
            的時候才有機會拍個人照。 我們就坐在樓梯上吹吹風拍拍照,等到夕陽西下才慢慢走回去,
            不是多麼花俏或是雄偉的景點,但是這樣輕鬆的散散步欣賞風景,我覺得很不錯! 虎尾鐵橋
            長度 437公尺的虎尾鐵橋走起來並不辛苦,有機會到虎尾旅遊的話,可以留一點時間到虎尾糖
            廠鐵橋走走!
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634972400
    assert parsed_news.reporter is None
    assert parsed_news.title == '熱門打卡古蹟!漫步雲林懷舊百年鐵橋 無邊際鐵軌上看日落太浪漫'
    assert parsed_news.url_pattern == '2096842'
