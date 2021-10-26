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
    url = r'https://www.ntdtv.com/b5/2011/12/21/a634964.html'
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
            朝鮮獨裁者金正日病逝後,擁有核武器的朝鮮權力過渡,引起外界各種猜測。與此同時,朝鮮
            半島有關各方保持謹慎克制,避免刺激朝鮮導致誤判、引發東北亞陷入嚴重危機。美國、
            韓國、日本政府一致認為,朝鮮半島的和平與穩定不能受到金正日去世的影響。 據
            《韓聯社》報導,12月19號在金正日去世的消息發佈3個半小時前,朝鮮試射了2枚短程導彈。
            韓國政府相關負責人表示,朝鮮試射導彈與金正日去世無關。顯示了韓國在加強警戒的同時
            謹慎的姿態。 由於去年「天安艦襲擊」和「延坪島炮擊」事件,韓國政府19號在金正日哀悼
            問題上存在不同意見。但是,韓國政府20號作出了哀悼的表示,並期待朝鮮盡早恢復
            穩定。 美國國務卿希拉里19號在與日本外相會談中說,平壤平穩、和平的政權交接符合美日
            兩國的共同利益。中俄官方也表達了相似的立場。 上海復旦大學韓國朝鮮研究中心副主任
            蔡建教授表示,中、韓、美、日、俄的表態,緩和了朝鮮半島目前的緊張局勢。 蔡建:
            「中、韓、美、日這個表態我覺得很重要,就是大家都不希望在這種情況之下出現混亂,維持
            這個地區的穩定是符合大家的利益的。因為實際上在過去一、二十年裡面,危機高潮階段,
            東北亞地區、朝鮮半島地區一直是出現很危險的局勢,幾次都似乎走到要打仗的
            地步。」 《紐約時報》說,美國與韓國政府官員擔憂,朝鮮內部的權力鬥爭可能導致朝鮮對外
            進行挑釁行為。 韓國《朝鮮日報》則援引北京朝鮮問題專家的意見認為,在過去2、3年內,
            能夠威脅到金正恩體制的七、八十歲元老大多被趕出核心,因此金正恩體制不會受到太大的
            影響。 中方在致朝鮮的弔唁電文中提及:朝鮮「在金正恩的領導下」。而俄羅斯總統
            梅德韋傑夫直接將電文發給了金正恩。《韓聯社》指出,中、俄事實上已經認可金正恩
            是朝鮮的最高領導人。 《朝鮮日報》說,韓國政府和大多數專家認為,金正日去世後,朝鮮
            體製出現劇烈動盪的可能性微乎其微。韓國政府核心人士說,只要中國繼續提供支持,朝鮮
            就不會發生崩潰、內戰等巨變。 美國智庫加圖研究所資深研究員班多(Doug Bandow)分析,
            金正日去世後,雖然有人希望朝鮮發生類似「阿拉伯之春」的民主化革命,但出現「朝鮮之春」
            的可能性不大。 俄羅斯自由民主黨領袖日裡諾夫斯基也指出,只要中國和俄羅斯這兩個朝鮮
            的主要支持者沒有真正的民主,就不應指望朝鮮民主化。他說,只有中共垮臺,俄羅斯更加
            民主化,朝鮮才會發生改變。 不過,北京大學國際戰略研究中心副主任朱鋒教授認為,金正日
            去世,這對東北亞來說是一次歷史性良機。金正恩沒有掌握像金正日一樣的強權,很難像父親
            一樣繼續閉門鎖國。 旅美著名學者謝選駿也表示,金正日之死為朝鮮提供了一個開放
            契機。 謝選駿:「北朝鮮發生社會變革的可能性,幾乎可以肯定是會發生的,問題就是說它
            甚麼時候發生,以及它以甚麼形式發生。既使中國和俄國雖然在背後還支持著北朝鮮,但是
            都比北朝鮮開放,所以,北朝鮮走向開放這個前景,比在金正日的領導下應該來的更好
            一點。」 《朝鮮日報》則援引中國人民大學教授時殷弘的話警告,「後金正日時代」,朝鮮
            將面臨重大挑戰。雖然韓國主導朝鮮半島統一的可能性不斷增大,但如果所採取的措施
            不當,也可能會引發軍事衝突危機。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324396800
    assert parsed_news.reporter == '常春,李元翰,孫寧'
    assert parsed_news.title == '後金正日時代 專家析朝鮮政局走向'
    assert parsed_news.url_pattern == '2011-12-21-634964'
