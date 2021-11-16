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
    url = r'https://star.ettoday.net/news/2053474'
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
            台灣最強歌唱選秀節目《聲林之王》即將重磅回歸,在網友的殷殷期盼下,台灣實體海選也
            終於到來了!《聲林3》本周六(14日)在遠百信義A13舉行海選,ETtoday從上午九點開始
            直播,帶你直擊現場戰況。當天請鎖定ETtoday新聞雲、星光雲、App、粉絲團、聲林之王
            Youtube頻道等,搶先關注這季的優秀選手! 聲林3海選直播看這裡 受到各界高度期待的
            《聲林之王3》即將重磅登場,8月14日首場海選率先於台北遠百信義A13開跑,當天還有邀請
            到台灣歌壇界資深音樂製作人陳子鴻老師、知名廣播主持人暨創作歌手左光平,以及才女歌手
            呂薔到場,要用最挑剔的耳朵選出令人驚豔的歌喉! 當天除了開放現場限量報名試唱,
            還有網路複試的評選,究竟會出現哪些神人級的歌手?歡迎鎖定ETtoday海選現場試唱實況,
            尋找令人感動的好聲音。 也歡迎各位有實力、懷有舞台夢的好朋友們,勇敢站出來實現你的
            歌唱夢想!8/14(六)遠百信義A13上午8:00前記得來排隊報名試唱喔,我們不見不散!
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1628674560
    assert parsed_news.reporter is None
    assert parsed_news.title == '民間高手大飆唱 《聲林3》台北實體海選14日上午9點Live直擊'
    assert parsed_news.url_pattern == '2053474'
