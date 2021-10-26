import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/04/10/a516866.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            在繁華的莫斯科市中心,有一個專門揭露共產黨紅色恐怖,介紹史達林政治迫害歷史的國立
            古拉格博物館。博物館領導人說,博物館成立7年以來未遇到任何麻煩,他們的任務就是向民眾
            介紹過去那段黑暗的歷史。 博物館提供英俄文講解 蘇聯解體20年來,雖然共產黨勢力在
            俄羅斯仍然非常強大,但批判共產黨統治歷史的工作從未間斷。位於莫斯科的國立古拉格
            博物館在這個領域扮演著重要角色。 國立古拉格博物館位於莫斯科市中心高檔商店林立的
            彼得羅夫卡大街上,距離著名的莫斯科大劇院不遠。博物館所在建築物的外表由於年久失修
            顯得破舊,這同周圍奢侈的氣氛相比顯得格格不入。但儘管如此,這個專門揭露共產黨紅色恐怖,
            介紹史達林大清洗和政治迫害,講述古拉格勞改營制度的博物館每天仍然接待大批遊客參觀。
            博物館可同時提供俄文和英文導遊講解服務。 遊客各種各樣 博物館副館長羅曼諾夫說,參觀
            博物館的人各種各樣。他們時常接待幾十人一組的中小學生和大學生參觀。遊客中也有不少
            外國人,有人專程來俄羅斯旅遊就是為了去古拉格博物館。 民眾和歷史間的橋樑 羅曼諾夫說,
            讓民眾瞭解過去的那段黑暗歷史,博物館恰好可在民眾和歷史之間起到橋樑作用。 羅曼諾夫說:
            “俄國社會目前對那一段歷史的瞭解處在一種渺茫狀態。所以國立古拉格博物館必須以較高的
            學術和藝術水準向社會全面介紹過去的那段歷史。博物館不僅應該從事那段歷史的研究,還
            應成為這個領域的學術研究中心。當然我們在這方面僅處在開始階段。” 羅曼諾夫說,博物館
            的展廳目前顯得簡陋寒酸,他們計畫對博物館裝修,提高博物館的藝術和專業水準。 古拉格
            博物館介紹的歷史從1918年布爾什維克開始紅色恐怖,建立第一個勞改營講起,一直到1956年
            結束。 展品中包括了歷史檔、信件、前勞改營犯的回憶錄、以及個人用品和反映勞改生活的
            油畫和照片等等。展廳中還陳列了勞改營囚犯居住的房間和審訊室的複製品。有的展品還介紹
            了一些囚犯的個人命運。 展覽中很大一部分專門介紹了古拉格勞改營制度在當時蘇聯的社會、
            經濟和政治生活中扮演的角色。還特別講述了如何利用勞改營囚犯開鑿著名的莫斯科運河,
            如何在農村開展集體化運動和消滅處決富農,甚至對前蘇共主要成員布哈林等人的審判也有
            介紹。 資金來源和工作人員 俄羅斯的許多博物館目前都面臨資金不足,工作人員年齡偏高
            問題。但國立古拉格博物館副館長羅曼諾夫說,他手下的工作人員都是年輕人,這使博物館
            發展得很快。除了獲得莫斯科市政府財政撥款外,博物館還時常獲得各種捐贈。比如展廳的
            照明系統就是由一名美國遊客贈送的。 羅曼諾夫說,一些官員,或是議員有時也出席博物館
            的活動。他說,雖然在俄羅斯不少人仍對史達林有好感,但這並未對博物館的工作帶來任何
            影響。羅曼諾夫說:“我們沒有遇到任何困難和阻撓。儘管俄國社會有人認為,正是史達林
            當年領導國家戰勝法西斯,贏得二次大戰勝利。但也有人持相反的觀點。” 行人指責博物館
            造假 羅曼諾夫說,他有一次遇到一個過往的行人看到古拉格博物館的招牌時,這個人勸阻
            遊客們不要進入博物館中參觀,這位行人指責博物館在撒謊和造假。但當他邀請這個人進去
            親眼看一看那段歷史時,這名行人乾脆拒絕。 安東諾夫-奧夫謝延科和博物館 國立古拉格
            博物館在2004年成立。莫斯科市長當年下令在市中心拿出兩層樓的地方提供給博物館使用。
            博物館的創建人和館長是91歲的歷史學家和作家安東諾夫-奧夫謝延科。他的父親曾是
            布爾什維克的一名領導人,因為是史達林的政敵和托洛茨基的支持者,在1938年被處決,
            他母親在勞改營中自殺。他本人三次被捕在勞改營中度過了13年的時間。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302364800
    assert parsed_news.reporter is None
    assert parsed_news.title == '莫斯科古拉格博物館揭共黨紅色恐怖'
    assert parsed_news.url_pattern == '2011-04-10-516866'
