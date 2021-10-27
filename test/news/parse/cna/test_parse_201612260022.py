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
    url = r'https://www.cna.com.tw/news/aipl/201612260022.aspx'
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
            立法院司法及法制委員會今天審查婚姻平權法案,朝野黨團都表示不會阻擋。但立法院內外
            周邊街道都有優勢警力駐守,慎防有人衝進立院干擾議事。 立法院司法及法制委員會上午
            審查婚姻平權法案,立法院朝野黨團都表示,不會干預、阻擋,但對於修民法還是立專法,仍無
            共識,就算完成初審,離三讀還有很長的路要走。 但今早立法院周邊都有優勢警力駐守
            ,院區內警力部署滴水不漏,康園餐廳外設有警察補給站,咖啡行動車提供咖啡等飲料與補給品
            ;場外社團集結,播放歌曲。 尤美女:不是上帝 怎有權決定別人人權 立法院司法及法制
            委員會召委、民進黨立委尤美女今天回應反同團體擬發動公投決定能否修正民法表示,人權
            不適合公投,「我們不是上帝」,怎有權力決定別人的人權。 立法院司法及法制委員會上午
            審查婚姻平權法案,總計有民進黨立委尤美女、蔡易餘、國民黨立委許毓仁、時代力量黨團
            各自提出的民法親屬編部分條文修正草案、民法部分條文修正草案等4個版本,法務部長
            邱太三列席備詢。 會議主席、民進黨立委尤美女上午會前受訪表示,台灣是一個民主的
            社會,可以有各種不同意見,草案出委員會之後,還有黨團協商,因為這個會期即將結束,下個
            會期開議後,先進行總質詢,總質詢結束後才能排法案,如果要二讀,要等明年4月底、5月初
            ,有半年時間盡量溝通協調。 被問到若有衝突發生是否要停止審查,尤美女說,世界各國關注
            ,留給立法院專業理性問政的空間,會依照正常程序逐條討論法案。 有關反同團體擬發動
            公投決定民法修正,尤美女說,人權不適合公投,「我們不是上帝」,怎麼有權力決定別人能否
            享有人權。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1482681600
    assert parsed_news.reporter == '溫貴香、王承中台北,溫貴香、王承中台北'
    assert parsed_news.title == '審婚姻平權法案 立院內外警力駐守'
    assert parsed_news.url_pattern == '201612260022'
