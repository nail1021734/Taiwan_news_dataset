import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.ntdtv
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/28/a638631.html'
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
            朝鮮領導人金正日17日因心肌梗塞猝逝,享年69歲,喪禮今天舉行。金正日辭世後,朝鮮政權
            三代世襲,由金正日3子金正恩接班,朝鮮進入新時代。 關於朝鮮的重要資訊如下: 地理:
            位於朝鮮半島北半部,接壤韓國、中國和俄羅斯。 面積:12萬2762平方公里,約等於美國
            密西西比州。 人口:2400萬。 首都:平壤。 宗教:佛教、基督教。根據美國國務院,朝鮮
            政府嚴格限制宗教自由。 歷史:朝鮮半島在1910年至1945年間遭日本殖民,第二次世界大戰
            戰後一分為二,分別落入美國和蘇聯的勢力範圍。金日成1948年建立奉行共產主義的
            朝鮮。 金日成於1950年入侵韓國,引爆3年韓戰。美國率領的聯合國部隊挺韓國,中國則
            支持朝鮮。戰事最終以停火收場,但南朝鮮戰爭在技術上從未結束。 金日成仗著冷血鎮壓
            異己培養出極端的個人崇拜。他追求核武導致與美國間的緊繃態勢升高,美國差一點在1994年
            攻打朝鮮。 朝鮮和美國之後簽署解除核武協議,已於2002年屆滿失效。 1994年金日成死後,
            由兒子金正日接掌政權,他繼續發展核武和飛彈。2005年六方會談陷入緊張,2006年朝鮮
            就上演首次核子試爆。 朝鮮在2009年4月退出六方會談、5月第二度試爆,同時試射飛彈,
            招致聯合國升高制裁。 金正日2008年8月中風後,去年9月公開欽定幼子金正恩為
            接班人。但毫無經驗、年方20多歲的金正恩繼任之路,仍籠罩不確定性。 經濟:農、礦、
            製造業,國家主導型經濟。 1990年代中期的饑荒奪走數十萬條人命後,朝鮮至今仍不斷為
            嚴重糧食短缺所苦,外援卻因政治緊繃而減少。朝鮮受到美國和聯合國多重制裁。 國內
            生產毛額(GDP):280億美元。根據2009年美國「中央情報局世界概況」
            (CIA World Factbook),其人均GDP為1800美元。 貨幣:朝鮮元。 軍事:約120萬軍力。
            多數估計顯示朝鮮擁有足夠製成6至7顆核彈的鈽原料,但不清楚是否有能力製造飛彈核子
            彈頭。 韓國國防部表示,朝鮮擁有至少1000顆各式飛彈,有些射程超過3000公里。朝鮮
            試射過3顆跨洲的大浦洞飛彈(Taepodong),化武庫存則在2500噸至5000噸之間。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325001600
    assert parsed_news.reporter is None
    assert parsed_news.title == '朝鮮國情簡介'
    assert parsed_news.url_pattern == '2011-12-28-638631'
