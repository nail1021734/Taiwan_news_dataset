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
    url = r'https://star.ettoday.net/news/1200168'
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
            小孩用藥一直是許多家長關心議題,其實對於幼兒用藥有以下「5點建議」: 1.6歲以下以藥
            水為主 幼兒不太會吞嚥,如果是在藥局磨粉又會擔心有污染及容易潮解進而影響藥效,因此
            ,如果可以,買磨藥研缽回去分包,但這真的很麻煩,我試過,所以還是建議還是以藥水為主,
            藥水的劑量也可以比較精準,對於幼兒相對安全。 2. 藥粉以冷水稀釋 很多家長會認為小
            孩感冒就是要喝熱水,因此用熱水稀釋藥粉,許多藥會受到熱破壞,例如益生菌、維生素和一
            些消化類的藥品,如果碰到熱水會破壞活性或是失效。 3.餵藥以滴管餵食 看過一些家長為
            了讓小孩吃藥會趁小孩大哭時,順勢把藥水倒到小孩口中,這是很危險動作,容易讓小孩嗆傷
            ,甚至可能引發吸入性肺炎,因此,建議用滴管或餵食器由嘴角慢慢滴入。 4.拿藥時多詢問
            藥品使用方式 有些小孩如果醫師診斷必須使用抗生素時,得再吃1個週期,以避免有抗藥性
            發生,因此,建議家長在拿藥時多詢問一下,醫師如果告知需要回診,不要因為小孩沒症狀而
            不回診。 5.藥不要放冰箱 很多人會以為藥就要放冰箱保存,最常見是藥水,但是其實冰箱
            溫度低、濕氣重,藥水有效成份可能沉澱結晶而失去效果,另外,眼藥水放冰箱,更可能濕氣
            重導致變質而有反效果,建議如果這次沒用完直接丟棄即可。 小孩用藥要安心,建議領藥時
            多詢問一下藥師或是到鄰近社區藥局詢問,這樣才可以讓自己小寶貝服用的安全又
            安心。 段方琪藥師,英國Bradford University碩士,曾任台大醫院護理師、長庚醫院
            藥師、榮民製藥經理、連鎖藥妝藥師。
            '''
        ),
    )
    assert parsed_news.category == '健康'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530151200
    assert parsed_news.reporter == '段方琪'
    assert parsed_news.title == '把藥放冰箱、配熱水吃都NG! 用藥「5建議」爸媽快筆記'
    assert parsed_news.url_pattern == '1200168'
