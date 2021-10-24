r"""Positive case."""

import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201812300004.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            中國國家主席習近平29日應約與美國總統川普通電話,兩國元首除互致新年問候,還表示
            ,依阿根廷重要共識進行的協商正取得積極進展,盼能達成對兩國和世界人民
            都有利的成果。 新華社29日深夜發布報導稱,國家主席習近平29日「應約」與美國總統川普
            通電話。川普向習近平和中國人民致以新年的問候和祝願,並指出,美中關係很重要,
            全世界高度關注,他珍視與習近平的良好關係。 川普表示,很高興兩國工作團隊正努力
            落實自己與習近平在阿根廷會晤達成的重要共識。有關對話協商正取得積極進展,
            希望能達成對美中兩國人民和世界各國人民都有利的成果。 報導稱,習近平
            也向川普和美國人民致以新年祝福,並指出,他和川普都贊同推動中美關係
            穩定向前發展。「當前,中美兩國關係正處於一個重要階段。」 習近平表示,本月初,
            與川普在阿根廷舉行成功會晤,達成重要共識。這段時間以來,兩國工作團隊正在積極推進
            落實工作。希望雙方團隊相向而行,抓緊工作,爭取盡早達成既互利雙贏、又對世界有利的
            協議。 習近平還強調,明年是中美建交40週年。中方高度重視中美關係發展,讚賞美方
            願發展合作和建設性的中美關係,願與美方一道,總結40年中美關係發展的經驗,
            加強經貿、兩軍、執法、禁毒、地方、人文等交流合作。保持在重大國際和地區問題上
            的溝通與協調,相互尊重彼此重要利益,推進以協調、合作、穩定為基調的中美關係,
            讓兩國關係發展更好造福兩國人民和各國人民。 報導稱,中美兩國元首還就朝鮮半島形勢等
            共同關心的國際和地區問題交換看法。習近平重申,中方鼓勵和支持北韓與美國雙方
            繼續開展對話並取得積極成果。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1546099200
    assert parsed_news.reporter == '林克倫北京'
    assert parsed_news.title == '川習通電盼美中穩定發展 盡早達互利雙贏協議'
    assert parsed_news.url_pattern == '201812300004'
