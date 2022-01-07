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
    url = r'https://www.epochtimes.com/b5/13/7/24/n3924107.htm'
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
            7月23日(週二),英國威廉王子、凱特王妃和他們的新生小王子在倫敦聖瑪麗醫院前
            現身。 露面時,這位英國王室第三順位繼承人,包裹在奶油色的毯子裡,由母親凱特王妃
            抱著。與此同時,威廉和凱特向外面守候的眾人揮手。 威廉王子表示,兒子長的比較像凱特,
            「他有她的容貌,謝天謝地。」 星期二晚,這對夫妻帶著男嬰離開醫院,搭乘一輛黑色SUV
            前往肯辛頓宮。迄今威廉和凱特仍未公佈兒子的名字。 男嬰出生在倫敦夏令時週一下午
            4時24分,重達8磅6盎司。 王室發出一份聲明說,威廉和凱特「再次感謝醫院所給予他們的
            護理和治療。」 週二晚,威廉王子的父親查爾斯王子,在妻子卡蜜拉的陪同下來到醫院 。
            他告訴記者,這是「了不起的。」 凱特王妃的父母早前就已來到醫院。凱特的母親告訴記者,
            母子狀況都「非常好」,她和丈夫作為祖父母,感到「非常興奮」。 凱特的母親還告訴記者,
            皇家寶貝「絕對漂亮」。 小王子取何名?全球關注 小王子一出生,已經被冠上正式頭銜
            劍橋王子 HRH Prince(forname)of Cambridge,至於他會取什麼名字?已成為各界關注
            的另一焦點。 通常皇室成員的名字都是長長的,例如劍橋公爵(威廉王子)的全名是
            威廉亞瑟菲力浦路易士(William Arthur Philip Louis);王室寶寶的祖父威爾斯親王
            (查理斯王子)的全名是查理菲利浦亞瑟喬治(Charles Philip Arthur George);叔叔
            哈利王子是哈利查理斯亞伯大衛(Henry Charles Albert David)。 根據英國博彩
            公司 Paddy Power 的資料,外界押注最大的前五名分別是:喬治 (George)、詹姆斯
            (James)、亞歷山大(Alexander)、路易士(Louis)以及阿爾伯特(Albert)。據悉,迄今
            已有5萬多人押注喬治(George)。 依據英國皇室的傳統,小王子也有可能沿襲祖父查爾斯
            王子名字,中間取名為查爾斯(Charles),或是跟其外公,亦即凱特王妃的父親名為邁克
            (Michael)。 法蘭西斯(Francis)則曾經出現在媽媽凱特的家族中,她的父親與祖父名字中
            都有這個字。而法蘭西絲 (Frances)則是曾曾祖母的名字,同時也是威廉王子母親的
            中間名。 據悉,小王子的名字在公告前通常會先告知英國女王以示尊重,但她一般不會更改。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1374595200
    assert parsed_news.reporter == '林南'
    assert parsed_news.title == '英小王子醫院前現身 威廉:長的像凱特'
    assert parsed_news.url_pattern == '13-7-24-3924107'
