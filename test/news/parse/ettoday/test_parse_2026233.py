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
    url = r'https://star.ettoday.net/news/2026233'
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
            COVID-19疫情延燒超過一年,全球股市在美股的示範下,頻創新高,跟以往的牛市不同的
            地方是,這次散戶自己當起了帶頭大哥,螞蟻搬象的故事到處頻傳,美股有GameStop
            軋空傳奇,台股有航海王的神奇之旅,透過互聯網的一傳十、十傳百,吸引有志若為的年輕人
            投身股海,不管初衷是理財還是投機,股海淘金這條路從來就不是外人所想像的那麼輕鬆
            暴富。 投機無本當沖 不是致富之路 疫情打亂了供應鏈秩序,黑天鵝頻傳意外造就了
            百年難得一見的高海運運費,基於籌碼的對作特性,貨櫃三雄掀起一波十倍上漲行情,在
            社群媒體的渲染下,無本當沖翻身術成為年輕人崇尚的致富之路。 根據證交所公布的資料,
            台股新增開戶人口有四成是三十歲以下,其中有十一萬戶每天當沖,以每天盤後公布資料至少
            二千億的當沖量,這群追漲殺跌的股市新勢力已不容小看。不過,各路英雄好漢齊聚一堂,但
            武林盟主只有一個,尤其是股市,二八法則是真理、是鐵律,人人都想靠股市翻身,到頭來,
            殊不知反倒成為韭菜被收割。一名月入三萬多元的網友在Dcard上傳了自己的銀行帳戶─
            負債百萬,原因是借錢玩當沖,連紓困貸款都賠進去了,月收入都不夠還銀行貸款,求助網友
            建議。 理財方法錯誤 可能淪為理債 二十多歲的年輕人剛出社會,不懂得珍惜無債一身輕的
            優勢,還沒累積到資本就嘗試高風險的投資,往往還沒賺到第一桶金,就自己挖了個坑把自己
            埋了進去,本想藉著投資理財,哪知道,越理財越窮,所以其實學會理債比理財更重要
            。 多年前,演藝圈名人曹啟泰,在二十多歲靠著張小燕的連環泡節目一炮而紅,在意氣風發
            的三十歲跨足婚顧事業,過度擴張,加上陌生行業,最終落個負債一.六億元下場。曹啟泰花了
            五年的時間每天軋三點半的票,最終還清債務,人生得以重來,但又有多少人可以東山再起?
            從曹啟泰的例子可以發現,擴張信用過度,往往就是一隻腳踏入負債深淵的開始。 五月母親節
            過後,原本在這場疫情裡掛免戰牌的台灣,突然間本土確診直線上升,安穩太平的日子過到
            麻痹的台灣人,一時間無法接受本土確診大幅飆升的事實,導致加權指數跌掉2550點,現在
            人人稱頌的航海王─貨櫃三雄,硬生生的從百元關卡拉回到六字頭,跌幅高達四成,連續四天
            都有券商申報違約交割,凸顯股民賭一把的投機致富心態,實不可取。 過了一個多月再
            回頭看,當時貨櫃三雄的拉回竟然是再賺一倍的發財機會,可以說,貪心、賺快錢、過度自信
            都是人生背債導火線,如果那些違約交割的股民當初不要急躁貪心,過度擴張信用,持股
            留到現在,相信每個都是走路有風的航海王。 理債正確作法 賣資產還負債 多數進股市
            的人,都是懷抱著數錢數到手抽筋的美夢,應該沒想過,如果有一天自己負債了,該怎麼辦?
            推測大多人數會像上述月收入三萬多的年輕人一樣,成為銀行的信貸奴隸,且別說每個月
            還不還得起分期付款,就算還得起,隨著時間所累積的複利,終將吃掉自己的勞力付出所得,
            虧了錢,還賠上青春。尤其最不可取的是,已經負債了,又不認輸,繼續想法子借錢來賭一把,
            期盼能連本帶利的賺回來,如此借短債、還長債,繼續從事高風險投資,利滾利的下場最後
            只剩宣告破產一路。 理債正確的作法,就是「賣資產、還負債」,有融資的,還融資;
            有房貸的,賣房子還負債。總之把握一個原則,就是無債一身輕,若有穩定的現金流前提下,
            退而求其次,可保留房子繳房貸(因為房子會增值)。其實用股市的白話來說,就是執行止損,
            且不可繼續借錢來加碼攤平,任何妄想成為電影中的賭神、賭聖的股民,最後都會被市場淘汰
            。 每月一成報酬 八個月就翻倍 愛因斯坦說過,複利是比原子彈威力更大的武器,每位股民
            應該應用七二法則,在進入股市建立部位之前,設定心中預期的報酬率,如此才能避免過度
            樂觀追高,與過度悲觀的殺低。所謂的七二,就是你把「72」當作分子,報酬率當作分母,
            得到的結果就是「翻倍需要的年數」。例如每個月追求10%的報酬率,那麼經過七.二個月
            之後,就能達到本金翻倍的報酬率。
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1625822760
    assert parsed_news.reporter == '洪寶山'
    assert parsed_news.title == '你越理財越窮嗎?'
    assert parsed_news.url_pattern == '2026233'
