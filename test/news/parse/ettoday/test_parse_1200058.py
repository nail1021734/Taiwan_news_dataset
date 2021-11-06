import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/1200058'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            日本Cygames旗下卡牌對戰遊戲《闇影詩章 Shadowverse》官方賽事
            《Shadowverse Taiwan Open》2018夏季總決賽在上週六(23)劃下完美句點,最後由
            海選殺出重圍、並拿下8強例行賽A組冠軍的「sasamumu」擊敗春季賽王者「NineVoice」
            抱走冠軍及16萬元獎金。 「sasamumu」在第1場4強戰就展現出旺盛的求勝意志,接連以
            精靈、亞瑟皇及龍族套牌連拿3局,最後一場對決雖然處於劣勢,但連續使用中立卡片
            「伊斯拉菲爾」及「癲狂暴龍」掃光對手場上的從者,最後再幸運拿到第2張可以突破對方
            「守護」的「巨鐮龍騎士」,順利晉級冠亞戰。 另一場4強對決由彼此皆為官方賽事常客的
            「NineVoice」對上「レッドデス」,果不其然雙方你來我往打滿5場比賽,最後由
            「NineVoice」以3:2驚險晉級最後的冠亞戰。 「レッドデス」選手雖然最後以1局之差
            無法晉級,但在使用復仇者套牌對上「NineVoice」於日本RAGE西日本預賽中大顯神威的
            言靈巫師套牌時,1回合解光對手3張強勁的傳說卡「宙斯」與「伊斯拉菲爾」,讓
            「NineVoice」也忍不住鼓掌致意,也讓主播、賽評及全場觀眾歡聲雷動。 最後的冠亞
            之爭,「sasamumu」選手面對春季賽王者「NineVoice」毫不畏懼,先以精靈職業牌組拿下
            首局,雖然「NineVoice」隨後使用龍族職業套牌將戰局一度扳成在1:1平手,但
            「sasamumu」在第三局使用原本應該是中後期型的皇家護衛套牌,卻硬是在第5回合就成功
            帶走比賽,拿下關鍵的1勝。自此氣勢完全轉向「sasamumu」,最後以4:1成為新任《STO》
            王者。 賽後官方也宣佈《STO》秋季賽將緊接著展開報名,賽事官方網站也已公布海選及例
            行賽日期。這次秋季賽比照春&夏季賽,總獎金為30萬台幣,若能晉級4強不但能參加總決賽,
            還能出賽預計在接近年底舉辦的《2018 STO總冠軍賽》,挑戰冠軍獎金100萬美金(折合約
            3,000萬元台幣)的「World Grand Prix」世界大賽參賽資格。
            '''
        ),
    )
    assert parsed_news.category == '遊戲'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530060120
    assert parsed_news.reporter == '樓菀玲'
    assert parsed_news.title == '《闇影詩章》sasamumu選手奪STO大賽冠軍 獨得獎金16萬'
    assert parsed_news.url_pattern == '1200058'
