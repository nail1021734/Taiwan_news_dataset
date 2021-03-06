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
    url = r'https://www.epochtimes.com/b5/13/12/1/n4023601.htm'
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
            《西遊記》是一部覺悟之書,講的是唐僧師徒四人去西天拜佛取經傳東土的故事,早已家喻
            戶曉,歷來為人們所傳頌。其中主要人物孫悟空正義、善良、智慧、勇敢,他忠心護師,全始
            全終;除惡揚善,明辨是非;堅心向道,矢志不移,一代英雄的真我本色與風采永遠留在了人們
            的腦海中。 孫悟空為東勝神洲傲來國花果山上一塊仙石,受「天真地秀,日精月華」孕育而
            生,一出世即「拜了四方,眼運金光,射沖斗府」,在花果山稱「美猴王」,「春採百花為飲食
            ,夏尋諸果作生涯。秋收芋栗延時節,冬覓黃精度歲華」。 他一心求仙訪道,向菩提祖師學
            了十萬八千里的筋斗雲,七十二般變化,從龍宮得到了重約一萬三千五百斤、可大可小的如
            意金箍棒。鬧龍宮,闖幽冥、大鬧天宮,被佛祖壓在五行山下。孫悟空內心雖嚮往天宮和眾
            神,卻不悟只有修心和積累功德才是正道,不能擾亂上天的規矩和綱常。 書中寫道:「富貴
            功名,前緣分定,為人切莫欺心。正大光明,忠良善果彌深。些些狂妄天加譴,眼前不遇待時
            臨。問東君因甚,如今禍害相侵。只為心高圖罔極,不分上下亂規箴。」五行山下,孫悟空反
            思後悔悟,渴望修行、向善、成正果。因此當觀音菩薩勸善時,他馬上說:「我已知悔了,願
            保護唐僧西天取經。」正如書中所說:「若得英雄重展掙,他年奉佛上西方。」 唐僧是一位
            慈悲為懷、一身正氣的聖僧,立志拜佛求取真經以濟眾生,意志堅定,持之以恆。孫悟空拜唐
            僧為師後,忠心耿耿地保護他去西天取經,一路上降妖除魔。經過白虎嶺時,狡猾的白骨精三
            次幻化為人形要害唐僧,被孫悟空識破打殺,唐僧肉眼凡胎不識妖,誤以為他枉傷人命而念緊
            箍咒,孫悟空抱著寧可自己頭痛也不能讓妖精害了師父的心念,義無反顧地打死了妖精。 唐
            僧將其從身邊趕走時,他不忍離去,使分身法四方圍住唐僧使其受拜,「噙淚叩頭辭長老,含
            悲留意囑沙僧」。回花果山的途中經過東洋大海時,「想起了唐僧,止不住腮邊淚墜,停雲住
            步,良久方去」。在花果山,「身回水簾洞,心逐取經僧」。 在他離開後,唐僧又遭遇了黃袍
            妖怪,豬八戒赴花果山請他回去。二人回去再次經過東洋大海時,孫悟空說:「我下海淨淨身
            子,師父是愛乾淨的,我自從回來後,這幾日弄得身上有些妖精氣了。」他對師父敬重、真誠
            ,心中時刻記掛著師父的安危和取經大業的成敗。 取經路上千難萬險,孫悟空從不畏懼退縮
            ,始終充滿必勝的信念,勇往直前。經常對唐僧說:「師父放心!沒大事。......有我哩!」、
            「我這一去,就是東洋大海也趟開路,就是鐵裹銀山也撞開門!」對魔難既不害怕,又不掉以
            輕心。戰獨角兕大王,連戰一天一夜,越戰越強。戰六耳獼猴,至天宮、地府、西天,直至將
            其「一棒打死」。 即使被壓在三座山之下或被金鐃扣住時也從不氣餒,依然「氣象昂昂,聲
            音朗朗」,想方設法除妖。豬八戒稱讚他是個「鑽天入地,雷打火燒,下油鍋都不怕的好漢」
            。他火眼金睛善識妖魔,手持金箍棒,「全憑此棒保唐僧,天下妖魔都打遍」,見惡必除,除惡
            必盡。 孫悟空善惡明辨,對殘害人民的妖魔徹底清除,不留後患;對百姓眾生則扶危濟困,救
            人救徹。在烏雞國,他掃蕩妖魔,為民眾辨明邪正;在車遲國,他解救了那些受妖精誣陷迫害
            的僧人,並勸諫國王「莫信妖邪,從此敬佛也敬道」,僧人們都感動地說:「齊天大聖,神通廣
            大,專秉忠良之心,匡正伏惡,濟人危難。」過火燄山時,他不僅搧滅了火燄山保證唐僧西行,
            而且還特意連扇七七四十九扇,斷絕了火種,使風調雨順,為百姓謀福。在比丘國除妖,救了
            一千多個兒童的性命,人們稱讚他「有仁有義,專救人間災害」。 經過鳳仙郡時,孫悟空看
            到此地因連年亢旱,民事荒涼,就立即上天宮求雨,了解到因那裡郡侯不敬天地,上帝見罪,立
            有米山、麵山、黃金大鎖,直等此三事倒斷,才該下雨。但亦有善解,若有一念善慈驚動上天
            ,那米、麵山即時就倒,鎖梃即時就斷。孫悟空回來告訴郡侯..「你只有改過向善,敬奉神佛
            ,感動上天,才會下雨。」郡侯聽後悔過自新,領著文武官員天天念佛向善,祭拜天地,滿城人
            民無一家一人不禮佛敬天,善聲盈耳。 所立兩座山都倒了,鎖鏈亦斷,上天普降甘霖。唐僧
            高興地對孫悟空說:「賢徒,這一場勸人歸善之善果,皆爾之功也。」沙僧說:「這場滂沱大
            雨,潤澤萬萬千千生靈!我也讚歎大師兄的法力通天,慈恩蓋地。」百姓們謝之不盡,孫悟空
            對百姓說:「福乃天賜。你等只一心向善,福自來爾!但只我們自今去後,保你郡人民年年風
            調雨順,歲歲雨順風調。」 唐僧師徒對佛理的堅定信仰和為了救人、濟世的慈悲心懷感動
            著後人,他們不為任何外物所迷惑,歷盡艱辛終成正果,更使人們認識到只有向善才是人生正
            道。孫悟空忠正、坦蕩、本真至純的精神鼓舞著人們追求美好和光明,不與黑暗勢力同流合
            汙。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文學世界,文學賞析,書評書話'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1385827200
    assert parsed_news.reporter is None
    assert parsed_news.title == '盪濁揚正氣 乾坤美名傳'
    assert parsed_news.url_pattern == '13-12-1-4023601'
