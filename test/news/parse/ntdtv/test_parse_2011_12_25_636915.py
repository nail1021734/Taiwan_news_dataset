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
    url = r'https://www.ntdtv.com/b5/2011/12/25/a636915.html'
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
            巴黎布蘭利河岸博物館現正展出毛利文化特展,邀小宛然戲團演出毛利神話故事。戲班班主
            班任旅運用的皮影戲、布袋戲技巧,全部師承自台灣。 已故布袋戲師傅李天祿法國弟子
            班任旅(Jean-LucPenso)率小宛然26日起在布蘭利河岸(Quai Branly)博物館演出
            10場毛利神話故事。班任旅為本戲設計新戲偶,綵樓上輪番上演皮影戲和布袋戲,又有真人
            現身演出。 班任旅的台灣太太廖琳妮為本戲作曲,旅法打擊演奏家楊怡萍現場演奏。楊怡萍
            在大鼓、鈸、和各式小型打擊樂器間,製造航海、驚濤駭浪等環境效果,以及各種偶戲人物
            不同感情,緊抓住觀眾的情緒。 這場偶戲表演以法文說毛利神話故事,敘述新西蘭的誕生,
            是毛利文化特展的系列活動之一。班任旅在戲中說、唱,還刻意穿插一曲台灣戲曲曲調。 小
            宛然在布蘭利河岸博物館的毛利神話一戲自26日至30日每天演出2場。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324742400
    assert parsed_news.reporter is None
    assert parsed_news.title == '台布袋戲弟子巴黎博物館演出'
    assert parsed_news.url_pattern == '2011-12-25-636915'
