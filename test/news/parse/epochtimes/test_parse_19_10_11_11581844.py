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
    url = r'https://www.epochtimes.com/b5/19/10/11/n11581844.htm'
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
            愛書成痴 樂在其中 從小,愛書成痴。就像吞雲吐霧的癮君子,可以食無肉,居無竹,但若一天
            沒有書看,便覺意興闌珊,人生無趣。 記得1976年唐山大地震,天塌地陷,死傷無數,整個夏秋
            季節,餘震連綿,滿村子人都不敢回家,只得在空曠之處安營紮寨。某一日,我有幸淘了本好書,
            一時看不完,自然百事無心,寢食不安。天黑之後,手執一盞煤油燈,坐在門檻上看得時哭時笑,
            劉海被燒去一撮也渾然不覺。夜深人靜,母親一遍又一遍低聲呼喚,我正魂遊太虛,自然不聞
            不見。十遍二十遍之後,母親終於不耐煩,劈頭把燈奪去:「人說你是個書呆子,我看你是個
            書蟲子。地震隨時會來,坐大門洞底下,問你要書還是要命?」寶物遭劫,我一時魂魄盡失,
            飛身來搶:「哎呦,俺的娘哎,沒了書,我還要命作甚?」 「書中自有黃金屋」,古人之言,誠不
            我欺,憑著痴痴呆呆,日夜無休地鑽書,居然鯉魚跳龍門,進城當了機關幹部。只可惜上世紀90
            年代初,砸三鐵(鐵工資、鐵飯碗、鐵交椅)流風所至,我一下子被吹落商海,任意西東。三千萬
            國企員工猝然下崗,四顧茫茫,謀生無計。那些年,示威靜坐,打橫幅群體上訪,全國各地浪潮
            洶湧,喧嘩一時。可高高在上的官老爺們如海岸邊黝黑的礁石,沉默如鐵,巋然不動。所有國資
            流失,員工失業的訴訟一律不予受理。只派出個長髮披肩,宛如獅首的劉歡,在央視聲嘶力竭
            「......看成敗人生豪邁,只不過是從頭再來」。 我呢,叨天之幸,早年就搞了個賣書的流動
            貨車,自己看書固然方便,對家計也不無小補。小小貨車,猶如一把降落傘,讓我得以徐徐而下,
            平安著陸。貸款一萬,租房一間,我的書店總算應劫而生。 天性疏懶,無意功名,做一個小小
            書商,可以溫飽,也算雅事一件,足矣。平房小院,細雨梧桐。一地月季開遍,牆頭,屋脊,凌霄
            花在風中搖曳。書案前,清水牆面掛著一條原白色布幅:閒居紙筆為伴,至樂莫過讀書。左下角
            畫一個竹筒,疏疏落落插著兩三枝毛筆。簡簡單單,大片留白。乃是我大學時代在濟南買的
            心愛之物。 兒子還小,雜事也多,書店一直是僱工經營,我其實不是天天都去。那時候,我家
            先生開始修煉法輪功,起早睡晚,樂在其中。 「我的書啊!我的錢哪!」 真、善、忍三字,
            真實不虛 一日,先生從外回家,鄭重其事地對我說:「法輪功書籍太熱銷了,市面上到處都是
            盜版,紙張發黑、錯字連篇,太不嚴肅了,也對師不敬。功友們都來找我,看上哪去進些正版的。
            」「能上哪去呢?一點沒頭緒。」「這樣,1994年不是開發區管委會請師父來咱這講過法嗎?
            當年負責接待的功友都在,他們說省青年管理幹部學院出版過大法資料,你去找找看,事要能成
            ,也是功德一件」。 故地重遊,自然心下甚喜。二話不說,第二天一早即便起程。四面荷花
            三面柳,一城山色半城湖。啊,濟南,久違了。你好,我的大明湖,你好,我的趵突泉。 青年
            幹部管理學院早已不再經營大法資料。經人指點,尋尋覓覓之下,進入一條彎曲的小巷。那是
            一個很小的書店,女主人從國棉一廠下崗,長得面色白淨,小巧玲瓏。第一次進貨,不知行情,
            我只敢批發了一箱藍色燙金封面的《轉法輪》,紙張厚實,字體碩大,單價才十二元,相當經濟
            實惠。 因為正版難得,市面上焦渴已久,自從擺上大法書,小小的書店很快門庭若市。人們
            呼朋引伴,三五相約,給自己買,給親友送,一買一包,一裝一袋,如風捲殘雲,即刻清零。讓我
            驚喜之餘,不由暗暗咂舌。 一天,在勝利油田鑽井公司大會堂召開法會,一年一度,盛況空前。
            我拉了小弟幫忙,在旁邊擺了個簡單攤位。圖書、音像、法輪章,一疊又一疊書籍,高低錯落,
            像小山一樣連綿起伏。收拾停當,兩個人站在案桌好整以暇。誰曾想,摩肩擦踵,熙熙攘攘的
            人群,足足幾千人,像大海漲潮,洶湧澎湃,卷地而來。書攤如海邊的礁石,頃刻沒頂。我手足
            無措,心下大急,完了!完了!我的書啊!我的錢哪! 等一片喧囂終於過去,我才慢慢睜開眼睛,
            仿佛滄海桑田,高聳的書山已被風暴刮平。我心跳如鼓,掙扎起來去清理現場,正如圓明園大火
            之後,憑弔那些斷壁殘垣,一地廢墟。 「姐姐!姐姐!錢不少哎,你看這麼一大堆!」聽小弟在
            那邊狂喜大叫,我尚在面如土色,手指發抖。不是做夢吧?我急步向前,低頭檢視,不禁喜心翻倒
            。居然真的錢貨兩清,一分不少!我使勁眨眨眼睛,又咬咬自己的下嘴脣。老天!老天!真、善、
            忍三字,的的確確,真實不虛。 又一日,一鄉間打扮的老者來店買書,次日折返,說算錯了帳目
            。我心下歉然,立即從櫃檯裡翻出一沓票子。老者笑著擺手:「不是!不是!你誤會了。是店裡
            多找了我錢。路遠,騎車跑了這麼半天。」聞言,我趕忙端茶讓座,再三道謝。如此君子之德,
            實在讓人肅然起敬。 從此,法輪功修煉者不單單只是我的客戶,更是一群可以傾心相交的朋友
            。大街上相見,彼此十分親熱,執手為禮,絮絮閒話家常。我的書店大開方便之門,可賒可欠,
            在法輪功圈子裡聲名鵲起,無人不知。遠近幾十里,客似雲來,絡繹於途。 那些年,公園裡打坐
            煉功的人們,既有後生小子,更多垂垂老者,那些舒緩從容,悠遊自得的煉功人,正是最尋常不過
            的街頭一景。 走過血雨腥風的十年文革浩劫,大家都慶幸有今天安穩祥和的日子。希望長此
            以往,歲月靜好,不要翻江倒海,再生事端。
            '''
        ),
    )
    assert parsed_news.category == '美國,舊金山,灣區廣角,文化腳步'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1570723200
    assert parsed_news.reporter is None
    assert parsed_news.title == '紀實散文:一夜驚夢'
    assert parsed_news.url_pattern == '19-10-11-11581844'
