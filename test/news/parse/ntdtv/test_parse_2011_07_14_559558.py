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
    url = r'https://www.ntdtv.com/b5/2011/07/14/a559558.html'
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
            谷歌(Google)在YouTube推出台灣第一部原生互動式偶像劇「搜尋語愛情」,讓網友透過
            互動式劇情選單加上行動搜尋,可不斷為主角重新選擇人生,有8種不同結局。 「搜尋語
            愛情」是Google台灣行銷團隊親自操刀製作的互動式影片,由知名人氣網路作家九把刀編劇
            ,新生代演員王傳一、賴雅妍和陳妍希擔任男女主角,劇情輕鬆詼諧,也融入不少Google語音
            搜尋橋段。 谷歌表示,影片透過YouTube小工具和特效等先進網頁技術,讓網友自行選擇
            劇情發展,並決定男女主角愛情結局;劇情發展超過20個選項,可製造出 8種充滿驚喜的
            結局。 「搜尋語愛情」不僅凸顯YouTube平台的互動特色,更完整體現Google行動應用
            服務優點,強調行動搜尋、語音搜尋、Google地圖、Google翻譯以及語音簡訊等Google
            行動服務,為日常生活帶來的便利性。另外,「搜尋語愛情」影片可選擇英文、日文和
            韓文字幕,讓更多地區網友一同欣賞。 谷歌表示,「搜尋語愛情」3支預告片在YouTube
            上線一週以來,已超過30萬瀏覽次數,劇中三角戀愛習題如何左右男主角命運,讓網友高度
            期待。 「搜尋語愛情」讓網友可透過互動式選單決定結局
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1310572800
    assert parsed_news.reporter is None
    assert parsed_news.title == '谷歌互動偶像劇 8種大結局'
    assert parsed_news.url_pattern == '2011-07-14-559558'
