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
    url = r'https://www.epochtimes.com/b5/19/12/23/n11739453.htm'
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
            我不知道是不是命運把我推上這講壇,由種種機緣造成的這偶然,不妨稱之為命運。上帝之有
            無且不去說,面對這不可知,我總心懷敬畏...... 一個人不可能成為神,更別說替代上帝,
            由超人來主宰這個世界,只能把這世界攪得更亂,更加糟糕。尼采之後的那一個世紀,人為的
            災難在人類歷史上留下了最黑暗的紀錄。形形色色的超人,號稱人民的領袖、國家的元首、
            民族的統帥,不惜動用一切暴力手段造成的罪行,絕非是一個極端自戀的哲學家那一番瘋話
            可以比擬的。我不想濫用這文學的講壇去奢談政治和歷史,僅僅藉這個機會發出一個作家純然
            個人的聲音。 作家也同樣是一個普通人,可能還更為敏感,而過於敏感的人也往往更為脆弱
            。一個作家不以人民的代言人或正義的化身說的話,那聲音不能不微弱,然而,恰恰是這種個人
            的聲音倒更為真實。 這裡,我想要說的是,文學也只能是個人的聲音,而且,從來如此。文學一
            旦弄成國家的頌歌、民族的旗幟、政黨的喉舌,或階級與集團的代言,儘管可以動用傳播手段
            ,聲勢浩大,鋪天蓋地而來,可這樣的文學也就喪失本性,不成其為文學,而變成權力和利益的
            代用品。 這剛剛過去的一個世紀,文學恰恰面臨這種不幸,而且較之以往的任何時代,留下的
            政治與權力的烙印更深,作家經受的迫害也更甚。 文學要維護自身存在的理由而不成為政治
            的工具,不能不回到個人的聲音,也因為文學首先是出自個人的感受,有感而發。這並不是說
            文學就一定脫離政治,或是文學就一定干預政治,有關文學的所謂傾向性或作家的政治傾向,
            諸如此類的論戰也是上一個世紀折騰文學的一大病痛。與此相關的傳統與革新,弄成了保守與
            革命,把文學的問題統統變成進步與反動之爭,都是意識形態在作怪。而意識形態一旦同權力
            結合在一起,變成現實的勢力,那麼文學與個人便一起遭殃。 二十世紀的中國文學的劫難之
            所以一而再、再而三,乃至於弄得一度奄奄一息,正在於政治主宰文學,而文學革命和革命文學
            都同樣將文學與個人置於死地。以革命的名義對中國傳統文化的討伐導致公然禁書、燒書。
            作家被殺害、監禁、流放和罰以苦役的,這百年來無以計數,中國歷史上任何一個帝制朝代都
            無法與之相比,弄得中文的文學寫作無比艱難,而創作自由更難談及。 作家倘若想要贏得思想
            的自由,除了沉默便是逃亡。而訴諸言語的作家,如果長時間無言,也如同自殺。逃避自殺與
            封殺,還要發出自己個人的聲音的作家不能不逃亡。回顧文學史,從東方到西方莫不如此,從
            屈原到但丁,到喬依斯,到托馬斯曼,到索爾任尼津,到一九八九年天安門慘案後中國知識分子
            成批的流亡,這也是詩人和作家還要保持自己的聲音而不可避免的命運。 在毛澤東實施全面
            專政的那些年代裡,卻連逃亡也不可能。曾經庇護過封建時代文人的山林寺廟悉盡掃蕩,私下
            偷偷寫作得冒生命危險。一個人如果還想保持獨立思考,只能自言自語,而且得十分隱祕。
            我應該說,正是在文學做不得的時候我才充分認識到其所以必要,是文學讓人還保持人的意識
            。 自言自語可以說是文學的起點,藉語言而交流則在其次。人把感受與思考注入到語言中,
            通過書寫而訴諸文字,成為文學。當其時,沒有任何功利的考慮,甚至想不到有朝一日能得以
            發表,卻還要寫,也因為從這書寫中就已經得到快感,獲得補償,有所慰藉。我的長篇小說
            《靈山》正是在我的那些已嚴守自我審查的作品卻還遭到查禁之時著手的,純然為了排遣內心
            的寂寞,為自己而寫,並不指望有可能發表。 回顧我的寫作經歷,可以說,文學就其根本乃是人
            對自身價值的確認,書寫其時便已得到肯定。文學首先誕生於作者自我滿足的需要,有無社會
            效應則是作品完成之後的事,再說,這效應如何也不取決於作者的意願。 文學史上不少傳世
            不朽的大作,作家生前都未曾得以發表,如果不在寫作之時從中就已得到對自己的確認,又如何
            寫得下去?中國文學史上最偉大的小說《西遊記》、《水滸傳》、《金瓶梅》和《紅樓夢》的
            作者,這四大才子的生平如今同莎士比亞一樣尚難查考,只留下了施耐庵的一篇自述,要不是
            如他所說,聊以自慰,又如何能將畢生的精力投入生前無償的那宏篇巨製?現代小說的發端者
            卡夫卡和二十世紀最深沉的詩人費爾南多‧畢索瓦不也如此?他們訴諸語言並非旨在改造這個
            世界,而且深知個人無能為力卻還言說,這便是語言擁有的魅力。 語言乃是人類文明最上乘的
            結晶,它如此精微,如此難以把握,如此透澈,又如此無孔不入,穿透人的感知,把人這感知的
            主體同對世界的認識聯繫起來。通過書寫留下的文字又如此奇妙,令一個個孤立的個人,即使
            是不同的民族和不同的時代的人,也能得以溝通。文學書寫和閱讀的現實性同它擁有的永恆的
            精神價值也就這樣聯繫在一起。 我以為,現今一個作家刻意強調某一種民族文化總也有點
            可疑。就我的出生、使用的語言而言,中國的文化傳統自然在我身上,而文化又總同語言密切
            相關,從而形成感知、思維和表述的某種較為穩定的特殊方式。但作家的創造性恰恰在這種
            語言說過了的地方方才開始,在這種語言尚未充分表述之處加以訴說。作為語言藝術的創造者
            沒有必要給自己貼上個現成的一眼可辨認的民族標籤。 文學作品之超越國界,通過翻譯又超越
            語種,進而越過地域和歷史形成的某些特定的社會習俗和人際關係,深深透出的人性乃是人類
            普遍相通的。再說,一個當今的作家,誰都受過本民族文化之外的多重文化的影響,強調民族
            文化的特色如果不是出於旅遊業廣告的考慮,不免令人生疑。 文學之超越意識形態、超越
            國界,也超越民族意識,如同個人的存在原本超越這樣或那樣的主義,人的生存狀態總也大於對
            生存的論說與思辨。文學是對人的生存困境的普遍關照,沒有禁忌。對文學的限定總來自文學
            之外,政治的、社會的、倫理的、習俗的,都企圖把文學裁剪到各種框架裡,好作為一種裝飾
            。 然而,文學既非權力的點綴,也非社會時尚的某種風雅,自有其價值判斷,也即審美。同人
            的情感息息相關的審美是文學作品唯一不可免除的判斷。誠然,這種判斷也因人而異,也因為
            人的情感總出自不同的個人。然而,這種主觀的審美判斷又確有普遍可以認同的標準,人們
            通過文學薰陶而形成的鑑賞力,從閱讀中重新體會到作者注入的詩意與美,崇高與可笑,悲憫與
            怪誕,幽默與嘲諷,凡此種種。 而詩意並非只來自抒情。作家無節制的自戀是一種幼稚病,
            誠然,初學寫作時,人人難免。再說,抒情也有許許多多的層次,更高的境界不如冷眼靜觀。
            詩意便隱藏在這有距離的觀注中。而這觀注的目光如果也審視作家本人,同樣凌駕於書中的
            人物和作者之上,成為作家的第三隻眼,一個盡可能中性的目光,那麼災難與人世的垃圾便也
            禁得起端詳,在勾起痛苦、厭惡與噁心的同時,也喚醒悲憫、對生命的愛惜與眷戀之情。 植根
            於人的情感的審美恐怕是不會過時的,雖然文學如同藝術,時髦年年在變。然而,文學的價值
            判斷同時尚的區別就在於後者唯新是好,這也是市場的普遍運作的機制,書市也不例外。而
            作家的審美判斷倘若也追隨市場的行情,則無異於文學的自殺。尤其是現今這個號稱消費的
            社會,我以為恰恰得訴諸一種冷的文學。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文學世界,小說大觀,現代長篇小說'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577030400
    assert parsed_news.reporter is None
    assert parsed_news.title == '文學的理由'
    assert parsed_news.url_pattern == '19-12-23-11739453'
