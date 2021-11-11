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
    url = r'https://star.ettoday.net/news/1200265'
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
            大家都知道防曬這件事很重要,但是根據我們的實際觀察,真的能做到確實的人其實很少。
            防曬效果不好的原因,有人是因為對防曬效果存疑、有人是覺得想到才擦已經來不及、有人
            是流汗沒補擦防曬效果降低、也有人覺得自己的妝品已經有足夠防曬力,但總歸一句就是對
            防曬觀念的認知不夠正確。 在前兩次的防曬實驗室中,我們已經回答了前三個疑慮。最近
            陸續收到網友們的回饋,很多人都想知道自己手邊的化妝品到底有沒有防曬力,什麼
            SPF 30 的隔離霜、SPF 35 的粉底液、SPF 23 的 BB 霜等等各種宣稱自己有防曬力的
            妝品。你就會想啊,如果今天上了全妝出門,那防曬效果應該相當驚人吧!而且就算有效,但會
            比得上單純擦一層防曬嗎?我們也很好奇!所以直接進入實測吧! 有防曬係數的化妝品防曬力
            夠嗎?畫了妝用噴霧防曬補? 在紫外線攝影實測結果中,這些宣稱有防曬系數的彩妝品和真正的
            防曬產品比起來,防曬效果似乎都不太好,應該沒有辦法取代防曬乳。 帶著這樣的結果來面對大
            魔王,永遠的棘手問題,就是「化了妝後要怎麼補防曬?」會說這是棘手問題並不是沒有原因
            ,畢竟上了妝後當然想保持妝的完整度,但是不去塗抹防曬又得不到均勻度。目前在網路上
            常見的推薦方法中,其實沒有完美的解答。其中很常見的就是用帶有防曬系數的粉餅、或是
            蜜粉輕拍臉部來補,這樣就可以不致於破壞底妝,但缺點就是補起來的防曬效果不佳。另一
            種說法就是用噴霧式防曬來補。會有這種說法,是因為覺得可以噴上去不用塗抹,就不會影
            響底下的彩妝。 但從紫外線攝影中看得出,用噴霧噴完後,並沒有得到想像中的均勻度,仍
            然需要用手來推開,那這樣不就失去上面使用噴霧的意義了嗎? 在實測中,我們並沒有以噴
            霧式防曬直接噴灑臉部,因為我們並不推薦用噴霧式防曬來噴臉。主要的原因有兩個:第一,
            噴霧式防曬噴灑出的成分進入空氣以後,一部份沾上我們的皮膚,卻也有另一部分可能被口
            鼻吸入,讓呼吸道承受了不必要的風險。第二個原因是很容易噴到眼睛,噴霧式防曬的添加
            溶劑有可能刺激或傷害眼部。大家可以回想一下,平常擦防曬的時候,如果擦到眼周常會覺
            得熏熏的,就是這個原因。 在帶妝的情況下要怎麼補擦防曬? 雖然沒有一個夢寐以求的完
            美答案,我們還是可以藉由觀念和實測結果得到個大致的結論。在沒有化妝的狀態下很簡單
            ,輕輕擦拭掉臉上的油污汗水,就可以塗抹防曬乳上去;化妝的情況下就比較複雜,通常防曬
            產品的使用,會在上妝之前,如果把防曬想像成內衣、妝品是外衣,那要補到內層的防曬,不
            就等於在不想弄皺外衣的狀況下換內衣嗎? 所以不擔心麻煩的話,卸除殘妝後再補防曬是最
            直觀的做法,但也要注意卸妝次數不要過於頻繁,避免產生過度清潔,影響皮膚正常的皮脂膜
            ;如果要使用噴霧噴灑臉部,就要小心防曬噴霧入侵眼、口、鼻的風險,況且噴霧也不如想像
            中的均勻,所以我們不太建議;補具有防曬係數的蜜粉和粉餅當然也很方便,然而根據我們的
            實驗,多數宣稱有防曬效果的彩妝品,實際效果都遠不如單一防曬產品。 所以總歸一句,濃
            妝你還要出去曬太陽,幾乎是找不到完美解法的啦!要補防曬的話,素顏最方便,擦乾汗水直
            接補上就好。淡妝也可以洗臉後就重新補上。濃妝的狀況下,除非你卸妝,不然幾乎不可能
            真正補好防曬,又不影響底妝。 不管選擇以上哪一種方式,都還是可以搭配帽子、長袖衣物
            、抗UV傘等等物理性遮蔽,防護力會更完整!有關這方面的知識,可以看看這篇文章。 我們
            未來也會推出更多實測破解系列影片,大家覺得實用有趣的話也別忘了幫我們留下一個讚,
            並分享給朋友們喔!
            '''
        ),
    )
    assert parsed_news.category == '健康'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530242280
    assert parsed_news.reporter == 'MedPartner美的好朋友'
    assert parsed_news.title == '化妝怎麼補防曬? 實測「濃妝、淡妝、素顏」補法大不同!'
    assert parsed_news.url_pattern == '1200265'
