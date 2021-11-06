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
    url = r'https://star.ettoday.net/news/1200260'
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
            睡眠障礙是比憂鬱症更為常見的一種疾病。 根據一項統計調查顯示,約有兩成的成年人有
            睡眠障礙的煩惱,更有高達三成的老年人深受失眠所苦。有人抱怨躺在床上輾轉反側,往往要
            花上好幾個小時才能入睡,臨床上稱這種睡眠障礙為「入睡困難」型。 此外也有人抱怨老是
            睡不好,經常中途醒來,想再睡卻又睡不著,這屬於「睡眠中斷」型。另外有人抱怨天未亮就
            醒來,這是很多老年人常見的「過早覺醒」型。還有一種「熟睡困難」型,患者睡醒後老是覺得
            沒睡飽,睡眠品質很不好。 一般睡眠障礙大致可分為這四種類型,不過,也有人同時出現一個
            以上的類型,嚴重影響生活品質。 人工照明太發達才會失眠? 如果到醫院求診,醫師多半會
            開給病人安眠藥來幫助他入眠,如此一來,又有「不吃就睡不著」的擔憂。事實上,長期使用
            安眠藥,的確容易讓人產生藥物依賴性,無論如何,依靠藥物終究不是辦法。 人們之所以會
            出現失眠或是睡眠障礙,追根究柢還是因為「人工照明太發達,人類不再曬太陽」這件事。大家
            都知道,地球上包括人類在內的所有生物,體內都有一個「生理時鐘」,一旦生理時鐘與現實
            時間脫節,就會誘發睡眠障礙。所以,請盡量養成在晨光中甦醒的習慣,讓生理時鐘自動回復
            正常,才是解決失眠問題的上上之策。 多曬太陽找回一夜好眠 當早晨的陽光映入我們的眼簾,
            光線經由生理時鐘中樞、也就是下視丘的視神經交叉上核到達脊髓,再經由上頸部
            的神經節傳回松果體,因而降低褪黑激素的分泌量。 隨著褪黑激素分泌量的減少,我們的生
            理時鐘會自休眠中甦醒,此時,包括體溫、血壓、脈搏、尿液量、各種激素與酵素的運作,以
            及食慾、自律神經系統和精神狀態等所有生命現象的節奏,都調整到最適合白天活動的狀態
            。 而當太陽下山後,光線轉暗,光刺激大幅減少,褪黑激素的分泌量便開始增加,此時我們身
            體的日夜節奏就逐漸進入休息、睡眠的週期。順便一提,就算是全盲的人,也能夠維持體內
            生理時鐘的正常運作,由此可知人類的皮膚細胞確實能夠感知陽光並加以反應。需要日夜輪
            班的人、以及生理時鐘中樞機能降低的老年人,當然都不容易過著「日出而作,日落而息」
            的生活,不過,如果能夠盡量與太陽同步,回到人類原本的自然作息時間,必能大幅改善睡眠
            問題。 根據一份最新的研究報告指出,有睡眠障礙的人,他們早死的風險大於正常人。所以
            我們除了應當維持生理時鐘的正常運作外,還可以多做運動。運動不但有益健康,還能夠幫
            助我們一夜好眠,從而使我們的日夜節奏與自然環境同步。 因為文明而被打亂了的生理時
            鐘,想要把它調回正常的運作狀態,還是得藉助太陽的力量,大家何不試著再重新設定一次看
            看呢?
            '''
        ),
    )
    assert parsed_news.category == '健康'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530225000
    assert parsed_news.reporter == 'Flora'
    assert parsed_news.title == '重新設定生理時鐘,可消除睡眠障礙'
    assert parsed_news.url_pattern == '1200260'
