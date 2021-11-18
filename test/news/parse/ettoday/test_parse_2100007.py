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
    url = r'https://star.ettoday.net/news/2100007'
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
            共機近來頻繁侵擾台灣防空識別區。美國國防部表示,中國擴大對台灣恫嚇與施壓,增加
            誤判風險。五角大廈重申對台承諾堅若磐石,也呼籲北京和平解決兩岸分歧。 中國解放軍
            軍機近來頻繁擾台,入侵台灣防空識別區(ADIZ)引來區域緊張,也成為美國國防部記者會
            今天的焦點議題。 美國國防部發言人柯比(John Kirby)今天面對媒體多次提問關於
            兩岸緊張局勢升高一事表示,中國擴大對台灣與其他盟友和夥伴的恫嚇與施壓,包括增加
            在台灣、南海、東海附近的軍事活動,將增加誤判風險。 他指出,美方對台灣的支持與和
            台灣的國防關係,與台灣當前面臨的中國威脅一致,美方也敦促北京履行美中三公報中和平
            解決兩岸分歧的承諾。 至於國防部是否正在討論若採取任何行動保衛台灣需要國會批
            准時,柯比表示,不會討論假設性議題。但他重申,美方長期遵循一個中國政策,這和北京的
            一個中國原則不同。根據中國的一中原則,中共對台灣擁有主權,但美方對台灣主權問題
            不持立場。 柯比也指出,美方將持續支持以符合台灣人民意願與最大利益,和平方式解決
            兩岸議題。美方對台灣的承諾堅若磐石,維護海峽兩岸與區域和平穩定。 柯比一再重申,
            不會討論防空細節,但也表達關切中國在台灣附近的挑釁性軍事活動,認為這將破壞穩定
            並增加誤判風險。他也數度敦促北京停止這種軍事外交與經濟施壓以及對台灣的脅迫,台灣
            和平穩定始終是美國利益所在,美方將繼續協助台灣維持足夠的自我防衛能力。 根據
            國防部統計,10月1日至5日期間,有高達150架次共機擾台,其中4日有56架,是國防部
            去年9月17日開始揭露共機動態以來,數量最多一次。相較去年整年約380架次,增加幅度驚人
            ,引發美國、澳洲及英國等民主國家關切。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634092080
    assert parsed_news.reporter is None
    assert parsed_news.title == '共機擾台架次飆增 美國防部:增加誤判風險「敦促北京停止脅迫」'
    assert parsed_news.url_pattern == '2100007'
