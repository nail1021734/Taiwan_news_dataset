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
    url = r'https://www.epochtimes.com/b5/19/4/21/n11201856.htm'
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
            我是來自中國大陸的人權律師李明,於去年逃離專制統治下的中國。 中國社會的人權律師
            群體,是中共現行極權體制下的一個特殊職業團體,其目前人員500人左右,占中國從業律師中
            的比例僅僅不到四百分之一,這一數據的結論是根據目前中國從業律師人數約35萬和自願加入
            中國人權律師團成員不超過500人的現實計算得出。眼下他們正在受到中共當局的強力打壓和
            重點迫害,生存空間也被反復的壓制而出現岌岌可危狀態,其受威脅的根本原因是為宗教人士
            ,民主人士和社會弱勢群體的合法維權和無罪辯護,而觸犯到中共敏感的統治底線。 從2015
            年7月9日淩晨抓捕中國人權律師包龍軍、王宇和他們的兒子,到次日抓捕北京鋒銳律師事務所
            的周世鋒及大多數加盟律師開始,在短短的數天之內,全國23個省市,被逮捕、刑事拘留、帶走
            、失聯的人權律師高達320餘人,這些人權律師和社會活動、異議人士被以所謂顛覆國家政權
            的罪名或判刑或處罰或警告或失去賴以生存得來不易的律師職業 ,製造了震驚中外「709
            事件」。 自此以後,更有余文生、李玉菡、李和平、祝聖武、隋牧青、謝陽、彭永和、文東海
            以及2017年被強制失蹤至今600多天的高智晟律師等等優秀勇敢的人權律師相繼被受到整肅
            ,限制執業限制出境離開中國的情況,受邊控上全國重點控制人員黑名單的人員比比皆是,去年
            5月3日的丁家喜律師和今年4月1日發生人權律師陳建剛,在北京機場因可能危害國家安全而
            不能到美國學習的案例,就 足以說明中國人權律師團體已經成為中共當局重點布控人員,已經
            成為中共當局從今年年初以來「掃黑除惡」的物件。 我本人因為堅守自己的信仰為法輪功
            學員無罪辯護,參加反對酷刑聯盟和接受境外新聞媒體的採訪,向媒體披露法輪功學員案件的
            內情內容等,也不能倖免於難,在2017年6月被上海市司法局強制註銷律師執業證。 中共當局
            持續針對人權律師採取了一系列的整治活動到近期來的清洗運動中可以看出,中共不僅僅要對
            中國人權律師大開懲戒之門,重要的是要消滅產生中國人權律師這一群體生存生活的土壤,
            以形成中國律師對中國的現行獨裁體制三緘其口明哲保身的連鎖效應,然而,中國民眾爭取
            自由民主法治文明的抗爭風起雲湧的今天,中國人權律師團體的成員和其他群體的國民一樣,
            正在進行著艱苦卓絕、形式多樣的抗爭。 與此同時,中國境內的其他群體也在受到大規模的
            整肅打壓和迫害,例如一直以來對法輪功學員的殘酷鎮壓,對民主人士對訪民對維權退伍軍人
            對P2P暴雷難民,尤其是近期在新疆對維吾爾哈薩克人設立百萬集中營,更使整個中國社會
            處於風雨飄搖動盪不安之中。 與此同時,中國境內外的抗暴風潮也在迅速增長,作為反抗中共
            暴政的一個重要組成部分,由法輪功學員主辦的三退服務中心自2004年11月成立以來,順應
            天意民意,結合九評共產黨,解體党文化等系列文章在中國大陸的遍地開花,中國的大江南北
            體制內外,掀起了一場三退運動,這場曠日持久運動從起初的數十人,幾百人,上千人,到每天的
            上萬人拋棄中共統治的自願自救運動,截止到2018年3月23日三退人數已突破3億人,而到現在
            ,每天拋棄中共統治聲明三退的人數在八到十萬人之間,有時每天的三退人員高達10萬人以上
            。 這組數據明確的告訴我們,人心所向勢不可擋。共產黨的大陸統治已經到了眾叛親離,人神
            共憤,窮兇極惡,窮途末路的地步,在中國共產黨末日到來之前,讓我們共同站在神佛一邊,堅守
            真善忍的信念,團結互助相守以望。 當下的中國,中共的殘暴統正面臨著隨時解體崩潰的地步
            ,一個嶄新的中國將要誕生,讓我們在這個時刻到來之前,堅守真善忍的理想信念,拒絕臣服和
            奴役,拒絕與中共妥協讓步,堅決地對中共的統治說不,同時也作為我本人的公開退出中共的
            公開聲明。 謝謝大家。
            '''
        ),
    )
    assert parsed_news.category == '北美新聞,美國華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1555776000
    assert parsed_news.reporter is None
    assert parsed_news.title == '大陸維權律師:三退迎來嶄新中國'
    assert parsed_news.url_pattern == '19-4-21-11201856'
