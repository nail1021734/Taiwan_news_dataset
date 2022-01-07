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
    url = r'https://star.ettoday.net/news/2026280'
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
            福原愛、江宏傑這對昔日「桌球界金童玉女」,從今年2月開始遭爆婚變,歷經近五個月後,
            終於在今(8日)宣告離婚,不管兩人婚姻告終的起始原因為何,福原愛丟下稚兒、病母在台灣,
            被日媒拍到和「橫濱大谷翔平」約會、上酒店,都讓她清純形象在台日兩地徹底毀滅,還可能
            要付出高額贍養費,但福原愛為了拯救事業,立刻出招在微博發聲,果然效益不錯。 日本向來
            對於「女性不倫」這件事看得頗重,日媒報導,東奧倒數兩週,原本福原愛接下解說員工作,
            在爆出不倫疑雲事件後,有知情人士爆料,她的行程表至今仍是空白,恐遭切割,連一向和她
            友好的日本桌球協會,原本預計東奧後要和她一起捐免費桌球桌,雖因疫情延到明年,但目前
            她形象變差,知情人士也說,可能計畫就此告終了;而台灣觀眾雖然善忘,但目前大多數也對
            福原愛印象不佳。 看似福原愛在台灣、日本的事業都毀滅,但她在與江宏傑聯名向台灣、
            日本媒體發出聲明後,又突然出招,不在家鄉日本慣用的推特,也沒在台灣常使用的臉書、
            IG發聲,在微博以個人身份發聲道歉:「一直溫暖守護,鼓勵著我並給我力量中國的球迷、
            粉絲們,很抱歉...因為我的私事報導給大家帶來困擾和麻煩,我一定會加油的,感恩不管何時
            都支持我的家人和朋友們。​」馬上引來大批大陸網友心疼留言打氣。 從婚變傳聞爆出以來,
            大陸網友始終一面倒給予福原愛滿滿的支持,福原愛從小就在大陸東北接受桌球訓練,一口
            流利中文還帶著東北腔,搭配甜美笑容,對陸網來說可愛又親切,聽到有人好像欺負愛醬,
            自然比誰都生氣,即使福原愛被拍到上酒店,也還是照挺,認為一定都是江宏傑的錯,還在
            江宏傑微博留下許多幾乎已涉及人身攻擊的言論。 如今福原愛選擇在微博上發聲,更特地
            強調:「給我力量的中國球迷、粉絲們。」不難看出她重視哪一邊的形象,即便未來日本體壇
            、台灣娛樂圈真的冷凍她,她也有極高機率轉向大陸市場發展搏翻身。 細屬兩人爆婚變這段
            日子以來,福原愛不斷透過特定媒體,以「友人」角度爆料與江宏傑不睦的新聞,江家這邊則
            選擇沈默以對,更在福原愛媽媽準備離台前,全家到齊送機;在今天訴請離婚結果出爐前,日媒
            報導江宏傑與師妹「木木」林葦妮曖昧,但木木在日本沒什麼知名度,卻突然躍上日媒版面,
            顯得相當離奇,如今隨著兩人正式離婚,這些紛擾終於能歸於平靜。 作者蔡琛儀,現為
            《ETtoday星光雲》娛樂中心唱片線記者。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1625752080
    assert parsed_news.reporter == '蔡琛儀'
    assert parsed_news.title == '福原愛不倫重創形象「台、日事業全毀」 婚變最終集放大絕救人氣'
    assert parsed_news.url_pattern == '2026280'
