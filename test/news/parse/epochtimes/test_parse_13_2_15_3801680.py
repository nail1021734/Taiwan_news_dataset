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
    url = r'https://www.epochtimes.com/b5/13/2/15/n3801680.htm'
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
            新發現的小行星2012 DA14約半個足球場大小,明天將掠過地球,成為目前所知這種大小的天
            體中,最貼近地球飛掠者,讓科學家難得有機會在無須發射探測器情況下近距離觀測。 小行
            星2012 DA14將以每秒13公里速度掠過地球,最接近地球的時間點是台北時間16日凌晨3時24
            分,屆時距離地球表面約2萬7520公里,比繞地運行的電視網絡和氣象衛星更接近地球。 雖
            然小行星2012 DA14是目前所知此等大小天體中,如此貼近掠過地球的最大顆小行星,但科學
            家表示,本週或可預見的未來它都不會撞擊地球。 加州巴沙迪納(Pasadena)美國國家航空
            暨太空總署(NASA)噴射推進實驗室(JPL)天文學家姚曼斯(Donald Yeomans)說,目前
            2012 DA14繞太陽公轉的速度與地球相仿,但明天掠過地球後,它的飛行路線將會
            改變。 姚曼斯說:「這次的接近將擾亂它的軌道,因此實際上公轉週期不是1年,反而將會
            減少幾個月。」他還說:「地球會讓這顆小行星處於相當安全的軌道上。」 儘管2012 DA14
            相當接近地球,但由於體積不大,即便用最大的光學望遠鏡觀看,仍只能看到1個亮點。根據
            它的亮度,天文學家預估小行星的直徑僅大約45公尺。 最佳觀測地點將是印尼,東歐、亞洲
            和澳洲也是觀星的好位置。但當地球轉自適合美國大陸觀星的角度,小行星的亮度已大幅減退。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1360857600
    assert parsed_news.reporter is None
    assert parsed_news.title == '小行星飛掠地球 難得近距觀測'
    assert parsed_news.url_pattern == '13-2-15-3801680'
