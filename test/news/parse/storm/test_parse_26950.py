import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/26950?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            車臣共和國 (Republic of Chechnya)現隸屬於俄羅斯聯邦,地理位置位於俄羅斯西南部
            的高加索山脈北側,面積約1萬6000平方公里,首府為葛洛茲尼(Grozny),車臣人大多信奉
            伊斯蘭教,屬遜尼教派(the Sunnis)。 車臣人於7世紀開始居住於高加索山區,主要從事
            游牧,13世紀開始受到蒙古人的侵襲,直到金帳汗國於16世紀解體後,車臣人才逐漸從山區
            向平原遷徙。18世紀初期,車臣地區開始成為當時波斯、鄂圖曼土耳其與俄羅斯3個帝國互相
            爭奪的對象,最後,車臣於1859年被俄羅斯帝國併入版圖。 1922年,蘇聯在當地成立車臣
            自治州,1934年,車臣與殷古索(Ingush)自治州進行合併,合稱「車臣殷古索蘇維埃社會主義
            自治共和國(Checheno-Ingush A.S.S.R.)。1938年,蘇聯要求車臣人放棄原本使用的
            阿拉伯字母,改學習俄語字母。1944年,蘇聯領導人史達林(Josef Stalin)以車臣人曾
            幫助過納粹德國為由,強行把近39萬的車臣人流放至中亞和西伯利亞。直到1957年,
            赫魯雪夫(Nikita Khrushchev)才同意車臣人重回原居住地,並恢復車臣殷古索自治
            共和國的建制,仍歸俄羅斯聯邦管轄。 由上述歷史可以得知,車臣原不屬於俄羅斯,兩者的
            語言、文化與宗教也都不相同,車臣在被俄羅斯強行併吞後,當地居民不僅被迫學習俄語,
            二戰時期流離失所的結果是連原居住地都被俄羅斯人所佔,車臣政府中的重要職務也大多由
            俄羅斯人擔任,造成車臣當地的獨立意願愈趨高漲,而車臣與蘇聯的衝突在蘇聯解體後更加地
            激化與升高,最終以戰爭的型態爆發。 1991年12月,蘇維埃社會主義共和國聯邦宣布解散,
            原本隸屬於聯邦內的許多共和國紛紛宣佈獨立。在此之前,出身於車臣的前蘇聯空軍少將
            杜達耶夫(Dzhokhar Dudayev)於該年9月,先以武力控制了位於葛洛茲尼的許多重要政府
            機構大樓,接著在1個月內舉行了總統與議會的選舉,當選總統的杜達耶夫隨即對外宣佈成立
            車臣共和國(Chechen Republic of Ichkeria),並同時組織車臣國民軍。而在蘇聯
            解散後,車臣既不願意簽署聯邦條約,也表示不會參加1993年的俄羅斯議會選舉,時任俄羅斯
            總統的葉爾欽(Boris Yeltsin)於1994年12月,下令6萬名俄羅斯軍隊進駐車臣,雙方
            隨即展開戰鬥。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1391196420
    assert parsed_news.reporter == '簡嘉宏'
    assert parsed_news.title == '《索契冬奧專題》車臣共和國獨立史'
    assert parsed_news.url_pattern == '26950'
