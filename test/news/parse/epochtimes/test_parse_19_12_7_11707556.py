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
    url = r'https://www.epochtimes.com/b5/19/12/7/n11707556.htm'
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
            自由從紀律而來,雜亂無章的行為,容易釀成不幸。德國哲學家亞斯培卻曾說:「沒有權威,便
            沒有自由。」孩子的日常規矩養成,是教育最重要的核心。除了愛,教育孩子更需要勇氣,即使
            管教會帶來不快,仍然必須正視衝突,不輕易讓步。 有次去小熊的班上代課,讓我留下深刻的
            印象。上課時,班長在黑板上登記不乖的同學的名字,台下的搗蛋鬼沒有一個覺得害怕。 我問
            班長:「不乖的人,老師怎麼處罰?」班長無力地說:「下課不准出去玩。」一個皮蛋偷聽到了,
            開心地高喊:「喔耶!我不出去玩,可以在教室玩塞爾號對戰卡,更棒!」下課後他果然跟死黨
            圍在教室後方玩卡,超級開心。 放學時,班長在走廊整隊,扯開喉嚨大叫:「排好!排好!」
            沒人理她,各玩各的,聲音比她還大。因為他們知道,不聽班長的話也不會怎樣!這一班孩子的
            確很活潑,但活潑未必代表沒規矩。班級缺乏紀律,最大的可能在於沒有賞罰分明的規定,或是
            孩子們不信服、遵從或在意這規定。 《韓非子.內儲說上》有云:「愛多者則法不立,威寡者
            則下侵上。」管教應該有賞有罰,如果獎懲的手段無效,管教的效果自然不彰。 《有紀律的
            孩子更優秀:德國王宮中學校長的教育心得》(先覺出版)一書提到:「教育的勇氣,指的尤其
            是堅持「紀律」的勇氣。紀律儼然是教育最不可愛的一環,卻是所有教育的基礎。 紀律所
            體現的,幾乎盡是大家所厭惡的事情:強迫、服從、制止、壓抑欲望和意志。紀律是將效率原則
            置於享樂原則之上:為達目標,應當接受各種節制,甚至必須如此。 紀律總是始於他人的決定,
            而且應該終於自我的決定,從外部的紀律轉為自律。以教育而言,紀律,必須出於對孩子和
            青少年的愛。」 日常規矩的養成,是教育的核心 教孩子需要勇氣,即使管教會帶來不快,仍然
            必須正視衝突,不輕易讓步、退縮。自由從紀律而來,雜亂無章的行為容易釀成不幸。德國
            哲學家亞斯培卻曾說:「沒有權威,便沒有自由。」孩子的日常規矩養成,是教育最重要的核心
            。 建立班級紀律應該有許多方法,我在美國看過小熊的幼稚園老師是這樣做的: 老師的賞罰
            紀錄工具,是一塊分成藍、黃、紅三色區塊的板子。孩子一大早到學校,老師會在聯絡簿貼上
            一張Mr. H專用的笑臉貼紙,如果一星期五天都貼滿,週五就可以去老師的神祕藏寶箱(Trea
            sure chest)拿一個小禮物,通常是可愛小玩具,如小望遠鏡、小寶石等。 每天一早,寫有
            全班同學名字的小木頭夾子,會先夾在板子的藍色區塊。如果上課不乖,老師會給予警告,也就
            是將寫有名字的小夾子從藍色區移到黃色警戒區。如果再犯,老師就會把名字夾移到紅色反省
            區,屆時聯絡簿上的貼紙就會被拿掉! 教育,不但要有獎賞與懲罰,更要給予警告的機會,黃色
            的區域就是「不教而誅謂之賊」這句成語的應用吧?不過話說回來,將所有的教育責任推給
            導師也不盡公平。 從許多孩子叛逆、不聽管教的舉動,能夠看出他的家庭環境。曾有一個
            美國牧師對我說過:「我帶兒童主日學多年,只要給我一小段時間觀察,就可以知道這個孩子
            來自怎樣的家庭。哪些小孩的家庭是幸福的、健全的、有管教的還是失能的,從他們的一舉
            一動都看得一清二楚!」 我們都不喜歡自己的孩子被人認為沒家教,但是「家教」的確在忙碌
            的工商社會中式微。老師固然應該管教我們的孩子,然而我們是否有在家中建立「遵守紀律」
            的行為與價值觀? 光是「愛」,不足以引導孩子走上正路。希望孩子得到教育,就要有「處罰」
            的準備。體罰固然不足取,但是父母應該善用「有效懲罰」,例如暫停(Time out)、取消
            零用錢或減少看電視時間等,讓孩子在家養成遵守紀律的習慣,才不會成為「沒家教」的孩子
            。 教導有主見的下一代的確很不容易,學校與家庭必須共同負起管教的責任,讓孩子感受到大
            量的愛而不被溺愛。
            '''
        ),
    )
    assert parsed_news.category == '文化網,教育園地,家庭教育,教養心得'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1575648000
    assert parsed_news.reporter is None
    assert parsed_news.title == '教育孩子 只有「愛」還不夠'
    assert parsed_news.url_pattern == '19-12-7-11707556'
