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
    url = r'https://star.ettoday.net/news/2031760'
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
            台灣正加速施打新冠肺炎疫苗,不過近期也瘋傳打完莫德納變萬磁王,手臂吸得住鐵湯匙,
            引起不少施打後網友實測。但也有醫師解釋所謂的「萬磁王」情況其實和疫苗無關;另外,
            國際上也有做施打後「皮膚症狀反應」整理,其實施打莫德納之後最常見的是「新冠手臂」
            。 目前台灣已經全面開放18歲以上民眾上網做新冠肺炎意願登記,至今已累計近8百萬人,
            隨著接種率上升,接種後不良事件通報也越來越多,國際上也早有針對接種疫苗後皮膚可能會
            出現的反應做研究整理。 包括醫學期刊「刺絡針」(Lancet)和美國皮膚科醫學期刊
            (JAAD)都有蒐集英美兩國大規模施打AZ、BNT與莫德納疫苗出現皮膚反應進行整理
            。 Lancet共搜集62萬人接受2劑BNT或1劑AZ的安全及有效性報告,發現施打後常見的
            皮膚局部副作用,包括紅/腫/熱/痛/癢/瘀青/壓痛/腋下淋巴腺腫等,當然接種不同疫苗,
            發生率也有所不同。另外,JAAD發表的期刊,則是針對414位施打mRNA疫苗後皮膚出現紅疹
            的案例分析,也分析出最常見的5種紅疹。 值得注意的是,其實莫德納最常見的是新冠手臂
            。書田診所皮膚科主任醫師蔡長祐先前提醒,倘若注射疫苗7到8天手臂腫起來,且有熱痛癢
            反應,就是「延遲型大型局部反應」,就叫做新冠手臂,而新冠手臂是mRNA疫苗特有的皮膚
            反應,大部分的人會在4天左右消退。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1626566460
    assert parsed_news.reporter == '趙于婷'
    assert parsed_news.title == '不會變萬磁王!接種後皮膚症狀總整理 莫德納最常見「新冠手臂」'
    assert parsed_news.url_pattern == '2031760'
