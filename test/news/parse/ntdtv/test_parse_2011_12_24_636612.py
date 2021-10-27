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
    url = r'https://www.ntdtv.com/b5/2011/12/24/a636612.html'
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
            朝鮮獨裁者金正日病逝後,外界關注他的兒子金正恩能否平穩接班,也有人不看好。不過,朝鮮
            官方已經確立了金正恩的最高領導人地位,金正恩也已經行使了軍隊指揮權。與此同時,韓國
            領導人表達了與朝鮮改善關係的意思,美國和中國則以朝鮮半島為棋盤,暗中較勁。 朝鮮
            勞動黨中央機關報12月22號發表社論,稱呼金正恩是「事業的繼承者、人民的領導者」。朝鮮
            官方通訊社則表達了朝鮮軍民將「忠於金正恩的領導」。《韓聯社》解讀,這事實上宣佈了
            「金正恩時代」的開啟。 韓國《朝鮮日報》23號報導,在公布金正日去世消息之前,金正恩
            以黨中央軍委的名義,向全軍下達了「金正恩大將1號令」,指示全軍立刻停止訓練,返回所屬
            部隊。 韓國《中央日報》披露,金正恩今年9月對朝鮮軍隊進行了改編,並已經在行使作戰
            領域的實質指揮權。金正恩撤下了全部一線指揮官,替換成對自己忠誠的30歲到40歲的
            軍官。 韓國統一研究院首席研究員鄭永泰表示,不要認為世襲體制會和原有體制存在太大
            區別,金正日生前已經為金正恩體制上臺打好了基礎。「上海復旦大學」韓國朝鮮研究中心
            副主任蔡建教授也這麼認為。 蔡建:「我覺得他順利接班的可能性還是比較大的,雖然他
            接班時間短,但是金正日在這之前也做了充分的安排,把一些重要的人物、非常忠心於他的
            人物安排在一些最重要的崗位上面,其中他的妹夫張成澤和吳克列這兩位對他非常忠誠的
            元老級的人物,安排在國防委員會副委員長的位置上面。」 德國《每日鏡報》指出,對金正恩
            和朝鮮的穩定來說,更為關鍵的是中國的支持。金正日去世後,胡錦濤等9名中共政治局常委,
            都前往朝鮮駐北京大使館弔唁,並明確表示支持金正恩,中國近期可能向朝鮮提供糧食
            援助。 美國白宮發言人卡尼21號在記者會上表示,「金正日生前指定金正恩為正式接班人,
            目前沒有找到任何變化跡象。」這是白宮首次將金正恩稱為接班人。 美國國務卿希拉里發表
            聲明為朝鮮民眾祈禱,表示美方已準備好援助朝鮮民眾,希望新領導人將朝鮮引入和平的
            道路。美國國務院官員則與朝鮮駐聯合國外交官進行「電話外交」。 韓國《中央日報》
            指出,美國和中國爭先恐後對「後金正日時代」的朝鮮實行介入政策,因為美中都不希望朝鮮
            內部的不穩定引發朝鮮半島緊張升級,同時也有擴大在東北亞影響力和牽制對方的意圖。 韓國
            總統李明博22號強調,六方會談成員國一致希望朝鮮體制能夠儘快穩定,未來南北關係完全可以
            做到「靈活」,「韓國所採取的措施為的是向朝鮮表明並沒有敵對朝鮮」。 《朝鮮日報》說,
            韓國政界在金正日去世後達成共識,將以此為契機改善南北關係。韓國政府高層官員說:「
            如果金正恩體制表現出與我方和解的誠意,我們完全可以提供幫助。」 《韓聯社》援引韓國
            經濟研究員的分析,隨著消極對待改革開放的金正日時代落幕,朝鮮改革開放的可能性也隨之
            增大。中國正在促進以開放為主的中朝經濟合作,韓國也曾以棄核為條件承諾提供400億美元
            的援助。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324656000
    assert parsed_news.reporter == '常春,李元翰,周平'
    assert parsed_news.title == '金正恩行使軍權 韓美中對朝釋善意'
    assert parsed_news.url_pattern == '2011-12-24-636612'
