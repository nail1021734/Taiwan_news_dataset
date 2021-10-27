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
    url = r'https://www.ntdtv.com/b5/2011/12/21/a635019.html'
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
            12月21日聯播簡訊,下面請看一組國際簡訊。 1、日決定向美採購42架F35隱形戰機 日本
            近日決定,將向美國採購42架F35隱形戰鬥機作為未來的戰備主力。日本防衛大臣
            福田康夫川(Yasuo Ichikawa)表示,這項決定是出於重要的國家安全戰略考慮。有專家
            認為,日本採購美國戰機反映出東京希望在中共軍事威脅以及其他種種區域安全的不確定
            因素中,加強美日間的合作關係。 2、阿盟擬派觀察員 敘衝突繼續 星期二,阿盟宣佈
            將可能在本月底前派遣觀察員進入敘利亞,以監督當局實施和平協議的狀況。阿盟秘書長
            阿拉比表示,觀察員必須有權自由活動,自由會見民眾以及考察監獄和醫院。據悉
            阿盟助理秘書長星期四將率領一個高級代表團從開羅搭機訪問敘利亞,為最終派遣觀察員到
            敘利亞各地鋪路。 3、英首相卡梅倫突訪阿富汗慰問英軍 星期二,英國首相卡梅倫突然前往
            位於阿富汗坎大哈的北約基地,在聖誕節前夕慰問駐紮在那裏的英軍部隊。卡梅倫在演說中
            表示,英國士兵10年來的努力沒有白費,他對阿富汗的局勢充滿信心,並稱英軍將在2014年底
            之前徹底結束在阿富汗的戰鬥任務。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324396800
    assert parsed_news.reporter == '陳新梅,白蘭,韋青一'
    assert parsed_news.title == '12月21日聯播簡訊'
    assert parsed_news.url_pattern == '2011-12-21-635019'
