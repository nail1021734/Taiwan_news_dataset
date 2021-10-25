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
    url = r'https://www.ntdtv.com/b5/2011/12/20/a634429.html'
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
            統治朝鮮17年的獨裁者金正日12月17號病逝,引發全球密切關注,尤其是他的第三個兒子、
            今年29歲的金正恩能否順利接班。外界分析,「後金正日時代」,對於朝鮮半島的無核化與
            和平進程,既存在契機又充滿風險,同時也給朝鮮社會的變革帶來了機會。 朝鮮官方媒體
            19號報導,朝鮮國防委員長金正日17號在行駛的列車上,死於急性心肌梗塞,終年69歲。在此
            之前,金正日15號視察了朝鮮首家中國式大型超市「光復地區商業中心」。 朝鮮勞動黨要求
            全民「忠於金正恩的領導」。《韓聯社》報導說,金正恩將像他的父親金正日當年接班時
            一樣,服喪三年,並在此期間謀求鞏固權力。 金正恩去年被推舉為僅次於金正日的軍方
            二把手。金正日的妹妹和妹夫張成澤也已被委任軍政要職,作為金正恩的接班監護人,形成
            金家世襲的統治集團。 金正恩1984年1月出生,曾在瑞士首都留學,學習英文、德文和法文。
            金正日去年8月秘密訪問中國時,在長春向中共總書記胡錦濤引見了金正恩,有媒體形容為
            「託孤」。 金正日之死是否引發朝鮮權力鬥爭,外界看法各不相同。遼寧社科院朝韓研究
            中心主任呂超認為,朝鮮很可能會平穩接班,如果權力不能平穩過渡,將會對東北亞局勢
            形成極大的衝擊。 韓國《朝鮮日報》報導,金正日去世後,朝鮮安全人員控制了主要街道,
            集市也被關閉,並封鎖了中朝邊境。中共也向軍隊下達了「一級備戰命令」,以防
            不測。 《中國事務》主編伍凡指出,中共與朝鮮「唇亡齒寒」。 伍凡:「金正日死了那當然
            是個大好的消息啦,對全世界獨裁專制的國家是一個噩耗。現在緊接著就是,中共要對
            朝鮮半島這一個部分它會加強軍事力量的控制,生怕因為金正日死了,那麼金正日這個系統
            全部垮臺,引起社會動亂,再一個,不要讓朝鮮的難民跑到中國來。」 美國總統歐巴馬與
            韓國總統李明博通了電話,重申華盛頓對朝鮮半島穩定的承諾。韓國軍隊已進入緊急戒備
            狀態。日本也成立了有關朝鮮問題的危機處理小組。 美國CNN表示,金正日去世後,朝鮮的
            領導層更換,對於解決朝鮮半島核問題、改善美朝關係可能是一個機會,但也有相當的
            風險。目前,有關各方都在緊張的觀望局勢發展,避免發出錯誤的信號。 《朝鮮日報》報導,
            美朝雙方16號在北京初步達成了協議,朝鮮表示願意接受韓美要求的「先採取無核化措施」,
            也就是中斷鈾濃縮計劃,換取每月2萬噸的糧食援助。 美朝並決定22號在北京舉行第三次
            美朝會談。如果會談取得成果,六方會談有望在明年2、3月左右重啟。但是,金正日突然去世,
            美國官員表示,這些進程很有可能將被推遲。 日本《讀賣新聞》報導,金正恩去年11月曾
            表示,「糧食比子彈重要」,要在3年內讓朝鮮人民吃上白米飯肉湯。香港《動向》雜誌主編
            張偉國指出,金正日的死給朝鮮帶來了變革的契機。 張偉國:「像中國、像朝鮮,如果它的
            政治制度沒有辦法推進這種社會變革的時候,領導人的去世就為這個變革帶來一些機會。
            所以,從這個角度來看,金正日的去世,為朝鮮新的變局帶來機會。」 外界分析,中共擔心
            金正日之死導致朝鮮政權變局甚至垮臺,倒向韓國和美國,最終由韓國主導實現朝鮮半島的
            統一。「後金正日時代」,朝鮮的政治、經濟等各方面的走向,都將對中國社會的轉型產生
            重要影響。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1324310400
    assert parsed_news.reporter == '常春,李元翰,蕭宇'
    assert parsed_news.title == '金正日死後 朝鮮半島契機風險并存'
    assert parsed_news.url_pattern == '2011-12-20-634429'
