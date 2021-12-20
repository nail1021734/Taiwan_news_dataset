import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/604954?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            第20屆台北電影獎於7月14日隆重登場,由金鐘編劇徐譽庭與許智彥一同執導的
            《誰先愛上他的》備受好評,一共拿下最佳男主角、最佳女主角、最佳劇情片,以及媒體票
            選獎四項大獎,成為本屆台北電影獎最大贏家,而在本屆金馬獎也風光入圍八項大獎,算是今年
            台灣電影中表現最為傑出的一部! 劇情描述劉三蓮(謝盈萱飾)的丈夫宋正遠,在三年前離家
            出走,而在某天她接到丈夫去世的消息,發現丈夫的保險受益人從自己的兒子呈希,變為一個
            叫阿傑(邱澤飾)的陌生男子,她氣不過帶著兒子到阿傑家理論,卻沒想到連呈希也跳槽敵陣,
            逃家跑到阿傑那寄宿,劉三蓮搶回兒子與保險金的過程也就此展開... 電影以幽默,且富有
            戲劇張力的方式講述故事,不論是張牙舞爪的三蓮、故作鎮定的阿傑,或是不斷頂撞母親的
            呈希,他們的誇張行徑在別人眼裡看似鬧劇,但在過程中可逐漸了解角色之間的深層情感,
            以及無理取鬧背後,他們刻意掩飾的傷痛與在乎,其實是沉痛的悲劇。 然而,究竟是誰先愛上
            正遠的呢?第三者是阿傑還是三蓮?答案其實不是最重要的,對三蓮而言,她只在乎正遠是否愛
            過她,至於看似破壞家庭的阿傑,其實顯露出被「社會期待」壓迫的辛酸,同志之所以會破壞
            家庭,是在於他們無法組成一個自己真正想要的家庭。 故事最後,阿傑學會了釋懷,三蓮學會
            了放下,而呈希則是象徵著旁觀者的我們,在這段愛情糾葛裡,看見「愛」的模樣,故事當中
            並沒有真正的壞人,而是將指控轉向於這個社會,讓觀眾體悟「社會的期待與壓迫」才是讓
            這段愛情淪為悲劇的最大兇手。 同性戀題材一向都是敏感話題,《誰先愛上他的》用如同
            八點檔「爭奪保險金」的故事包裝,將同志議題巧妙地融入其中,且讓同性的第三者與原配直
            接衝撞,產生激烈的火花,也讓觀眾理解「好人與壞人、受害者與加害者」的定義,有時候是
            因立場與觀點不同,而有不一樣的解讀。 電影以「全知」的角度,引導觀眾理解每一個人物
            所經歷的傷痛與無奈,而在每個角色都被愛傷的遍體鱗傷後,最終才學會「學會包容與接受」
            ,這樣的結果,或許也是這部電影想帶給我們的體悟的吧!
            '''
        ),
    )
    assert parsed_news.category == '風生活,電影,影視,性別'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541550660
    assert parsed_news.reporter == '電影教我們的五件事'
    assert parsed_news.title == '當男小三遇到原配老婆,將擦出什麼火花?《誰先愛上他的》用不同的角度,探討同性婚姻議題'
    assert parsed_news.url_pattern == '604954'
