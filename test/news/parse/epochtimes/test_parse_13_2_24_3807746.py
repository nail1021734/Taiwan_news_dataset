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
    url = r'https://www.epochtimes.com/b5/13/2/24/n3807746.htm'
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
            家庭房車品牌可謂是種類繁多,樣式或款式也是多種多樣,豪華的、省油的、油電混合型的
            、運動型的等等,消費者也是根據自己的需要或愛好去選擇一款最適合自己的。而對於來自
            日系的Honda Civic可以說是家喻戶曉,如今的Civic可到底是甚麼樣的一款車呢?它是否能
            打動或吸引熟悉它的人群的眼球呢? 試駕的這款2013 Honda Civic Touring是Civic房車的
            四個版本中的最高版本。它的Touring版裝備當然也是樣樣齊全,可以稱得上是步步到位;另
            外,它的價格也頗具吸引力,售價為加幣$26,335。 如今,體形較小的Civic的外觀更顯時尚
            魅力,姿態端莊大方,柔和細膩的線條均勻地勾畫著整個車身,使得車身顯得狹長而纖細,飽
            滿的尾部設計中夾雜著幾條錯落有緻的弧線,看上去多了幾分矯健,幾分帥氣,幾分自信。在
            車頭部位較為突出的是它的進氣格柵和頭燈組的設計,分為上下兩條呈向上弧狀彎曲的鍍鉻
            條槓鑲嵌在車頭處,這樣一來,使得整部車透出一種強勢的氣息。 觀察車廂內,此時正逢落
            日,柔和的光線穿過天窗進入室內,室內裝飾佈置整齊有序,按鈕式啟動引擎,各種信息從各
            個界面閃現,一種溫馨愜意油然而生。車門、儀錶盤、傾向駕駛者方向的中控台、擋位、手
            剎車操作桿,以及前排座椅扶手團團圍住整個駕駛位置周圍,這些都便於駕駛者進行操作。
            至於它的各種裝備,如:藍牙,導航系統,音響系統,空調,車輛運行時還有節油環保的Eco系統
            的輔助,以及多角度倒車影像等等都安裝到位。 2013款Honda Civic Touring擁有著
            一台1.8升四缸16氣門引擎,最大動力輸出為140匹馬力,最大扭力為128磅呎,同時也標準搭配了5前
            速自動波箱,車輛在行駛期 間,尤其是穿梭在繁忙的城市道路間,頻繁的起步,加速,剎車中,
            車輛都給予積極響應和恰當的配合;即使是在小角度轉彎或是在掉頭時,輕便的方向盤運用
            起來輕鬆自然,操作起來一步到位;泊車時也很好掌握合適的角度去操作,出泊車位時,在廣
            角倒車影像的輔助下,運行操作安全方便自如。進入高速行駛時,車輛的加速過程積極而迅
            速,擋位的轉換順暢流利。在400公里的路程中,耗油為9.2升每百公里。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361635200
    assert parsed_news.reporter is None
    assert parsed_news.title == '時尚魅力 2013 Honda Civic Touring'
    assert parsed_news.url_pattern == '13-2-24-3807746'
