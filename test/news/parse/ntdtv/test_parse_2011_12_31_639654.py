import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.ntdtv
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/31/a639654.html'
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
            金正日去世後,外界密切關注朝鮮半島的和平和穩定,12月30日,朝鮮國防委員會發表聲明,
            宣稱:國際社會“不要期待我們會發生任何變化”。“朝鮮將永遠不會同李明博交往。”這表明
            兩國關係降到了冰點。 朝鮮前最高領導人金正日於12月17日去世,朝鮮為其舉行國葬。 據
            英國《BBC》報導,韓國方面對國民前往朝鮮弔唁做出限制,只允許兩個民間弔唁團前往悼念,
            引發朝鮮不滿。 朝鮮國防委員會聲明說:“我們對韓國傀儡政權以及世界上所有愚蠢的政治家
            鄭重宣布,不要妄想我們會發生任何變化。”“朝鮮將永遠不會同李明博交往。” 這項聲明
            星期五(30日)中午在朝鮮國家電視台播放了11分鐘。 韓國「聯合新聞通訊社」報導,據韓國
            政府官員表示,朝鮮國防委員會的聲明內容和措辭都令人大感失望,但韓國政府的基本立場
            不會受其影響。 韓國政府一貫主張努力減緩朝鮮緊張氣氛、透過對話解決問題。 韓國統一部
            表示,將會“迅速回應”朝鮮半島上的任何變化。 韓朝關係降到了冰點 朝鮮在1994年領導人
            金日成追悼大會次日,也曾點名批評時任韓國總統的金泳三,導致兩國關係一度陷入惡化。 自
            李明博2008年2月當選韓國總統後,韓國政府將對朝鮮的經濟援助同停止核武計劃掛鉤。韓朝
            關係持續降溫。 在2010年3月韓國“天安艦”被擊沉造成46名水兵身亡以及同年11月朝鮮
            砲擊延坪島之後,兩國關係更是降到了冰點。 韓國韓聯社認為,聲明直接來自朝鮮勞動黨
            國防委員會,而不是引述那裡的一名發言人,這種情況較少發生。這意味著南朝鮮關係將在
            今後很長一段時間內難以走出困境。 美、中、韓開始密集外交 美國國務院星期四(12月
            29日)發表聲明說,美國助理國務卿坎貝爾將於下星期訪問中日韓三國,討論包括“同朝鮮
            相關的最新發展”等相關議題。在韓國,美國駐有28000名士兵。 《BBC》報導,韓國
            國防部長金寬鎮與美國國防部長帕內塔已通過電話,韓國國防部表示,雙方一致認為朝鮮半島
            和平穩定至為重要,決定維持聯合防衛。需要關注朝鮮內部動向,會繼續維持對朝鮮的監視及
            偵察級別不變。 不足30周歲的金正恩上台,世界更加關注朝鮮是否發生某種變化。金正日
            執政期間,朝鮮于90年代發生特大饑荒,數十萬人因饑饉而亡。與此同時,朝鮮大力發展核武
            與導彈計劃,而該行動又導致國際社會的製裁。聯合國機構稱,該國目前仍有約三分之一的
            人口(即600萬)急需食品援救。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325260800
    assert parsed_news.reporter == '楊雪'
    assert parsed_news.title == '報復韓國 朝鮮稱與李明博斷交 別妄想有變'
    assert parsed_news.url_pattern == '2011-12-31-639654'
