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
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640245.html'
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
            2012年新年第一天,日本關東外海發生規模7.0強震,所幸震源深度約350公里,沒有發生
            海嘯,也沒有人員傷亡報導傳出。 地震發生在日本當地時間下午2點27分,架在東京大樓的
            攝影機正好錄下地震來襲時震盪的情景,地震當時東京震度4級。 地震發生後,日本北部的
            新幹線列車一度停運數分鐘,但很快恢復運行。 這起地震震中位於日本南部伊豆群島
            海域,距海面349公里,屬於深層地震。儘管如此,東京,福島及周邊都測到強烈震感,所幸
            沒有人員傷亡和財産損壞傳出。東京電力公司的發言人也表示,福島第一核電站沒有出現異常。
            '''
        ),
    )
    assert parsed_news.category == '天災人禍,各國地震,日本地震'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1325347200
    assert parsed_news.reporter == '王晨光'
    assert parsed_news.title == '日本發生7.0深層地震 未傳傷亡'
    assert parsed_news.url_pattern == '2012-01-01-640245'
