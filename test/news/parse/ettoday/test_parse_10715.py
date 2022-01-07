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
    url = r'https://star.ettoday.net/news/10715'
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
            四分之一來自外公德國血統的俊帥外表,百分之百深情的創作型偶像手李聖傑,在他歌唱生涯
            的第十二個年頭,開了公司自籌演唱會,但他卻說:「我發現原來唱歌只佔了歌唱事業的五%!
            其他的九五%就是必須懂得唱片這門生意,以及確立自己所扮演的角色及態度。」 「要懂得
            看清楚自己,是最難的部分,但是確立自己之後,可以從裡到外,把自己的個性和態度,藉由
            歌唱完整表達出來,這樣子做自己,是一件最棒的事。」 變得很『一個人』 才會是最特別的
            那一個 十二年的奮鬥歷程,從一個網球國手轉行的新人,到如今能完全主導自己的演唱會
            ,李聖傑說:「就像時鐘由一回到了十二,圓滿走回原點,當中有著自己的堅持、忍耐、毅力
            和存亡的取捨,這一切並不容易。」 尤其對於連細節都務求精準完美的李聖傑而言,辛苦的
            不只是他,還有身邊的夥伴們。他可以為了幾十秒的電台廣告,重錄再重錄,只想讓襯樂調整
            到不干擾主題,又能恰如其分襯托出主題,而其中「恰如其分」的奧妙,也只能依憑他對音樂
            美學的靈敏度加以分辨。 執行上分量繁重的要求,當然會佔據創作的時間和能量,但若不去
            掌控執行品質,又無法淋漓盡致展現自我,這就是創作者的兩難。矛盾還不僅止於此,兩難的
            抉擇不時浮現。「歌手有時候必須『一個人』,當你把自己變得很『一個人』,才會是最特別
            的那一個,當別人都不了解你,也才會有自己獨特的思考,才會出現一種十分自我的氛圍,別人
            會覺得不知道你在想什麼?像我平常走路時,也都不自覺一個人走在最前面,就是不想和別人
            走在一起。只不過一個人走久了,總是希望有朋友可以了解我,而且當我獨自站在台上,卻有
            一整個團隊在幕後,又怎能不讓他們了解我參與我?所以情緒就在來回拉鋸中掙扎,必須要知道
            自己的極限在哪裡,也一定要將自己逼到那個谷底,創作的火花才會出現。」 創作必須忍受
            寂寞,然而創作者的孤寂感,如何才不至於孤芳自賞?李聖傑說:「我所唱出的每一個字句
            ,都跳躍出許多畫面的訊號,當我站在台上,就將這些畫面的訊號輻射出去,在台下的觀眾
            接受到我的訊號,看到了我所表達的情境,或是同理心地投射到自己的回憶畫面被打動,就會
            覺得我唱出了他們的心事。其實歌手唱的是大方向,而每個聽眾都在大方向裡尋找符合自己
            的故事。」 歌手不能有所侷限 任何一秒都期待被觸動 如此多的情感畫面,想必來自於豐富
            的愛情經驗吧?李聖傑承認:「戀愛很重要,我的情歌記錄的就是戀愛的過程;每次戀愛的結果
            都只是答案,只有過程能令人品味不已。當你遇見一個人,有了感覺就開始了曖昧,曖昧以
            至於相戀、分手,包括如何離開,這些都是值得記錄的過程。」 「戀愛一定要有很多次的
            失敗,才能找到自己要什麼?但是很多人過一輩子也不知道自己要什麼。遇到對的人,和她
            相戀,那是幾億分之幾的機率,有的戀愛很準確,有的就不是,必須在一次次失敗中找到自己
            所需。」 他所需要的女人是什麼樣的呢?諸多緋聞,令媒體對他的情愛世界窮追不捨
            。這又是李聖傑的另一個兩難!他說:「歌手的世界不能有所侷限,我們要能飛到每個角落
            ,任何一秒都期待著被觸動,要不停去感受,把這些情感一直不停放近來,再發射出去,才能
            累積歌手對聽眾放電的energy。然而過去我身邊的人很難接受這些,以後的人我也不期望她
            能完全理解我的世界,因為找到一個能理解我的人,遠比找到一個愛我的人還困難。人生本就
            必須做出取捨及犧牲,但是換個角度來看,如果這樣的情況會令我很不快樂,我早就放棄了
            ,可見這是我寧願做出的選擇。我在乎的是心靈的享受,而不是跟誰去渡個假玩樂一番,例如
            在新疆大草原有人牽著一頭羊來聽我唱歌,那一個moment的感動就會深深留在我的心中。」
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1323049380
    assert parsed_news.reporter is None
    assert parsed_news.title == '李聖傑:找到理解我的,比找到愛我的還困難'
    assert parsed_news.url_pattern == '10715'
