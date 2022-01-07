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
    url = r'https://www.epochtimes.com/b5/19/12/26/n11746439.htm'
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
            樹多必有枯枝,人多必有白痴。在人生的路上,如月有陰晴圓缺,譬如朝露的人生中,雖短卻有
            人寸步難行,日子煎熬難耐,不知如何是好?如果再腦殼發燒,簡直就是雪上加霜! 一位32歲
            小姐,鮮亮而紅的月亮臉,像炸開的大氣包,水牛肩,嘴翹翹的,坐下來,話一開口就淚流滿面,
            泣不成聲。我拍撫她肩膀,握握她的手,拿手紙幫她擦眼淚。冷靜下來後,大氣包開始述說病情
            :「醫生,我的臉燙到不能睡,不能見陽光。已經看病17年了,類固醇愈吃愈多,病也愈重,覺得
            自己是個廢人,哪裡也不能去,什麼事也做不了,沒有人敢愛我!我是不是得了不治之症?」她
            那眼睛含著千萬恨,恨及天涯,一把鼻涕,一把眼淚! 針灸處理:先安神,針神庭、神門穴;易動
            怒,情緒不穩,瀉肝火,針太衝穴;解血毒,針血海、曲池穴;瀉血熱,針陽池、陽谿穴;補腎水
            ,瀉肺熱,針太谿穴;瀉陽明經熱,針合谷穴;引陽明經下行,針內庭穴;一派瀉法中要加補法,
            微補陽氣,增加機動力,陰中求陽,針足三里穴;四肢冰冷,強心,引心火達四肢,針內關穴。特別
            囑咐:雖臉很熱不能吃冰品,熱被冰所鬱更散不去,使病情更加膠著。 大氣包經過針灸吃藥後
            ,臉發燙時間雖然縮短了些,可是她情緒很不穩定,時常發飆。寒流一來,四肢冰冷,身體也冷
            得要命,一蓋上棉被,臉又燙得不行,即使用冰水潑臉,但是只會舒服幾分鐘,大氣包被折騰得
            整晚也不能睡。大氣包來門診時,一直在哭!一直向我抱怨病還沒好!17年的病要如何在短時間
            之內緩解?我也傷透腦筋! 有一天大氣包來診時,竟不哭了,但她表情兇怒的說:「醫生,我
            長得這麼醜嗎?」怎麼突然問這個問題?我不假思索的回答:「妳很可愛啊!」大氣包立即說:
            「我晚上穿黑衣服黑褲子,黑夜中躺在馬路中間,想讓車子輾過,結束生命。可是所有車子都
            從我身邊繞過,都不肯壓我,我有這麼醜嗎?」大氣包生氣的臉真醜! 我沉默了一分鐘,瞪著她
            ,嚴肅厲聲的說:「妳這小子沒勇氣活,也沒勇氣死,要死還要害家人!妳以為死了就一了百了,
            沒那回事!人死了也沒有離開三界,除非修行超出三界。三界內的生命都叫人,都很苦,比人低
            的還有另一種人,再低的有地獄,比地獄低的還有很多,妳想死了到哪裡去受苦?像你這樣不存
            善念的死法,死了也要還業,在層層償還業力中受苦,去到另外空間,比現在作人還痛苦千倍
            萬倍。」她聽了愣住了!人生真是苦海無邊!自殺解決不了問題。 我又換了和緩語氣,拍拍
            大氣包的肩膀說:「我知道妳受了很多苦!妳這樣叫別人輾死妳,別人無辜犯了刑事罪,要被關
            ,還要賠償妳的家人。妳的病不會馬上好,治療需要過程,都已熬了17年,何必急於一時?受苦
            會消業力,業力消越多,病也去越多。病越久越需要長一點時間來調整,妳想要立刻好,要醫生
            給妳開類固醇、特效藥,反而使血管愈脆弱。身體器官有一定承受力,就像車子都有一定馬力
            ,過度治療一時的好是暫時的假象,病沒治好又傷肝傷胃,最後傷腎,這就是台灣成為世界第一
            洗腎國家原因之一。」 我找了一位病人出生即患異位性皮膚炎,已求醫33年,和另一位上半身
            發紅發疹已15年,經過治療一段時間後,都已入佳境,請他們給大氣包鼓勵,這樣她才會定下心
            來接受治療。以後大氣包來診就不再苦瓜臉,逗逗她也會笑了,相由心生,病情就一直有進展。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文明探索,人體修煉•長生延年,陰陽五行另類療法'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577289600
    assert parsed_news.reporter is None
    assert parsed_news.title == '朝露人生去日苦多'
    assert parsed_news.url_pattern == '19-12-26-11746439'
