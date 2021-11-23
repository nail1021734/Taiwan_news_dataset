import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/12/7/3/n3626870.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            考古學家在危地馬拉科羅納訥(La Corona)遺址的一座石梯發現若干刻文,證實了瑪雅
            曆法的「終結日期」落在2012年12月21日。 中央社援引英國「每日郵報」(Daily M
            ail)報導,這是第2塊已知證實「終結日期」的碑文。全球各地的新紀元(New Age)教
            派解讀此為可能發生世界末日,使得美國防爆避難所銷售激增,以及末日信徒湧入法國
            一座村莊避難。 此瑪雅碑文成為狂熱網絡陰謀論的話題,有些人預言人類世界將被黑
            洞吞噬,或是遭小行星撞上,或者會被遠古天神摧毀。 這塊石碑有1300年曆史,是數十
            年來發現的最具意義象形文字文物之一。 這塊石碑的碑文,內容多半與政治歷史有關
            ,但在一段關於國王回歸的文字裡,也提及「終結日」。 領導此次考古挖掘的美國得
            克薩斯州大學(University of Texas)史徒華(David Stuart)表示:「當時瑪雅地
            區處於嚴重政治動盪時期,使這位國王不得不暗示更大規模的時間週期將於2012年結
            束。」 然而,許多瑪雅人指稱,啟示預言主要是西方觀點。瑪雅人認為,碑文指的是新
            時代的開始,而非時間本身的結束,這份「啟示」是指從瑪雅長期歷(Long Count)西
            元前3113年開始計算以來,歷經5125年的週期結束。 美國國家航空暨太空總署(NASA
            )表示,這個故事源於蘇美人發現的一顆假設行星Nibiru正朝地球而來的說法。這些傳
            說稱瑪雅古老曆法的其中1個週期將在2012年冬至結束。 共同領導拉科羅納挖掘工作
            的卡努托(Marcello A. Canuto)說:「碑文提到的是古代政治歷史,不是預言。」
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1341244800
    assert parsed_news.reporter == '郭惠'
    assert parsed_news.title == '瑪雅出土碑文證實 「今年存在終結日」'
    assert parsed_news.url_pattern == '12-7-3-3626870'
