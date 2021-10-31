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
    url = r'https://star.ettoday.net/news/1200190'
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
            美食是律師生活的慰藉,但應酬不是。 律師常被請客、也常請客,嘴巴也越吃越刁。對小律師
            而言,沒見過的奢華餐廳、美酒佳餚,一開始會有些想像、會有些期待,一次一次,又是另一個
            大觀園,以為已經見識過,卻總還有超過你想像的奢華。 一開始會感謝老闆、客戶帶你見世面。
            但,幾次下來,也應該要懷疑,他們是不是看上你新鮮的肝?幾次下來,你也會發現,應酬對
            小律師而言,更痛苦。 這樣的場景應該很常見:5點交代工作,明天早上要,但7點要陪老闆、
            客戶應酬,已經疲憊不堪,下了班還要跟客戶搏感情!更痛苦的是:老闆明天可以晚點到,小律師
            不行!老闆明天不用趕書狀,小律師不行!老闆明天不用去開庭,小律師不行!更慘的場景是:明天
            已經等著被法官電的庭,前一天還要強顏歡笑,還要拼酒,就算喝的是Latour、Lafite、
            黑金龍⋯⋯,連在Facebook打卡炫耀的興致都沒有。 總是想不通,為何還是有人樂在其中?
            真的有必要應酬嗎?真的對業務有幫助嗎?看人喝酒喝到吐,
            有那麼好玩嗎?這些問題,其實不只小律師想問,大部分律師都想問。 不勝酒力?你要家庭生
            活?你個性不喜歡應酬?就是不會說場面話?很多人不敢說,深怕老闆、客戶不會諒解。其實
            不用勉強,坦誠說出困難及想法。而且別忘了,你是律師,就是要處理奇奇怪怪的事。不想應
            酬也要想個漂亮的說法。「應酬」如果是危機,律師就是要處理危機,處理自己的危機。 對
            小律師而言,有時最大的危機反而是和老闆吃飯。老闆請吃飯,總是不自在,怕被訓話,又不
            想奉承,能閃則閃,能躲就躲,但,或許老闆也想多了解你,多提點你,或許你也可以多了解老
            闆背景與個性,讓你更清楚知道自己想當什麼樣的律師,要如何當你想要當的律師。 不要什
            麼聚會都一律回絕,同事聚餐、迎新送舊⋯⋯,有關「人和」的聚會,尤其是同事間的聚會,還
            是要儘量參加。在職場上,尤其律師生活中,由於我們處理的事情,通常緊張、嚴肅、快速,
            時常忘記給個笑容,說聲謝謝,甚至說聲抱歉。同事間的聚會,能夠緩和職場中的不愉快,多
            多了解同事的背景與個性,不只有助於日後工作,也讓工作有人性一些。 而不管什麼樣的應
            酬,就算躲不掉,被逼著參加後也要節制,也要漂亮的閃酒、躲酒,看看別人如何淺嚐即止、
            進退合宜。看看別人如何談笑風生、賓主盡歡。如何灌別人酒,也是一種學習。 最近就見
            識到一招:雖然說「喝酒不開車,開車不喝酒」,但如果遇到應酬高手,他就會告訴你,
            前一句對,後一句不對:「喝酒後當然不能開車,但別以為開車來就可以不喝酒,
            『喝下去!計程車錢自己出!』」
            '''
        ),
    )
    assert parsed_news.category == '法律'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1531267200
    assert parsed_news.reporter is None
    assert parsed_news.title == '小律師專欄:拼命又要拼酒的小律師'
    assert parsed_news.url_pattern == '1200190'
