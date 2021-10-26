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
    url = r'https://www.ntdtv.com/b5/2011/04/12/a517548.html'
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
            4月10號 (星期日),美國神韻巡迴藝術團在倫敦的7場演出圓滿結束,素有“天下第一秀”
            之稱的神韻演出,給英國觀眾留下了深刻印象。下面請看來自英國的報導。 斯黛梅•考塔克斯
            是倫敦市合唱團成員 ,她被神韻深邃的內涵而打動。 斯黛梅•考塔克斯:“我喜歡神韻的歌曲,
            喜歡神韻傳達的理念,喜歡神韻歌詞裡的精神,和歌詞中傳達的信息。”“(信息)就是要有勇氣,
            要忠誠,要有善念,要真誠,要堅持自己的信仰。” 海倫•埃姆斯:這個演出太棒了,能夠體驗
            到失去的真正的中華文化是甚麼樣的,也學到了歷史,簡直難以想像。服飾優美,舞蹈迷人,
            我從來沒有看過中國古典舞,很精彩,真是非常美妙!我對整場演出印象非常深刻,太了不起了!
            ” 路易斯•拉科夫斯基:“我非常喜歡,並受到激勵。我喜歡所有的舞蹈,服裝和色彩,她使我
            更有興趣去了解中華文化和歷史,並能真正的去理解她,因為我目前了解的不多,真的使我受到
            激勵。” 4月10號下午,美國神韻巡迴藝術團在倫敦大劇院的七場演出圓滿落幕。神韻完美、
            精湛的演出不僅讓英國觀眾享受到最頂級的藝術饗宴,更讓他們感受到了心靈的震撼和精神
            啟迪。接下來,美國神韻巡迴藝術團將於4月12號和4月14號在荷蘭的海牙舞蹈劇院進行
            兩場演出。
            '''
        ),
    )
    assert parsed_news.category is None
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302537600
    assert parsed_news.reporter == '梁東,文正英國倫敦'
    assert parsed_news.title == '神韻英國圓滿落幕 震撼觀眾心靈'
    assert parsed_news.url_pattern == '2011-04-12-517548'
