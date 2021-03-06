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
    url = r'https://www.epochtimes.com/b5/19/11/25/n11678991.htm'
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
            釋迦牟尼佛說一粒沙有三千大千世界。沙中沙,世界疊世界,無窮無盡,浩瀚的宇宙,最終只能
            用「其大無外,其小無內」來詮釋,所以佛祖是最偉大的科學家。在我們同時同地,是否也存在
            無數橫向、縱向的空間和時間?那麼天外天,人外人,就不是傳說或神話,是誰可以看到或接觸
            到另外空間的天人? 一位25歲從事設計的聰明女孩,自從國中時期,不知道什麼因緣,她開始
            可以聽到另外空間的聲音,家人以為她幻聽,但行為沒有異常。到高中時期,漸漸可以看見另外
            空間的生命體,包括奇形怪狀,五顏六色的人和動物。設計師後腦勺的頭髮一直掉,後來竟至
            全禿,叫鬼剃頭。月經越來越少,到高中時已閉經。設計師如果沒有上婦科去催經,就一整年
            月經都不來。這種被動式,老打催經針,會干擾賀爾蒙運作。她怕日久引發惡性病變,想試試
            中醫。 當設計師出現時,整個人看去好像沒發育完全,而停留在國中期含苞未開的樣子。身高
            149公分,體重39公斤,面色蒼白臘黃,眼神閃爍又漂浮不定,看去怪怪的,說話聲音細而低沉,
            像陽氣不足。設計師說最擔心頭髮和月經的問題。 針灸處理:提陽氣,除陰氣,針百會穴;月經
            與任脈關係密切,因任脈為陰脈之海,針任脈起點承漿穴,斜刺至下唇緣凹陷處;陽明經多氣
            多血,鼓動氣血,針天樞、合谷穴,藉以升降氣機;經血乾枯,針三陰交穴,健脾益腎,養血調肝;
            先天腎氣不足,針任脈之氣海穴;後天脾氣失調,針三陰交、足三里穴;胞宮氣血閉鬱,針血海、
            三陰交穴,其中三陰交穴針至地部,令針感逆經向趾端方向放射,隨即提至人部;促排卵,針關元
            、中極、子宮、三陰交穴;刺激生髮,先圍刺點刺毛髮禿處,後針血海、三陰交穴、禿處由上往
            下齊下3針排刺。 原本月經,按月而至,如潮有信。但月圓月缺,已過了三輪,月信如細水還
            來不及長流,源頭已被抽刀斷水,那是為什麼?這位設計師真有耐心,月經一點動靜都沒有,還是
            不離不棄繼續來看診!不喜歡吃藥的她,終於願意試試看。 又是明月照夜空,而我難以舉頭,
            望月愁更愁啊!因為所有通月經的中藥,所有有關閉經的理論全用上了,仍然月信渺無音訊!我
            以天床地被,枯坐書案前,靜吟蘇東坡的「缺月掛疏桐,漏斷人初靜。誰見幽人獨往來,縹緲孤
            鴻影。」而可愛的設計師服藥後望斷天涯半年了,加針灸前後近一年,她的月經仍未至,卻無恨
            也無悔的,每次看診只是望著我傻笑! 有一天,我靈機一動,對設計師說:「我們來關閉妳的
            陰陽眼!」她「啊!」了好大一聲!不知道是驚慌?還是大疑問?設計師說連白天走過土地公廟,
            土地公還叫住她,令她好害怕!要怎麼關?我也不知道,總要試試看,我說:「最關鍵點是不回應
            ,不論所見所聞,不要有任何反應,例如驚恐、害怕,或對話。全當作看電影,視而不見,聽而
            不聞!甚至閉上眼睛,以防神光外洩,也洩掉肝血和腎精。」剛開始,設計師很難做到,但她努力
            配合試試看。 特別囑咐:11點以前要睡覺,晚上設計師看到生命體特別多,子時一陽生,她的
            陽氣一直被陰氣所啃噬。天黑儘量少出門,晚上出去辦事,9點以前要回家,尤其不要停留在
            樹蔭下。勿到陰廟拜拜。勿奔喪,勿探望重症病人。少吃寒涼性食物。用鹽巴和米混拌,放臥房
            四角落,勿用布包或盒裝,3天換新。每晚用艾條灸湧泉、關元穴各5分鐘,勞宮穴關鬼牢必薰
            10分鐘,見到異形多時,灸10~20分鐘。 設計師因被另外空間生命體吵得很煩,她說國中時
            收驚還有效,以後就越來越無效,束手無策,也不敢隨便向人訴說,人家會認為她精神異常。
            男朋友剛交往,不久就會因她陰冷冷的,令男朋友不舒服,莫名的就躲開了!最後都是傷心收場!
            所以一直都是孤家寡人,小姑獨處,落寞,她決定一試。 針灸改針人與神靈交會的百會穴;安神
            ,針本神、神庭、四神聰穴輪用,針鬼宮人中穴、鬼信少商穴、鬼壘隱白穴、鬼心大陵穴、鬼路
            申脈穴、鬼床頰車穴、鬼市承漿穴、鬼窟勞宮穴、鬼堂上星穴、鬼腿曲池穴,這些穴,有空用
            艾條各灸5分鐘,每次選3穴輪灸。處方只用人參養榮湯,歸脾湯,把耗散的枯血補回來。 一個
            月後,設計師的月經竟然不需打催針而自行報到,她高興的都快哭出來,抱著我說:「醫生,我
            好愛你哦!」其實之後月經也沒按月來,半年只來2次。有一天設計師手足舞蹈的拍手說:「
            醫生,我終於關上陰陽眼了,再也看不到、聽不到奇怪的異形,好棒哦!」她的臉色開始紅潤,
            很嬌美,人也變得快樂,青春有活力,像春花怒放般的燦爛! 之後設計師因工作搬家,就介紹
            當地醫生讓她去看診,但她還是排除萬難來看診。每次月經來就高興的打電話來報喜!漸漸的
            月事如潮有信而來。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文明探索,人體修煉•長生延年,陰陽五行另類療法'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1574611200
    assert parsed_news.reporter is None
    assert parsed_news.title == '天外天'
    assert parsed_news.url_pattern == '19-11-25-11678991'
