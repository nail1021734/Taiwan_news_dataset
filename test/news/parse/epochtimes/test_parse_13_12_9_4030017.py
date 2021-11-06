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
    url = r'https://www.epochtimes.com/b5/13/12/9/n4030017.htm'
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
            泰國反政府示威活動已持續1個多月,以下是這段期間的大事回顧。 10月31日:民眾反對政
            府特赦法案發起示威,批評人士表示,特赦案目的是要替因貪汙遭定罪的前總理戴克辛(亦譯
            :他信)(Thaksin Shinawatra)漂白,讓他能夠結束自我流亡,返回泰國。 戴克辛是泰國總理
            盈拉(亦譯:英祿)(Yingluck Shinawatra)胞兄。 11月1日:執政黨主導的眾議院表決通過
            特赦法案。 11月11日:街頭示威越演越烈,參議院以壓倒性票數駁回特赦法案。但示威者
            並未就此罷手,反倒矢言加強集會規模,訴求推翻總理盈拉,終結戴克辛政權。 11月20日:
            憲法法院(Constitutional Court)駁回執政為泰黨的參議院產生辦法修正案,但沒有裁決解
            散執政黨。 11月24日:當局表示,多達18萬名反對派示威人士響應在曼谷民主紀念碑
            (Democracy Monument)上演的大型集會活動,對政府施加更多壓力。另有約5萬名力挺
            政府的「紅杉軍」,在市郊1個場地發起敵對示威活動。 11月25日:數以萬計反政府人士
            闖入政府建築物,占領財政部。政府實施特別安全法,賦予首都曼谷員警更大權限。 11月
            26日:國會開始就盈拉的不信任動議展開辯論。示威者包圍數個部會機關,揚言癱瘓政府。
            警方以策劃占領財務部為由,對煽動示威的蘇德(Suthep Thaugsuban)發出
            逮捕令。 11月27日;示威活動在泰國各地蔓延,尤以在野民主黨(Democrat Party)
            南部大本營的示威規模最大。示威者由蘇德帶領,在曼谷各處遊行,並占領曼谷市郊的政府
            建築物為示威基地。 11月28日:國會執政黨議員駁回盈拉的不信任案。蘇德則拒絕盈拉
            以會談終結危機的請求。 11月29日:和平示威者闖入陸軍總部,在裡頭停留2個小時,敦促
            軍方加入他們的行列;但陸軍總司令帕拉育(Prayut Chan-O-Cha)表示,軍方不會倒向
            任何一方。另外有數千名示威者在執政為泰黨(Puea Thai)總部外頭集會。 11月
            30日:示威者闖入兩大國營電信公司的辦公室,並一度試圖闖入政府總部。1輛搭載「紅杉軍」
            的巴士遭反對派示威者攻擊,這是示威活動首次發生暴力事件,街頭衝突造成數人死亡,
            數十人受傷。 12月1日:示威者設法越過拒馬,闖入戒備森嚴的總理府
            (Government House)及曼谷市警察總部,警方使用強力水柱及催淚瓦斯回敬。 12月
            3日:發生接連數日的街頭衝突後,政府命令員警避免進一步與示威者衝突,泰國國王蒲美蓬
            大壽前,緊張局勢緩和。 12月5日:泰王蒲美蓬(Bhumibol Adulyadej)在86歲大壽演說中呼
            籲全國團結,維持國家「穩定」。 12月8日:泰國國會在野黨議員集體請辭。 12月9日:總
            理盈拉宣布解散國會,提前舉行大選,但示威並未平息,約10萬人走上曼谷街頭。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386518400
    assert parsed_news.reporter is None
    assert parsed_news.title == '泰國反政府示威大事記'
    assert parsed_news.url_pattern == '13-12-9-4030017'
