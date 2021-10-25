import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/28/a638636.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            朝鮮故領導人金正日喪禮今天舉行,三子金正恩接班,朝鮮孤立、貧困,卻擁有數量龐大的
            部隊,以及不少火炮、化學武器與少量核子武器,成東北亞潛藏危機,令鄰國和列強
            憂心。 以下是朝鮮部隊的基本情況: 核子武器:大多數估計顯示,朝鮮擁有的鈽原料足以
            生產6到7個原子武器。目前仍不清楚朝鮮能否為它的飛彈製造核子彈頭,不過分析家認為
            技術可能接近能生產的水準。 飛彈:據韓國國防部的消息,朝鮮至少擁有各型飛彈1000枚,
            其中某些射程超過3000公里。朝鮮已試射3枚大浦洞洲際飛彈。 化學和生物武器:美國與
            盟邦軍事專家認為,若與韓國進行傳統戰爭,朝鮮並非韓國的敵手。不過專家擔心平壤會用
            化學和生物武器。 韓國國防部和其他報告表示,朝鮮擁有2500到5000噸化學武器,足以對
            韓國造成可怕的傷亡。 這些化學藥劑可用長程火炮、多管火箭發射器、彈道飛彈、飛機或
            海軍艦艇投放。 朝鮮也有生物武器計劃,不過分析家表示,不清楚朝鮮的生物武器計劃是否
            已超越研究發展階段。 據信平壤擁有炭疽熱病毒、芥子毒氣、沙林毒氣、臘腸桿菌(或
            肉毒桿菌)與光氣。 人力:朝鮮規定17歲開始服兵役,三軍部隊共計約120萬人,後備軍人
            770萬。 陸軍:朝鮮陸軍有大批重炮對準首爾。美國政府與分析家估計,武器包括約3500輛
            主戰車、560輛輕戰車、2500輛裝甲運兵車、3500門拖式火炮、4400輛自走炮、2500個
            多管火箭發射器、7500門迫擊炮以及1萬1000門防空炮。 海軍:朝鮮海軍擁有龐大
            潛艦艦隊,估計有92艘潛艦。水面艦艇則有3艘護衛艦、6艘輕武裝快艦、43艘飛彈艇、158
            艘大型巡邏艇、103艘魚雷快艇與超過334艘巡邏艇。 空軍:朝鮮空軍是為了迅速越過非
            軍事區攻擊韓國而建的,估計有80架轟炸機、541架戰鬥機和地面攻擊戰鬥機、316架運輸機、
            588架運輸直升機、24架攻擊直升機、至少1架無人飛機,而且空對空和地對空飛彈供應充足。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325001600
    assert parsed_news.reporter is None
    assert parsed_news.title == '朝鮮軍力不弱 東北亞藏危機'
    assert parsed_news.url_pattern == '2011-12-28-638636'
