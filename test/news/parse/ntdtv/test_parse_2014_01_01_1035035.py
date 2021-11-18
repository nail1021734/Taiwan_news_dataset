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
    url = r'https://www.ntdtv.com/b5/2014/01/01/a1035035.html'
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
            南蘇丹衝突雙方定於星期三在鄰國埃塞俄比亞開始舉行談判,爭取結束數星期來導致1千多人
            死亡的暴力衝突。 埃塞俄比亞總理德薩萊尼將負責斡旋南蘇丹總統基爾的代表與叛軍領導
            人馬查爾的代表之間的談判。 屬於丁卡族的基爾指責屬於努爾族的馬查爾企圖發動政變,
            就此引發流血衝突。南蘇丹是世界上最新成立的國家。 美國對南蘇丹雙方舉行談判表示
            歡迎,並再次呼籲雙方立即停止戰鬥。聯合國安理會發言人海登說,美國將拒絕支持試圖奪取
            政權的人,並認為各方領導人應為其軍隊的所作所為承擔責任。 聯合國說,南蘇丹的暴力
            導致成千上萬平民流離失所。 星期二,南蘇丹主要城市博爾繼續發生戰鬥。目前不清楚博爾
            的控制權掌握在哪一方手中。
            '''
        ),
    )
    assert parsed_news.category == '國際,社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter is None
    assert parsed_news.title == '南蘇丹政府將與叛軍舉行停戰談判'
    assert parsed_news.url_pattern == '2014-01-01-1035035'
