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
    url = r'https://www.ntdtv.com/b5/2011/12/30/a639463.html'
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
            海洋生物學家今天發表年度報告,宣布在蘇格蘭海岸發現許多新物種,包括會發磷光的海筆
            在內。 「每日郵報」(Daily Mail)報導,學者利用多波束掃描測深儀和高清晰度攝影機
            捕捉到數種罕見、難找的物種,包括外形既像羽毛筆又像聖誕樹的海筆,是住在海底的珊瑚
            蟲群,一碰就發光。 學者在奧克尼群島(Orkney)附近水域發現了被稱為「無臉無腦魚」的
            史前蛞蝓,牠沒有眼睛也沒有臉,背上佈滿神經索。學者認為,脊椎動物和蛞蝓的共同祖先
            存在於5億5000萬年前。 此外,學者還在開斯奈斯(Caithness)諾斯角(Noss Head)附近
            找到最大的馬蚌蚌床,這些成長速度緩慢的軟體動物可以存活將近50年。 西岸附近則找到了
            非常罕見的巨大扇貝,長達48公分,為蘇格蘭海貝類之最。 學者也在阿吉爾郡(Argyll)
            找到火焰貝床,火焰貝擁有亮橘色的攝食觸手,只有西岸極少數地點才找得到。 環境部長
            羅克海(Richard Lochhead)說:「蘇格蘭周圍海域富含如此令人著迷的生物多樣性,保護
            這個脆弱的環境正是我們的責任。」
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325174400
    assert parsed_news.reporter is None
    assert parsed_news.title == '蘇格蘭海底 閃亮耶誕樹現蹤'
    assert parsed_news.url_pattern == '2011-12-30-639463'
