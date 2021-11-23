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
    url = r'https://www.epochtimes.com/b5/19/1/4/n10954370.htm'
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
            加拿大統計局週五(1月4日)表示,2018年12月新增就業人數淨值為9300人,失業率維持在43
            年低點,達到5.6%。 據美房置業網消息,自加拿大1976年1月開始收集
            並測量可比數據以來,失業率連續第二個月處於最低水平。而在此前,經濟學家預計12月將
            增加5,500個就業崗位,失業率為5.7%。 即使在緊縮的就業市場中,最新的勞動力調查顯示
            ,12月的工資增長再次顯示為1.49%,遠低於通脹。11月份永久僱員的平均小時工資增長率為
            1.46%——自5月份的峰值3.9%以來穩步減速。 12月份的結果是,11月份淨就業人數增加了
            94,100人,這是加拿大自2012年3月以來的最大月度增幅。 加拿大統計局表示,全國新增
            就業人數在2018年增加了163,300人,增長率為0.9%,增速放緩,而2017年為2.3%,2016年
            為1.2%。 2018年的就業增長主要集中在服務業,產生了151,000個職位,而商品生產行業僅
            增加了12,300個。 2018年,25至54歲婦女的就業人數增加了125,600個職位(或2.2%),
            而同一年齡段的男性就業人數增加了1%,為60,600個。 2019年第一個主要經濟數據 週五的
            報告是2019年發布的第一個主要經濟數據。 由於加拿大強勁的經濟表現,央行將於下週三公
            布利率。自2017年夏季以來已上調基準利率五次,加拿大央行行長Stephen Poloz已表示
            需要進一步增加以防止通脹上升過高。 以下是加拿大12月就業情況速覽(括號中為11月數據)
            :失業率:5.6%(5.6%)失業人數:1,125,100(1,124,800)工作人數:18,808,
            400(18,799,100)青年(15-24歲)失業率:11.1%(10.8%)男性(25歲以上)失業率
            :4.9%(5.0%)女性(25歲以上)失業率:4.6%(4.7%) 加拿大12月份的全國失業率為5.6
            %。以下是各省12月的失業率(括號中為11月數據):紐芬蘭和拉布拉多11.7%(12.2%
            )愛德華王子島9.6%(8.5%)新斯科捨省7.1%(7.0%)新不倫瑞克省8.4%(7.9%
            )魁北克5.5%(5.4%)安大略省5.4%(5.6%)曼尼托巴省6.0%(5.7%)薩斯喀
            徹溫省5.6%(5.5%)艾伯塔省6.4%(6.3%)卑詩省4.4%(4.4%)
            '''
        ),
    )
    assert parsed_news.category == '加拿大,溫哥華,新聞,加拿大新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1546531200
    assert parsed_news.reporter is None
    assert parsed_news.title == '統計局:加拿大失業率維持43年來新低'
    assert parsed_news.url_pattern == '19-1-4-10954370'
