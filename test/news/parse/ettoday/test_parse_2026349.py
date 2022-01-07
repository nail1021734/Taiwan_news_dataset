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
    url = r'https://star.ettoday.net/news/2026349'
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
            中央流行疫情指揮中心昨(8日)宣布,全國三級警戒再延長2週至7月26日,但13日起適度
            鬆綁博物館、電影院、健身房等場所。對此,福部草屯療養院醫師沈政男表示,
            這是一個超微解封、象徵性解封、2.99級解封,而背後原因就是「台灣有了三級警戒
            倚賴症。」 面對三級警戒以來,外界許多的猜測與言論,沈政男晚間在臉書發文表示,
            「5月中說新增會破千!5月底說降到三位數以下是奇蹟!6月初說從重症率推估染疫黑數少
            說上萬!6月中說沒疫苗不可能清零!6月下旬屏東delta群聚說R值高達8!6月底說台北批發
            市場群聚麻煩了!還有更多更多看起來危言聳聽,其實就是亂扯的人,現在又在說什麼?解封,
            會再燒起來喔!疫苗沒打到六成,不能解封喔!再過一陣子,會有下一波喔!全都是,無稽之談
            。」 沈政男表示,評估解封後會怎樣,應看去年台灣R0值,然後乘以1.5倍,就會是解封後的
            R值,因為,去年台灣從頭到尾都沒有三級警戒,而alpha病毒的傳播力是去年病毒的1.5倍,
            「你去看英國流行病學家是不是這樣評估解封?但今天台灣有人提到嗎?就只是憑直覺與個人
            經驗在那邊胡亂喊價。」 沈政男認為,指揮中心今天所宣布的7月12日微解封,最有意義是
            開放內用,但因為規定相當繁瑣嚴苛,到底有多少餐飲業者將會照辦,還是乾脆維持只能外帶
            ,猶待觀察,其他戶外景點與戶內場所的微解封,其實本來就無關防疫大局。 沈政男說,
            整體而言,這是一個超微解封、象徵性解封、2.99級解封,而背後原因就是「台灣有了三級
            警戒倚賴症。」 沈政男舉例,這在其他國家也都出現過,也就是封城太久,習慣躲在家裡的
            安心感覺,於是即使解封,也寧願不出門了。但,這在國外是個案,在台灣卻是普遍現象,
            「君不見,好多民眾一看到最近風景區有人聚集,就開始著急大罵?」 沈政男預期,即使官方
            說要解封,很多民間業者與消費者,仍然會自我三級警戒,就因擔心病毒會趁機從暗地裡竄出,
            展開絕地大反攻,因此7月12日如果不敢降到二級,到了7月26日仍得面對同樣的考驗,就只是
            把頭痛時間延後兩個禮拜罷了,「除非7月26日能夠清零,而有沒有機會?當然有,就看你有
            沒有決心。只是,清零還得累積十四日,才能確定沒有死灰復燃,而這就不是7月26日可能
            達到了。」 沈政男表示,早就說唯一安心的解封之道就是清零,而清零絕對可能,並且無需
            疫苗就能達成,「現在,大家相不相信了?」只是,什麼時候能夠清零,牽涉疫調與隔離技術,
            而且需要一點時間,很難由現在的R值推估,現在的R值連續幾周都是0.6左右了,才會降到
            現在剩下十幾二十例,問題是兩周後雖然照算會剩下個位數,但清零什麼時候可以達成,
            就是另一回事了。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1625797860
    assert parsed_news.reporter == '邱晟軒'
    assert parsed_news.title == '713「2.99級解封」醫曝原因 指7/26還有考驗'
    assert parsed_news.url_pattern == '2026349'
