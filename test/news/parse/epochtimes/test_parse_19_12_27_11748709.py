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
    url = r'https://www.epochtimes.com/b5/19/12/27/n11748709.htm'
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
            第七章 十年生死(5) 王庭。 鐸克齊負立多時,心內惴惴不安,抬眼之間,望見皇甫只手扶額
            ,閉目不語。 「納蘭庭芳何在?」皇甫道,並不睜眼。朱公公道:「已派人通傳武平王府,想來
            該在路上。」 皇甫眉心一皺,道:「不等了。」袍袖一揮,正襟危坐。 刑部大牢火災,莫少飛
            被人救走,鐸克齊跪地不起:「老臣有罪——」 「你又——何罪之有?」皇甫手按奏摺道。 鐸克
            齊略述刑部監牢大火之事,不敢抬眼,靜待發落。少時不聞其聲,偷偷抬眼,只見皇甫手持朱筆
            ,正在批改奏摺,凝眉之際,隱有怒色。皇甫再拿一本,正對上鐸克齊雙眼,道:「已撥銀兩,再
            建囚牢......」轉念一想,道:「便在京郊西山,該處地勢險峻,可關押萬餘人。」 「老臣
            遵命。」鐸克齊伏地道,心下不解,緣何王上也不生氣,還下令督造大牢。費解之際,納蘭庭芳
            上殿。皇甫奏摺一合,語帶微嗔:「可是讓孤久等。」 「王上恕罪。」納蘭跪地叩首。 「此
            番又有何說辭?」皇甫道。 納蘭道:「王府進入刺客,內眷遭人劫持。」 皇甫眼神一凜,道:
            「宛月何如?」 納蘭拱手道:「回稟王上,宛月尚在府中;被劫持者,乃臣之側福晉,哈爾奇.昭
            雪。」 「嗯?」鐸克齊捋著鬍子,眼中多有不滿之色。 皇甫清咳一聲,道:「鐸克齊,說罷。
            」鐸克齊拱手道:「武平王可知,方才刑部大火,莫少飛讓人救走了。」 「嗯?」納蘭眉心一
            皺,道:「刑部戒備森嚴,鐵桶一般,緣何能讓人劫囚?」鐸克齊面色陰沉:「劫囚之人何者?
            王爺心中沒有數麼?」納蘭道:「還請尚書大人示下。」鐸克齊再要反唇相譏,忽聽皇甫一喝,
            二人皆閉嘴。 「叛軍名冊一事,查得如何?」皇甫道。 「回稟王上。本已查到莫少飛,不想
            其人越獄,線索已斷。」鐸克齊道。 納蘭道:「日前尚書大人所言,不是還有一人?」 鐸克齊
            氣得鬍鬚飛起,道:「那人突發疾病,暴斃而亡。」 納蘭冷笑一聲,道:「想必是嚴刑拷打,含
            冤而死。」 「住口。」皇甫打斷,又對納蘭道:「你也莫想隔岸觀火,享得清閒。叛軍名冊一
            事,禁曲一案,現令你二人協同辦案。禁曲,孤不想再聽聞其事;名冊,無論爾等雷霆手段,速翻
            出此冊,呈孤御覽。」 「臣遵旨。」二人拱手道。 「鐸克齊退下。」皇甫道。 殿內只餘皇
            甫、納蘭二人。皇甫步下龍椅,將一封書信交予納蘭,道:「這是有人祕呈之名冊,你看可信否
            ?」納蘭打開閱視,只見其上所列,為首一人,曲正風乃是金山,登時啞然失笑。 「為何發笑?
            」皇甫道。 納蘭收斂笑意,道:「江湖傳言,曲正風身長八尺,聰勇精悍,不似金山。」皇甫道
            :「江湖傳言,曲正風乃武林盟主,常年以金銅覆面,無人曾見其面。金山身形雖有千差,但亦
            不知其是否偽裝,作下萬別,以擾亂視聽。」 「再者——」皇甫續言:「密探來報,曾言親眼見
            過叛軍首領白門柳,出入金山府邸,令人生疑。」 納蘭沉默不語,頓了一頓,出口道:「白門
            柳,正是劍聖風軒逸,其人曾在江湖享有盛名。後來因白門血案一事,失心喪志,改換容顏;我
            等與其對峙之時,方才發現此事。」 「劍聖?白門血案?」皇甫皺眉凝思。 納蘭道:「王上
            難道忘記?蕭企親自追殺叛逃家丁?」 「蘇州蕭園。」皇甫面色凝重,踱步有思,忽地轉頭,
            看向納蘭道:「既是劍聖,當有江湖勢力,豈可輕忽?」說話之間,面色甚憂。納蘭拱手道:「
            王上莫急。西南侯門攻伐武林,現下江湖大亂,各方勢力碰撞,不成一體。」 皇甫皺眉道:「
            然則,孤卻聽聞那白門柳正是當今武林盟主。」 納蘭一愣,未及料到皇甫何時開始關注江湖
            之事,轉念之間,道:「正是。然則現下侯門勢大,臣此前多有試探,此人無心天下,只想爭得
            武林首位,揚名江湖。」 「侯門,又是何物?」皇甫道。 「侯門乃西南一方門派,擅於用毒,
            二十年前曾顯赫於武林;後不知何事,日漸零落。其門現主夜洋掌門,雖其貌不揚,但也算年少
            有為,智謀過人。」納蘭略述其事,皇甫暗暗心驚,陷入沉思。 納蘭疑惑:「有甚不妥之處?
            」 皇甫嘴角一牽,坐回龍椅之上:「並無不妥。孤要離宮數日,爾不可宣張。」 「所因何事,
            又私自出宮?」納蘭面現憂色。 皇甫喜上眉梢,道:「多年之後,夙願終償。」交予納蘭一封
            密旨,道:「希望孤回宮之時,爾已得叛軍名冊。」 「是。」納蘭接信,告退離宮而去。 話說
            金府抄家,小翠兒捨命相護,金海逃出升天,無處可去。
            但尋舊日施恩之人,皆遭推諉,不與救濟,更甚者報官來捉。金府可謂樹倒猢猻散,正是昨日
            黃花,過街老鼠,人人喊打。金海四下遊蕩,無處可去,忽然看見街市一處,人人提著木杆,煙霧
            繚繞,便似爹爹手中之物,不過材質差些,遂抬腿進入。 老闆見其身有綾羅,鑲金配玉,看著像
            個財主,便然笑臉相迎,奉上數只菸袋。交談兩句,老闆心下便知:「正好遇上個傻冒,來敲上一
            筆。」遂挑了上癮的毒,送與金海。金海回憶金山動作,吸了兩口,竟然渾身飄飄然也,不餓也
            不難過了。於是乎,整日泡在大煙館裡,如此半月,全身上下洗劫乾淨,一腳踢出門外:「原來
            是個騙吃喝的,拿了錢再來。」 金海上前打門求施捨,未叫出煙桿,卻敲出五六個壯漢,一番
            毒打,眼睛鼻子皆冒出血。金海大駭,慢慢爬到牆邊兒,就著暴雨冷風,睡了一夜。蒞日,風和
            日麗,幾個乞丐看著天氣不錯,也便出工。到得牆邊兒,卻見個死狗賴著不動。 「哎喲,待爺爺
            看看......啊?這不是金府的胖公子,緣何幾日不見,瘦成皮包骨?」一個乞丐打趣道,吐沫
            噴了一手,抹在金海臉上:「來,爺爺好好洗洗,也來討個賞錢。」金海屈辱至極,猛力一推,
            那乞丐無有留神,竟坐倒在地,立時怒然躍起:「小叫花子,還真當自己是大老爺,來人給我
            揍他。」幾個乞丐一哄而上,拳腳相加,金海舊傷未好,再加新傷,重重吃痛,哭爹喊娘。 「
            官差來了,快跑。」忽聽一個聲音,眾人一鬨而散。金海抱頭縮在牆角:「別抓我,別抓我,我
            啥都不知道。」叫喚一陣,方才放下手,四下裡無人,只有一個老乞丐,晒著太陽吃發了霉的
            花生豆。 「給我兩個。」金海道。 老乞丐看其一眼,伸出手去:「都給你。」金海扒開拳頭
            一看,啥也沒有,登時惱怒,悻悻而去。拖著瘸腿,蹭回金府巷,但見門上白條封禁,四周皆是
            官兵,心下難過,蹲下抱頭哭了一陣。待天晚時分,秋初風涼,方才無淚再流,擤了個鼻涕,雙手
            揣袖,衣衫單薄,往繁華地方走去。 落雁閣繁華依舊。金府勢敗之後,樹倒猢猻散,有人牽連
            倒楣;有人趁機發財。門口雜役見著面熟,走下台階一看,竟然是金海,心下感慨,吁嘆一番。
            回去廚房,拿了碗飯出來。金海身體早讓煙毒掏空,多日未食,頭暈眼花,雙手發抖,鼻子聞見
            飯香,抓米而食。雜役但見其狀,既是可笑,又是可憐,嘆了口氣,道:「老闆家的,吃完便走吧
            。官府知你是此地老闆,正守著要捉人,今日才散去。您老可好自為之吧。」搖了搖頭,回轉落
            雁閣。 盆大的海碗,竟讓金海吃了個底朝天,就著碗邊,米粒添淨。忘情之際,竟不聞遠處鐵蹄
            聲響,街上路人如鳥雀驚飛。趙子豫下馬,厲聲喝道:「有人舉報,言金海在此出現?」 「大人
            明鑑,未有啊。」老闆娘舉著粉帕上來招呼。趙子豫瞪了一眼,老闆娘嚇得跪地,道:「大老爺
            ,那金海巴不得逃之夭夭,怎會回來此地?」 「搜。」趙子豫下令,落雁閣人仰馬翻。 「哎呦
            ,這還讓不讓人做生意啦。」老闆娘坐於地上,哭爹喊娘。脂粉之氣,令人作嘔,趙子豫負手
            出來,立於門前。但見紅燈綠帳掩映之下,一個乞丐,蓬頭垢面,舔著光溜溜的海碗,心下一慟,
            不禁落下淚來,長嘆一聲。 兵士出來,道:「大人,無有發現。」 趙子豫道:「既然如此,再去
            別處搜,走。」說罷,上馬離去。 是夜,金海蹲在牆角打盹兒,突然被人迷暈。再醒來時,只見
            日光晃晃,身上多了只荷包,沉甸甸的,立時坐起來看,竟是好幾錠白銀,登時心內大喜。翻將
            出來,方才發現原來自己是躺在棺材裡,心內嘆道:「上次險些死掉,便有了個好爹爹。此次
            棺材裡躺一躺,憑空多了這些銀子,哈哈哈哈。」大笑著下山去了。 到得一處城鎮,尋了個
            煙花之地,又有大煙可抽,混跡一月,銀子敗光,又成乞丐。隨著一夥兒流民,四處尋摸吃食。
            越走黑夜越長,天氣越冷。突然一日,遇上劫匪,一眾流民皆死於非命。金海菸癮屢犯,全身
            抽搐,口吐白沫,休克不醒。 再次睜眼,全身濕透,冰冷僵硬,漫天暴雨,如若瓢潑。金海顫抖
            不已,勉力起身,但見水霧茫茫,屍首遍地,雨血成河。心裡害怕,越逃越遠,日頭越大,終跑
            不動,摔倒在此,仰躺望天。日光晃晃,腦中空空,今生之事,歷歷在目,死期將至,心中未
            有一絲害怕,反而暢然無比,嘴角竟牽起微笑。 耀耀日光,晃得人眼難開。金海心下好奇,向
            著山丘上一片白光而去。揉揉眼睛,白光熠熠;環顧四周,荒山野嶺。「不知是啥,待爺爺看
            上一看。」金海腳步踉蹌,彎腰去拾,腳下一滑,撲倒在地,但感光滑細膩,溫暖無比。滾了
            幾滾,套在身上,竟無一絲重量。 「好像是件衣服,待爺爺來穿上一穿。」金海迷迷糊糊,
            將天衣往身上一罩,洋洋得意,走起了四方步。突然,只感周身輕盈,似腳步離地,天衣閃爍耀眼
            光芒,瞬息之間,消失不見。山林靜寂依舊,杳無人煙。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文學世界,小說大觀,現代長篇小說'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577376000
    assert parsed_news.reporter is None
    assert parsed_news.title == '天地清明引 東流水-十年生死5'
    assert parsed_news.url_pattern == '19-12-27-11748709'
