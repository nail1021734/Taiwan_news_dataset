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
    url = r'https://www.ntdtv.com/b5/2011/04/17/a519866.html'
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
            下面來看本週其他大事件 美英法聲明 軍事行動至卡扎菲下臺 星期五,美英法三國首腦
            發表聯合聲明,矢言將持續軍事行動,直至卡扎菲下臺。聲明說,屠殺本國平民的卡扎菲繼續
            掌權是不可思議的,是對反抗卡扎菲的利比亞人民的道德背叛。聲明還指出,國際刑事法庭
            應對卡扎菲軍隊在鎮壓中對平民犯下的嚴重違反國際法的罪行展開調查。星期五北約外長在
            柏林結束了第二天的會議。預計盟軍會增派飛機,以加強對卡扎菲軍的空襲。 阿根廷前獨裁者
            被判無期 星期四(4月14日),前阿根廷軍政府獨裁者比尼奧內和軍政府的另外3名高官由於
            當政期間參與謀殺、酷刑折磨、非法監禁等一系列侵犯人權罪而被阿根廷法院判處無期徒刑。
            人權組織說,在1976到1983年的阿根廷軍政府獨裁統治期間,高達3萬人被綁架和殺害。 北非
            前獨裁者面臨審判 在茉莉花革命浪潮中被推翻的兩名北非前獨裁者面臨控罪和審判。突尼斯
            司法當局星期四準備向前總統本阿里提出18項指控,罪名包括販毒和蓄意殺戮等。突尼斯當局
            正試圖將本阿里及家人引渡回國。另外埃及前總統穆巴拉克(Hosni Mubarak)和兩個兒子
            本週被拘押,接受貪腐及暴力鎮壓等罪名調查。埃及官方媒體星期五說,如果被裁定下令殺害
            示威者的罪名成立,穆巴拉克最高可能被判死刑。對穆巴拉克的審判預料將持續至少1年。 無
            錫數萬人抗議垃圾焚燒 迫警撤離 江蘇無錫東港鎮黃土塘村民抗議垃圾焚燒發電廠項目再起
            高潮。11號,數萬民眾與政府出動的數千武警對峙,迫使武警於當晚撤離。錫東生活垃圾焚燒
            發電廠建在黃土塘村人口稠密區,方圓五公里內,有十幾所幼兒園和中小學,且離直通長江的
            運河僅100米。當局雖承諾點火開工要經環保總局評估,但實際已多次夜間點火試燒,環境學家
            表示,混合垃圾直接進行焚燒處理是產生二惡英的「罪魁禍首」,是目前世界上已知毒性最強
            的環境污染物。 全球各地紀念人類首飛太空50週年 4月12號是人類首次實現太空飛行50
            週年紀念日,俄羅斯,美國及世界許多地區都舉行了慶祝活動。在俄羅斯首都莫斯科,人們冒著
            雨雪來到加加林廣場,用鮮花和氣球慶祝。這一天也是美國首次發射航天飛機30週年的
            紀念日。美國宇航局和國際空間站也都舉行了慶祝。1961年4月12號,前蘇聯宇航員加加林
            乘宇宙飛船繞地球一週,實現了人類史無前例的宇宙飛行。1981年4月12號,美國哥倫比亞號
            航天飛機升空在太空中遨遊了2天,實現軌道飛行,開創了人類太空旅行和探索的新時代。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302969600
    assert parsed_news.reporter is None
    assert parsed_news.title == '新聞週刊265期大事件'
    assert parsed_news.url_pattern == '2011-04-17-519866'
