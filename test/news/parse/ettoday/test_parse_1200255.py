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
    url = r'https://star.ettoday.net/news/1200255'
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
            “Bon Appetit!”,是梅莉史翠普在電影《美味關係》內,扮演傳奇烹飪家Julia Child的經典
            台詞,就這一句高亢又唯妙唯俏的令我印象深刻。這部由女人、理想與愛情串起的烹飪電影
            ,劇情簡單、感動、平易近人且毫無壓力,成了我近半年在電腦前工作時的最佳背景音樂
            (Replay大概近十次都聽不膩)。 雖然艾美.亞當斯的表現也為這聽似沒什麼高潮的劇本加分不
            少,但確實還是因為梅姨,在劇中說服力十足又真性情的表現,才讓我徹底愛上這部美味小品
            。 仔細回想,有多少部電影、角色都是如此,若不是由她來詮釋,誰還能賦予平凡的劇本更
            多生命力?《天使在美國》、《媽媽咪呀!》、《走音天后》、《時時刻刻》、《鐵娘子:堅
            固柔情》裡強悍的柴契爾夫人、扮演《穿著Prada的惡魔》的時尚女魔頭、《八月心風暴》
            裡那位酗酒的老母親......。 大家都知道,被封為「世界上最偉大的女演員」的梅姨,在這
            四十多載為好萊塢帶來多少經典作品,又透過多少位強悍的女性角色,為女權、人權、平等
            權發聲。多到她也數不清的入圍與提名次數,3座艾美獎、8座金球獎、3座小金人,以及第74
            屆金球獎終身成就獎的殊榮......皆再再證明了她在影劇圈的地位。梅姨透過好萊塢看世
            界、體悟人生,在頒獎典禮、校園發表的演說,句句都是激勵人心的佳句。 回顧去年,梅姨
            在金球獎頒獎典禮上分享了「莉亞公主」對她說的一句話:
            ”Take your broken heart; make it into art.”
            (拾起妳破碎的心,並用以成就藝術。)雖然旨為勉勵在座的創作者們,處在
            艱難的(川普)時代更要堅持,但也讓我想起她少為人提及的一段短命婚姻、一段塑造梅莉史
            翠普,卻以悲劇收場的摯戀。 兩個多月前,心血來潮的花了兩晚的時間,把《教父》三部曲
            全部重看了一遍。仔細研究了各角色的背景才發現,其中一位在劇情前段乍看下毫不起眼,
            卻又是凸顯教父性格的關鍵人物—Fredo。這位名為約翰.凱澤爾(John Cazale)的美國演員,
            不僅是啟發艾爾.帕西諾演戲方法的重要人物,更曾在梅姨的生命裡留下深刻的痕跡。 年輕
            的約翰,從波斯頓大學戲劇學系畢業後,為了邊討生活邊尋找演戲機會,曾當過計程車司機,
            也在紐約當過攝影師和送信差。直到認識了好友艾爾.帕西諾(Al Pacino),兩人一起在百老
            匯演出時被電影製作人看上,才有機會從舞台劇進入大螢幕,《教父》上映時,他已37歲。而
            與約翰相差十四歲的梅莉史翠普,當時才從戲劇系畢業,同樣在大蘋果裡尋找能讓她發光的
            舞台。 1976年,兩人因一齣紐約莎士比亞節的舞台劇《以牙還牙》(Measure for Measure)
            而相遇,他們沒多久便陷入熱戀,梅莉史翠普還搬進了約翰位於下城西區的公寓,兩人說好各
            自接下下一部電影角色後,便要互許終身。想不到一年後,約翰便被診斷出罹患肺癌,甚至已
            擴散到骨頭,但同時間,他也得到了《越戰獵鹿人》(The Deer Hunter)中的一個要角,而梅
            莉史翠普為了陪伴他,便自願加入了這部片的演出。 據報導,在約翰病情嚴重到無法隱藏時
            ,製作人還一度想換角,直到梅姨威脅辭演,以及主角勞勃.狄尼洛和導演的努力下,才保住他
            的角色。 「我從沒見過一個人能如此全心全意的為另一個人付出。看到她對約翰無窮盡的
            愛,讓我相當感動。」艾爾.帕西諾在接受紀錄片《我知道是你:走進約翰.凱澤爾》
            (I know it was you)時這麼說道。「無論梅姨身為演員有多大的成就,我總是想到她在
            約翰臨走前陪伴他的那段時間。」 雖然梅姨在約翰去世後六個月,就嫁給了當時提供她暫宿
            的雕塑家唐.伽梅爾(Don Gummer),還有人曾質疑,梅姨既然這麼愛約翰,為何這麼快就能
            再嫁?哎,但這不就是梅姨過人的智慧嗎?拾起破碎的心,想盡辦法勇敢的走下去,再呼應
            莉亞公主的那番話“make it into art”,難道她得讓自己一蹶不振,才能證明自己與約翰的
            愛夠轟烈? 約翰離世後約有30年,梅姨幾乎不願意在公開場合或接受訪問時提及這段戀情的
            細節,但她曾在接受《梅莉史翠普:演員剖析》(Meryl Streep: Anatomy of an Actor)
            的作者訪問時說道:「我沒有忘記,我也不想忘記。無論我嘗試多少方法,那傷痛還是隱藏在
            心中的深處,而且它一直影響著自此之後的一切。」人生免不了傷痛,但有痛,不代表不能活得
            精彩,我認為梅姨的故事,即是最好的見證。
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530361020
    assert parsed_news.reporter is None
    assert parsed_news.title == '「世界上最偉大的女演員」 梅莉史翠普對《教父》的他藏著無盡的愛'
    assert parsed_news.url_pattern == '1200255'
