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
    url = r'https://star.ettoday.net/news/2031765'
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
            台北101購物中心一年一度的「頂級珠寶腕錶大師之作World Masterpiece」,
            正於Stage@Taipei 101(簡稱Stage 101)線上熱烈進行中,逾20個品牌端出超過200件
            傑作共襄盛舉,不僅可線上欣賞與購買品牌精選之作,亦整合線下資源,可於網站預約專賣店
            鑑賞。此外,台北101也邀請瑞士鐘錶權威機構FHH總理事Carson Chen進行線上講座、
            分析趨勢,讓消費者收穫滿滿。 堅強陣容 受新冠肺炎疫情全台三級警戒影響,台北101舉辦
            的「頂級珠寶腕錶大師之作World Masterpiece」,今年首度轉往線上平台,依然吸引
            BLANCPAIN、Breguet、LONGINES、OMEGA、RADO、Swatch、TISSOT、BVLGARI、
            CHAUMET、Chopard、HARRY WINSTON、MIKIMOTO、FRED、HUBLOT、IWC、
            Jaeger-LeCoultre、PANERAI、PIAGET、Roger Dubuis、Vacheron Constantin
            與 Grand Seiko等品牌參展,紛紛祭出限量款或全台獨家款式吸睛。 系列手鐲式彩寶花卉
            高級珠寶工藝腕錶。 優惠驚喜 結合實體與線上兩大版圖的「頂級珠寶腕錶大師之作
            World Masterpiece」,展期正逢七夕情人節與父親節前夕,台北101獻上珠寶與腕錶高達
            7%的驚喜回饋,即日起至8月15日止凡消費珠寶腕錶,刷101聯名卡單筆滿5萬元送2500,刷
            合作銀行信用卡滿10萬元送5000,若從線上Stage 101下單再加碼購物金點數10倍送,等
            同於再拿2.5%回饋。 知識專區 除了賞珠寶腕錶與購物,「頂級珠寶腕錶大師之作
            World Masterpiece」還開辦線上講座,自7月23日到8月20日的每個星期五,提供了
            線上藏家錶友私人聚會,也就是國際專家開講的線上直播workshop,由瑞士高級製表基金會
            FHH 總理事陳楷遜Carson Chan主講,透過「專家導航看2021國際腕錶趨勢」、
            「何謂高級製錶?瑞士高級製錶基金會來告訴你」、「如何收藏與保養你的機械錶?瑞士
            腕錶專業認證 課程預告」,以及「該進廠保養了嗎?專家教你判斷腕錶的狀態 」等主題,
            傳遞第一手資訊。 而針對珠寶客群,台北101特別規劃「抽一張牌,找到你跨時空的幸運
            力量!」workshop,邀請占星大師蘇飛雅以星座塔羅的方式,輕鬆有趣帶領大家認識珠寶藝術
            。所有台北101 World Masterpiece 線上講座採預約報名制。
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1626656400
    assert parsed_news.reporter == '陳雅韻'
    assert parsed_news.title == '台北101頂級珠寶腕錶大師之作展線上起跑 專家開講收穫滿滿'
    assert parsed_news.url_pattern == '2031765'
