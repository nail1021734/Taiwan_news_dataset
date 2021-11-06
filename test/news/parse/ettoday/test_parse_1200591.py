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
    url = r'https://star.ettoday.net/news/1200591'
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
            BMW 集團擁有 MINI 及 Rolls-Royce 2 個英國汽車品牌, 也在英國設立引
            擎生產線,不過受到英國脫離歐盟的影響, BMW 關務經理 Stephan Freismuth 表示,未來若
            進口成本增加,使供應鏈不易進入英國,導致生產時程延遲,將難以維持工廠運作,走向關廠
            一途。 根據 Stephan Freismuth 的說法, BMW 希望維持英國工廠的營運,也正在制定針對
            脫歐的應變計畫,不過英國脫離歐盟關稅相關協定的影響若
            拖延 BMW 目前 Just-in-Time 製造模式,使零件與貨品無法自由流通,造成零件無法在
            預期時間內送達工廠,將嚴重影響工廠營運的可靠性,畢竟 BMW 集團在英國工廠使用的零件
            有近 90% 來自歐陸。 BMW 在英國 Swindon 、 Hams Hall 及 Oxford 等工廠
            共有 6,300 名員工,其中去年生產的 37.8 萬輛 MINI 車系,
            有 60% 來自 Oxford 廠。 BMW 認為英國脫歐後的關稅問題,因不確定性高,使
            人無法安心,對企業進行長期營運規劃形成阻力。 一名英國政府的發言人則表示,英國冀望
            能與歐洲各國進行自由且順暢的貿易往來,有信心與歐盟談妥條件良好的協議。
            '''
        ),
    )
    assert parsed_news.category == '車'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530199740
    assert parsed_news.reporter == '7car'
    assert parsed_news.title == '英國脫歐衝擊零件供應 BMW集團考慮關閉勞斯萊斯&MINI工廠'
    assert parsed_news.url_pattern == '1200591'
