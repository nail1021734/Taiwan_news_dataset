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
    url = r'https://www.epochtimes.com/b5/19/12/29/n11753517.htm'
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
            母奶對孩子非常重要,但母乳餵養多久才合適呢?給寶寶斷奶時,有的媽媽在乳頭上抹辣椒、
            抹清涼油,或者是吃辛辣食物,讓母奶變味。這些方法是否正確?那麼對孩子和媽媽都好的方法
            是什麼呢? 母乳餵養到底要多長時間呢?有小兒科的報告說,如果能維持很平穩的狀況呢,至少
            餵母乳6個月。餵母乳6個月以上的話,這個孩子的腸胃道的健康狀況,至少可以維持到上小學
            之前。也有研究發現,即使到1歲的時候,母乳的營養也夠用了。 孩子上幼兒園之後,與很多
            孩子在一起了,最容易發生交叉感染。吃母乳的孩子,可以減少這種風險。吃母乳可以更好地
            保護孩子的健康,孩子不容易腸胃發炎,不容易請假。 斷奶的時候,母親要從改變飲食開始
            做起。中醫說麥角之類的食物有助回奶,但不是對什麼人都起作用,最好問問自己的母親,吃
            什麼東西可以讓乳汁變少。 當母親的乳汁變少後,寶寶會吃不飽,他就會增加副食品,就會去
            吃其它食物。用這種漸進的方式,慢慢就把奶斷了。如果,乳汁一直很多,減不下來,除了飲食
            調整之外,還可以把奶抽出來。 我認為,不要用辣椒、芥末、清涼油之類刺激的東西斷奶,對
            孩子來說這是很痛苦的經歷。本來,吃母乳這段時間是很美好的經歷。現在,用刺激物強迫
            斷掉,對孩子的邏輯來說是破壞性的,孩子也會產生不可預期的恐懼感,情緒不容易穩定。 母
            親哺乳辛苦 得到的更多 我必須強調,餵母乳不僅對孩子好,而且也對母親的健康很有幫助。
            有婦產科的數據顯示,餵母乳的媽媽得乳腺癌的機率只有平均值的1/5左右。 現在的科學越來
            越多地在回歸自然,就是「Organic」。在這種回歸自然的哲學思想指導之下做的科學研究
            發現,如果母親的身體沒有特殊的障礙,或者特殊的疾病,也沒有特別勞累的話,能有奶就繼續
            給孩子餵母乳。 有科學研究發現,如果母親是心甘情願地餵孩子母乳,哪怕一開始有痛,甚至
            些許發炎的問題,但母親並不放棄,認為這是自己的天職,她的子宮收縮會比不哺餵母奶的媽媽
            好很多,也快很多。 老天爺是很公平和慈愛的,媽媽哺乳孩子,付出了一些辛苦,但得到會更多
            。至少會有兩個好處,一個是身材會苗條一些,另外一個就是子宮收縮得好和快,以後罹患子宮
            方面的婦科疾病的機率會減少很多。 人類科學在發展中,經常會有反省,發現以前認為一定對
            的方法,其實並不一定對。在育兒中,一些追求速效的方法產生的副作用,讓父母將來會有大
            麻煩。剖腹生產就容易造成對母親的傷害。 我舉個例子,我的一位醫生朋友第二天要去做
            手術,我就去看望她。去她家時,發現她家的廚房好像基本不開伙的樣子,但是擺了一排的藥。
            我是醫生家庭出身,知道很多醫生是討厭吃藥的。所以很清楚地知道,她一定已經沒有法子了,
            才要吃這麼多的藥。 這位朋友因為子宮積血,排不出去,長達十多年,造成她非常不舒服。她
            是有兩個孩子的媽媽,生完第二個小孩後,肚子沒有收縮,反而腫脹得像懷孕三四個月的樣子
            。 一開始查不出原因,吃了很多藥,像退燒藥、消炎藥、肌肉鬆弛劑,最後還吃安眠藥,什麼藥
            都吃了。但問題不僅沒有解決,反而症狀越來越多,身體免疫力越來越差。而且對藥物的抗藥
            性越來越高,就不斷地換藥,所以廚房裡才有那麼多的藥。 原來,她最後一次生孩子,沒有自然
            生產,是剖腹生產的。剖腹產後,在縫合的時候,沒有縫好,導致她的經血每次都排不乾淨。
            經血不斷積存在那裡,導致脹痛十多年。這樣的慘痛經歷,值得嗎? 生辰八字不是萬能的 還要
            看孩子是什麼料 現在有些華人為了求孩子的八字命運好,要在某月某日某時剖腹生產。我認為
            ,這樣對母親不會有好處。而且,孩子的未來如何,也不是光靠生辰八字就能解決的,還要看他
            是塊適合什麼的料。 我的父親是個非常有智慧的人。我在小的時候,告訴父親自己長大後要
            做一件大事情時,他就告訴我,你沒有那個本錢,你父親也沒有那個條件。 那個本錢是什麼呢
            ?他說,你要做那麼大的事情,你要去做官才行,但你的個性不合適。不是你的能力不夠,是你
            的個性不合適。你太直了,不適合官場。 那這件大事是什麼呢?我小時候,家的後面是一大片
            的農地。我經常可以看到菜農天不亮就起來巡視農地,非常辛苦。但是辛苦了一整年,到年底
            的時候,卻有很多菜都收獲不了,讓周圍的鄰居隨便去摘菜吃。原來,因為請工人收獲,還有運
            出去所要的錢,還不夠菜錢,只能荒廢掉。 我當時看到這樣的情形,就很同情農民,就想自己
            長大後,要去做這種幫助農民產銷的事情。我父親說,你從小就不是眼界很小的孩子,想的都是
            大事,以後一定想做大事。但我們不是官宦世家,也沒有那種人脈,你的性格也不適合做官,你
            要好自為之。 我5歲讀幼兒園,6歲上小學,是提早入學的。因為我媽媽太忙,沒有時間管我。
            開始只是寄學,不算正式入學。但由於我的成績進入班級前三名,就正式入學了。 我的父親
            發現,當時我雖然還很小,但有一種特質,就是很多小朋友都會來找我解決問題。如小朋友受傷
            了,皮膚破了流血了,他們不找護士阿姨,反而會去找我解決。還有,我在讀書時,生物學基本
            不用看,課本像新的一樣,但考試成績卻非常好。父親就鼓勵我去學醫,走幫助別人這條路
            。 作為醫生,以及後來做教育工作,這都是一件重要有意義的事情,我做得挺開心,爸爸也非常
            支持。
            '''
        ),
    )
    assert parsed_news.category == '美國,舊金山,生活嚮導,教育,家庭教育'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577548800
    assert parsed_news.reporter == '曹景哲'
    assert parsed_news.title == '給寶寶斷奶 自然勝過強制'
    assert parsed_news.url_pattern == '19-12-29-11753517'
