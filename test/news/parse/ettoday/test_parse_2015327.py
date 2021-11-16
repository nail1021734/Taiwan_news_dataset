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
    url = r'https://star.ettoday.net/news/2015327'
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
            西濱台61線快速道路清晨4點50分發生重大車禍事故!陳男駕駛的化學曳引槽車疑未注意
            車前狀況,行經彰化芳苑南下路段188公里處追撞停在路肩正待道路救援的故障大貨車,
            導致槽車車頭斷裂,陳男眼角創傷、手腳擦挫傷送醫。不料此時,在前方184公里執行巡邏的
            警車,也被後方的自小客追撞,造成警車嚴重毀損。 彰化消防局清晨4時50分據報後,出動
            漢寶及芳苑分隊、2輛消防車、2輛救護車,消防人員7人,到達現場為槽車與大貨車車禍,現場
            無起火燃燒及冒煙情況,無人員受困,運輸槽車為空車無載運物品,槽車駕駛頭部紅腫、右手
            撕裂傷,由芳苑91於北上端後送傷者至彰濱秀傳醫院,另大貨車司機無受傷。 據警方
            初步調查,陳男的槽車撞到停在路肩的貨車,導致貨車左後方車體毀損、而槽車則是車體斷成
            2截,車頭斷裂,占用整個南下車道,陳男自行脫困輕傷送醫。 警方派出鹿港海埔派出所
            、芳苑草湖派出所警車前往管制交通,員警站在184公里處引車輛下漢寶交流道,警車被一輛
            自小客車從後方追撞,其中草港所警車後方變形,玻璃全部碎裂,所幸員警平安無事。至於
            整起交通事故於上午8時排除,確切肇事的原因,正有待警方進一步調查。
            '''
        ),
    )
    assert parsed_news.category == '社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1624587060
    assert parsed_news.reporter == '唐詠絮'
    assert parsed_news.title == '西濱彰化段槽車撞大貨車「斷頭」 警車馳援也遭殃「車尾消失」'
    assert parsed_news.url_pattern == '2015327'
