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
    url = r'https://www.epochtimes.com/b5/19/10/23/n11606025.htm'
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
            此刻,許多應屆高中畢業生正在緊張地申請或應考各個大學。這可能是他們畢業前,所面臨的
            最艱鉅的挑戰。入讀高等院校的競爭,一年比一年激烈了。雄心勃勃者可能竭盡全力去打拼,
            而有些人可能會被嚇倒,不敢把目標訂得太高,只是順其自然。也有些人將目標鎖定在社區
            學校,或徹底放棄高等教育。面對未卜的前途,一些學生可能會伴隨著壓力和沮喪,產生憂鬱
            症狀,甚至開始吸毒。但其實申請大學有其竅門,我們將舉辦一場講座,等您來尋獲這塊敲門磚
            。 舊金山市最具競爭力的公立學校最近透露:四分之一的學生吸食大麻。父母能做些什麼呢?
            怎樣去激勵孩子求學上進呢?許多家長對此束手無策。為此,我最近採訪了哈佛大學(Harvar
            d University)畢業生和哈佛招生辦面試官張彼得(Peter Zhang)。擁有幼稚園到高中
            心理諮詢執照的張先生,在過去數十年裡激勵無數高中學生,實現其就讀世界頂級學府的夢想。
            分享他的輔導經驗可能對畢業生及其家長們大有助益。 了解高等教育的歷史淵源 無論是東方
            的孔子,還是西方的蘇格拉底(Socrates),都十分注重把智慧和美德的重要性傳授給人。
            柏拉圖(Plato)設立了稱為「雅典學院」的第一所大學,以啟蒙哲學思維和智慧為重點。遺憾
            的是雅典學院沒有延續至今。而在公元11世紀,波隆那大學(University of Bologna)
            卻成為了世界上依然存在的最古老的大學,當時的授課內容主要是神學經典和民法,後來增加
            了哲學和人文學科,用以培養社會菁英。 而當今的高等教育,特別是在法蘭克福學派興起之後
            ,到了二十世紀初期,教育學家約翰杜威提倡實用主義教育,把象牙塔般的人文教育逐步引導為
            實證科學教育,強調應用性強的術類,而不是傳統的抽象思辨和人文教育。然而,這也是學院
            被斷絕神學與道德的開始。今天的高等教育注重實際應用課程和體驗式學習。而不再強調歷史
            、哲學、古典文學和藝術等人文學科。 你是名牌大學正在找尋的人才嗎? 今天的常春藤聯盟
            錄取,除了保持入學考試的高分和挑戰學術課外,還有什麼呢?去年,申請哈佛的逾4萬3千多名
            考生中,其中被錄取的大多都是學習成績滿分的優秀人才,然而其中也有些被錄取的學生考試
            成績並不完美。那麼,這些大牌學校在申請人身上尋找什麼呢? 張先生認為,儘管高等教育
            已發生了很大變化,但哈佛等頂尖院校的錄取標準在近幾十年來沒有什麼特別的變化,哈佛
            仍然非常看重學生的課外活動,以及個人品德,這些是高分之外的重要錄取因素。 張先生指導
            過的學生,包括贏取Google大賽和Intel大賽冠軍,以及國際遺傳工程機器設計競賽(iGEM)
            和HOSA等,甚至進入《美國達人秀》(America’s Got Talent)的Quarter Finalists
            。 尋找適合你的名牌大學 即便你曾多次獲獎,這證明了你有潛力,可是,張先生強調,並不是
            所有名牌大學都適合每一個人。比如哥倫比亞大學(Columbia University)也許更適合於
            喜歡居住在大都市的學生,特別是對新聞專業有興趣的人,因為哥大有舉世聞名的新聞學院
            。 而喜愛藝術、平面設計或攝影的學生或許希望進入布朗大學,因為它與著名的羅德島設計
            學院(Rhode Island School of Design)合作提供雙學位機會。對商業感興趣的學生,
            可能會關注賓州大學的沃頓商學院或康乃爾大學的Johnson School,因為這兩所大學是
            常春藤盟校裡,僅有的為本科提供商業學士學位的大學。 在11月6日,週三晚上5點至7點舉辦
            的研討會上,張先生將與大家分享他多年來升學輔導的經驗,幫助家長、應屆畢業生,以及明年
            的畢業生籌劃升學策略。 大學申請研討會主題包括: – 最熱門學府如何挑選報考者,以及
            家長/學生該怎樣應對? – 如何在申請大學方面提高自己的具競爭能力? – 寫作申請essay
            的注意事項? – 考生及家長應該如何優化自己的學習以及課外活動,包括參加各種學術或文藝
            和體育競賽的考量? 座位有限,欲報名者從速!
            '''
        ),
    )
    assert parsed_news.category == '美國,舊金山,生活嚮導,教育,學生園地'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1571760000
    assert parsed_news.reporter == '馮尚琳'
    assert parsed_news.title == '準備強大的大學申請:被常春藤盟校錄取不是夢'
    assert parsed_news.url_pattern == '19-10-23-11606025'
