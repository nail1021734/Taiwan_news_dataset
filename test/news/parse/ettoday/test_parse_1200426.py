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
    url = r'https://star.ettoday.net/news/1200426'
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
            各位應該都想知道,究竟什麼樣的復習在進行學習時是有效率的呢?如果
            學習內容有特定範圍的話,有一種進行方式幾乎可以說是「鐵則」,那就是以速度為優先,把
            理解度擺在其次,盡快學完所有範圍,並一再重複的方法。 如果你現在的學習進行方式是像
            「龜兔賽跑」中的烏龜式,也就是非得要一步一腳印前進才行的話,我建議你立刻改變成以
            速度為優先的兔子式學習法。或許你會擔心,如果用那種方式進行,好像學得不夠扎實,不曉
            得能不能夠確實記住學習內容,但如果從最後的記憶定著度來判斷,這才是最有效率的進行
            方式。 所謂學習上的記憶定著度,請把它想成像塗油漆一樣的概念。在牆壁上塗油漆時,不
            可能一次就塗完,因為只塗一次的話,會有很多塗不均勻的地方。因此在完成之前,必須塗好
            幾次以增加厚度,學習的記憶也可以說是同樣的道理。 舉一個淺顯易懂的例子,假設現在有
            兩個學生,打算背新的英文單字,其中一人為A,另一人為B。兩人要背的是同樣的一百個單字
            ,A同學在一天之內花了4小時背誦那100個單字,B同學則在4天之內,每天用1小時的學習時間
            背誦,兩人用於背誦的總時數都是4小時。 假如背完以後馬上進行記憶測驗,那麼兩人在當
            下的記憶量並不會有差別。然而經過一段時間以後再進行測驗,結果卻會變成,分成4天學習
            的B同學能夠想起的單字量比較多。這種大腦關於記憶的特性,顯示出分成多次重複塗上淺
            薄的記憶,比好好花時間一次背誦起來,更容易形成不易遺忘的強烈記憶,也就是記憶的定著
            度較高。 不過在進行之前,一定要先考慮一項條件,那項必須考慮的條件就是「學習範圍的
            廣度」,亦即「學習的總量」。如果只是學校的定期考試,那還沒什麼問題,但如果是入學考
            試或證照考試的話,必須學習的範圍相當龐大,學習內容的分量也非同小可。 我們來想想看
            ,面對如此龐大的範圍,如果用前面的方法進行學習,會發生什麼事呢? 假設我們重視速度,
            把記憶的定著擺在其次,打算一口氣學習所有範圍。因為記憶會經由復習變厚,所以在只經
            過一次學習的前提下,就算記憶稍微淺薄一點,照理來說應該也無妨,但在範圍非常龐大的情
            況下,只經過一次學習的記憶實在是太過於淺薄了。正如前一節的記憶遺忘曲線所示,記憶
            會在短時間內急速流失。 雖然說只要把淺薄的記憶重複塗上好幾層,就能夠變成強烈的記
            憶,但由於只經過一次學習的記憶實在太過淺薄,所以如果想增加厚度,必須重複非常多遍才
            行。在這種學習範圍很廣的情況下,這種學習的進行方式,反而有可能變得缺乏效率。 那麼
            有沒有什麼學習法是在學習範圍很廣的情況下,依然能夠讓這個重視速度的觀點派上用場的
            呢?答案就在我所參加的記憶競賽中。 # 即使學習時間相同,記憶量也會出現差異 背誦100
            個英文單字 1) 一口氣背完全部的A同學 在一天之中,花4小時背100個單字 2) 把時間分段
            反覆背誦的B同學 分成4天,每天一小時背100個單字 背完之後馬上進行測驗,兩人的記憶量
            並沒有差別,但經過一段時間以後再進行測驗,卻會出現分成4天學習的B同學能夠想起的單
            字量比較多的結果。
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530084060
    assert parsed_news.reporter is None
    assert parsed_news.title == '金魚腦適用!兔子式學習法k書復習 記憶定著度較高'
    assert parsed_news.url_pattern == '1200426'
