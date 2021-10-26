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
    url = r'https://www.ntdtv.com/b5/2011/12/19/a633545.html'
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
            英國倫敦林國榮創意科技大學(LIMKOKWING UNIVERSITY OF CREATIVE TECHNOLOGY)
            是一所全球性的國際大學,校區座落在倫敦市中心的梅費爾(MAYFAIR)。12月9日,該大學
            舉行了一年一度的年終學生作品展。 倫敦林國榮大學成立於2007年10月,它的校區位於倫敦
            的市中心,比鄰著名的白金漢宮與海德公園。這所大學創辦於馬來西亞,特色是以科技創新為
            目標,但有同時保持了對亞洲傳統文化的包容。這從大學的環境風格設計中,就可見創辦者的
            用心,無處不在凸顯佛家在馬來西亞傳統文化中的影響力。 這裡的大學副校長塞德里克.貝爾
            (Prof.Cedric Bell)介紹了倫敦校區的情況:「英國倫敦林國榮創意科技大學已經有25年
            的歷史了,在這期間大學的成長非常迅速,我們有3萬名學生,遍佈3大洲8個國家,11個校區。
            吸納了來自140個國家的學生。這次一年一度的作品展,包含多個學科和領域,從建筑
            環境, 創意多媒體到服裝設計,這些都體現出學生們在專業技能的應用上可以充分發揮與
            表現。 這裡的學生大多數都是國際學生,麗薩是來自馬來西亞留學生:「在這裡學習的最大
            好處是,我可以走出校園,我認識一些行業,因為我們的項目都是為真正的客戶而做,我們為
            他們做廣告和做類似的事情。」倫敦對學生來說是最具吸引力的世界中心之一,這裡有好多
            理由:倫敦是一個非常國際化的城市,倫敦校區有一系列的管理制度,我們對教學的質量
            保證上,始終列為最優先的主導地位。 當晚大學還就有著傑出成績的學生,進行了頒獎表彰
            儀式。這些學生都是在各自的專業裡針對當下市場的需求,做出自己獨特的設計作品。這對
            他們能在畢業後,迅速和需要人才的僱主們取得信任,顯得尤為重要。倫敦林國榮大學沿襲了
            英國大學的招生傳統,一年裡有兩次入學時間分別在二月和九月。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324224000
    assert parsed_news.reporter == '文沁,孫衛英國倫敦'
    assert parsed_news.title == '英倫敦林國榮大學年度學生作品展'
    assert parsed_news.url_pattern == '2011-12-19-633545'
