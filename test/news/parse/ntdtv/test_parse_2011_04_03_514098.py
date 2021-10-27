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
    url = r'https://www.ntdtv.com/b5/2011/04/03/a514098.html'
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
            4月3日(週日)上午11點,澳洲紐省新任省長奧法雷爾(Barry O』Farrell)領導其組建的
            首任內閣,在悉尼政府大樓宣誓就職。內閣中的3名新成員引起了公眾的關注,他們和新調整的
            部門職能一起,向人們展示了新省長的改革決心。 據澳新社報導,參加週日宣誓的共有22名
            內閣廳長,其中包括三名非前影子內閣成員。他們是環境和遺產廳長派克(Robyn Parker),
            體育和娛樂廳長安妮斯麗(Graham Annesley)以及公民、社區和原著民事務廳長
            多米尼羅(Victor Dominello)。派克和安妮斯麗分別來自梅特蘭(Maitland)區和
            米蘭達(Miranda)區,兩人都是首次當選議會議員。多米尼羅來自賴德(Ryde)區,曾在
            立法委員會任職,但沒從未進入過影子內閣。 奧法雷爾在宣誓儀式前發佈的一份聲明中說:
            「三名新任部長都贏得了在內閣中的職位,他們的加入確保我們團隊有了新的人才。」奧法雷爾
            還證實了對政府職能進行的改革,包括引進大部制,合併原有部門職能成立8個大部門;增設
            金融與服務廳、精神健康和健康生活方式廳等新部門,以及對人員職位的相應調整。 按照
            調整後的分工,副省長斯通納(Andrew Stoner)將負責貿易投資、邊遠地區基礎設施
            和服務事務,之前他在反對黨影子內閣中負責的公路事務將由民族黨(Nationals)議員
            蓋伊(Duncan Gay)接管;負責警察事務的加拉徹(Mike Gallacher)將擔任新組建的緊急
            服務廳廳長,原來的警察廳職能將併入緊急服務廳之內。原影子健康廳長斯金納
            (Jillian Skinner)和影子交通事務廳長貝雷吉克萊恩(Gladys Berejiklian)將分別
            繼續負責健康和交通事務。 新內閣還增加了邊遠地區事務管理職能,5名新任命的邊遠地
            區廳長將分別負責紐省西部、北海岸、中部海岸、獵人區和伊拉瓦拉邊遠地區事務。新內閣中
            的民族黨代表預計將從之前影子內閣中的8名減少至7名。
            '''
        ),
    )
    assert parsed_news.category == '海外華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1301760000
    assert parsed_news.reporter is None
    assert parsed_news.title == '紐省新內閣就職 新人新部門新氣象'
    assert parsed_news.url_pattern == '2011-04-03-514098'
