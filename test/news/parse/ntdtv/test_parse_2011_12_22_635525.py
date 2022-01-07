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
    url = r'https://www.ntdtv.com/b5/2011/12/22/a635525.html'
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
            朝鮮領導人金正日17號突然去世。80後的兒子金正恩繼任朝鮮最高領導人。曾經留學瑞士的
            金正恩是否會成為朝鮮變革契機?據報導,金正日生前,曾經希望安排金正恩與中共領導人
            見面,但是中共沒有答應。作為朝鮮唯一盟友的中共將怎樣對待金正恩政權? 金正日去世消息
            曝光後,朝鮮最高當局很快的向全國發佈通告,要求全體黨員、人民軍官兵和人民「忠於尊敬
            的金正恩同志的領導」,確立了金正恩最高領導人的地位。中共中央也立即向朝鮮發去弔唁
            電文說,相信朝鮮人民會「在金正恩同志領導下」「化悲痛為力量」。由此,金正恩的領導
            地位被北京承認,電文明確啟動了共產黨國家相互確認合法性的機制。 原《百姓》雜誌主編
            黃良天認為,中共的電文已經表明他會支持金正恩政權。因為中共清楚,在這樣一種制度下,
            只能依靠血統來延續獨裁的政權。如果不是中共第一代領導人的後代執政,政權活不長久,
            中國也會走上這條路。 不到30歲的金正恩成為朝鮮最高領導人。有分析認為,曾留學瑞士的
            金正恩,思想可能較父親金正日開明,估計這位80後新領袖,非常清楚北韓不可以永遠在世界
            孤立,可能會逐步開放社會,鼓勵外國投資。 而黃良天認為,朝鮮不會在短期內會發生大的
            變化,因為朝鮮國內環境封閉,民眾被嚴重洗腦,國家內部缺乏民主改革的推動力。 黃良天:
            「我到過朝鮮,那個地方的民眾被洗腦的程度,我們從這些現在金正日逝世階段的畫面我們
            看得出來,如喪考妣呀。還有一個,改造一個國家,或者改造一個政府很容易,但是改造民眾的
            思維定勢應該是很難的。他在這個環境裡只能繼承他父親的遺志,或者他祖父的遺志。繼續
            這種獨裁。不管你在哪裏學習,在這麼一個國家裏,離經叛道那是不可能的。」 「東南
            大學」法學院教授張讚寧則認為,獨裁者的死亡往往會加速政治變革。 張讚寧:「我認為
            金正日去世可能會使朝鮮的政治改革會提前,會掃除一定障礙,可能對朝鮮的政治改革有一點
            幫助。因為民主是大勢所趨。和平演變其實是不可阻擋的。你像蘇聯、東歐都是這種情況。
            所以當一個獨裁者死了以後,多少是為民主進程掃除一定障礙。」 經濟學家茅於軾也認為,
            金正日的去世對於朝鮮的發展是一個契機。原來僵持的國際關係會得到緩和。 茅於軾:「我
            想朝鮮有可能會開啟一個新時代,但是也有可能會亂一陣。總而言之原來那個非常扭曲的
            制度會維持不下去了。」 《紐約時報》12月19號的文章說,金正恩缺乏領導經驗,是否能夠
            保證國家穩定,中國目前很難確定。中國可能要求金正恩進行有條件的經濟改革。雖然,
            一些觀察家認為金正日死後,朝鮮會發動民主政變。但是,中國方面會強烈抵制這種情況
            發生。即使美韓支持這類政變,但是中國才是深入朝鮮的國家,美韓無能為力進行干預。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324483200
    assert parsed_news.reporter == '秦雪,黎安安'
    assert parsed_news.title == '80後成朝鮮最高領袖 朝鮮變革契機?'
    assert parsed_news.url_pattern == '2011-12-22-635525'
