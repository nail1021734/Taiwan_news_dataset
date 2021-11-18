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
    url = r'https://www.ntdtv.com/b5/2018/11/26/a1400746.html'
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
            香港星期日舉行立法會九龍西補選,民主派全體總動員聲援李卓人,呼籲選民務必集中票源
            全投李卓人,對抗中共將香港變為大陸城市,選出能夠捍衛香港一國兩制,及守護香港核心價值
            的候選人。 口號:「選情嚴峻,爭你一票」、「集中就贏,分散就輸」。 代表民主派出戰
            的工黨李卓人早上8時在九龍區石硤尾展開拉票活動,包括被政府剝奪參選資格的劉小麗、
            民主黨主席胡志偉、公民黨主席梁家傑及多位民主派立法會議員到場聲援。李卓人強調今次
            選舉關乎港人的未來。 工黨李卓人:「二個未來的對決,兩陣的對決,我李卓人是代表我們
            繼續捍衛香港一國兩制,我們的自由和法治、人權,爭取我們應有的真普選的權利,五號的
            保皇黨(陳凱欣)所代表的是只會配合中共打壓,將香港變為另一個大陸城巿。」 民主派強調
            中共投入大量資源滲透社會各方面,只差一步就掌握港人命運。呼籲選民務必集中票源,投票
            支持李卓人。 民主黨主席胡志偉:「3號李卓人是唯一的選擇,也是民主派支持的唯一代表,
            如果大家不能集中票源的話,其實就是幫共產黨在港的代言人。所以大家在港想安生樂命,
            所需要是一個能夠真正維護一國兩制、核心價值的候選人。」 九龍西有約49萬選民,選民
            從早上七時半到晚上10時半,可到所屬票站投票。補選其他候選人包括伍迪希、曾麗文、
            馮檢基、陳凱欣。 扒:今次補選是民主派關鍵的一票,關乎能否守住立法會分組點票的
            否決權。
            '''
        ),
    )
    assert parsed_news.category == '港澳'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1543161600
    assert parsed_news.reporter == '林秀宜'
    assert parsed_news.title == '港九龍西補選 民主派動員撐李卓人抗衡中共'
    assert parsed_news.url_pattern == '2018-11-26-1400746'
