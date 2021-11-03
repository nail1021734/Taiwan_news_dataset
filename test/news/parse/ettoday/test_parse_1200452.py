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
    url = r'https://star.ettoday.net/news/1200452'
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
            炎熱的夏季到了,手搖飲是民眾的最愛,CoCo特地量身訂製一首「CoCo夏日主題曲」和影片,
            歌詞簡單讓人朗朗上口,搭配簡易舞蹈,引起不少網友注意,有些網友還拍攝自己跳舞的版本
            上傳,成功打造「洗腦神曲」,就連LamiGirls、網紅和學生團體都來一起共襄盛舉! 超受歡
            迎的女團LamiGirls副隊長巫苡萱、琳妲、羚小鹿跳起「CoCo夏日主題曲」,她們三位表示
            舞蹈超級易學,只花了10分鐘就學會,而巫苡萱說她平常就最喜歡喝CoCo的百香雙響炮,是名
            符其實的CoCo粉絲,羚小鹿對加了草莓和蔓越莓的莓果系列情有獨鍾、琳妲則支持CoCo珍奶
            ,感覺特別有嚼勁。 超受歡迎的女團LamiGirls副隊長巫苡萱、琳妲、羚小鹿跳起「CoCo夏
            日主題曲」,她們三位表示舞蹈超級易學,只花了10分鐘就學會,除了LamiGirls和學生團體,
            現在就連網路紅人也來參一咖,包括Nico古璇、super Lisa 、街頭藝人小綠人,還有超活潑
            的世新啦啦隊也都拍攝影片上傳到粉絲團,讓許多網友看了直呼超可愛,忍不住都想衝到
            CoCo來買茶飲! CoCo推出「飆涼Fun暑假」主題活動,從7月5日至8日為期四天,各店任選 2天推
            出夏季飲料折扣優惠,百香雙響炮特價35元(原價$45)以及莓果派對特價28元(原價$50),民
            眾可得把握機會,各店還有「涼夏變裝主題」,店員會打扮成不同的可愛裝扮,讓顧客充滿新
            鮮感,想知道詳請快上CoCo官網查詢,跟著CoCo一起「飆涼Fun暑假」!
            '''
        ),
    )
    assert parsed_news.category == '民生消費'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530788820
    assert parsed_news.reporter is None
    assert parsed_news.title == 'CoCo夏日主題曲超洗腦 「飆涼」飲品限定優惠!'
    assert parsed_news.url_pattern == '1200452'
