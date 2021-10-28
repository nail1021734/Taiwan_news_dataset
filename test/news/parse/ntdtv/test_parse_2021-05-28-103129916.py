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
    url = r'https://www.ntdtv.com/b5/2021/05/28/a103129916.html'
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
            27號當天,日本與歐盟,舉行了視頻會議,並發布聯合聲明,首次提到「台灣海峽和平穩定的
            重要性」。外界認為,這是為下個月G7國領導人峰會,討論台灣議題鋪路。 日本首相菅義偉
            27號與歐洲理事會主席米歇爾、歐盟執委會主席馮德萊恩舉行視訊會議。 雙方發表
            聯合聲明,「強調台灣海峽和平穩定重要性,並鼓勵和平解決兩岸議題。」日本將與歐盟
            在香港、新疆等地區事務緊密合作。 日本《讀賣新聞》報導,這是歐日峰會首次提到
            台灣問題。 台灣中山大學中國與亞太區域研究所教授郭育仁:「這個其實是美國拜登總統
            他的對中政策的意志的貫徹了,穩定台海局勢或台海局勢的重要性,已經成為世界主要國家的
            共識了。所以日本跟歐洲的日歐之間的共同聲明,基本上是延續拜登政策的一貫的脈絡
            。」 美國國家安全委員會印太協調員坎貝爾近日表示,美中交往時期已宣告終結,美對華政策
            將在「新的戰略參數」下運作,「主導模式將是競爭。」 隨著中共通過《海警法》使得
            東海局勢緊張,美、日、法三國本月在東海聯合軍演,日本準備成立第三支水陸機動團,防範
            中共軍隊登島作戰。 菅義偉在這次峰會上表明,堅決反對中國(中共)改變東海和南海現狀
            的企圖。 中共駐歐盟使團發言人對此聲明,表示「強烈不滿」和「堅決反對」
            。 郭育仁:「台灣當然對他們來講是很主要的政治禁忌,之前都只做不講,今年決定把台海
            局勢把台灣直接放上檯面,所以整個戰略邏輯就有一貫性了。所以一路從東海、台海、南海
            ,然後往東南走到南太平洋往西,透過南海、到麻六甲、到印度洋
            。」 郭育仁認為,台海穩地與印太區域安全,已成世界主要國家的共識。
            '''
        ),
    )
    assert parsed_news.category == '新聞視頻,環球直擊,環球直擊新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1622131200
    assert parsed_news.reporter == "江禹嬋,林岑心,劉芳"
    assert parsed_news.title == '日歐聲明首提台海 分析:貫徹拜登對中政策'
    assert parsed_news.url_pattern == '2021-05-28-103129916'
