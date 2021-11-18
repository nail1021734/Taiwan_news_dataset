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
    url = r'https://star.ettoday.net/news/4556'
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
            MLB全明星台灣大賽1日開打,大聯盟明星隊在先發投手古斯利(Jeremy Guthrie)和
            葛蘭德森(Curtis Granderson)滿貫砲聯手發揮,以及雨神幫忙下,6局上打完即以7比0
            完封中華隊,搶下頭彩。但賽後總教練波奇(Bruce Bochy)和兩大功臣仍稱讚中華隊表現
            ,認為這場交手相當精彩。 雖然因雨未能打完6局,但波奇仍隊比賽給予高度評價,特別是
            古斯利在天候不佳情況下3局都未失分,表現出色。波奇說:「古斯利投得很棒,關鍵時刻也以
            雙殺化解危機,加上葛蘭德森的滿貫全壘打,大家都表現很不錯。」 而古斯利則表示很開心
            能在第1場先發,並對球迷的熱情印象深刻。另外他也稱讚中華隊打者纏鬥能力相當不錯
            ,也都能將球打進場內,只可惜攻勢未連貫,沒能得到分數。 而砲轟陽耀勳的葛蘭德森,談到
            3局的打席時說:「當時我沒有特別想揮全壘打,那次投打對決洋的配球甚至讓我有些迷惑
            ,最後是逐球調整,最後抓到1顆滑球揮擊。」 此外葛蘭德森也不忘稱讚古斯利表現
            ,葛蘭德森說:「古斯利今天投的很好,在困難(下雨)情況下還能壓制對手,相當不簡單。」
            大聯盟明星隊7分分別由葛蘭德森(4分)、波尼法西歐(Emilio Bonifacio)(2分)和
            摩斯(Michael Morse)(1分)打下。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1320156960
    assert parsed_news.reporter == "黃樺君"
    assert parsed_news.title == '剋中華奪首勝 波奇:投、打都很棒!'
    assert parsed_news.url_pattern == '4556'
