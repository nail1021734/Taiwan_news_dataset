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
    url = r'https://www.epochtimes.com/b5/20/1/1/n11759265.htm'
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
            1.周曉輝:習發賀詞 2020說新年快樂有些沉重 2019年走過,2020年走來。在這個辭舊迎
            新的日子裡,人們彼此見面時都毫不吝嗇地送上一句「新年快樂」,希望在新的一年中順順
            利利,快快樂樂,平平安安,而最後一天晚上的狂歡也是少不了的。只是祝福終歸是祝福,在
            2020年大陸中國,上至國家、中南海高層,下至普通百姓,真的能做到順利、快樂、平安嗎
            ? 2.華為:生存是2020第一要務 將淘汰10%主管 2019最後一天,華為輪值董事長徐直軍向
            員工和客戶發表新年賀詞。他在致辭中稱,生存將是華為2020的第一要務,10%的主管面臨
            淘汰。 3.歐盟趨強硬 華為:2020生存第一 幾個月前,華為歐盟首席代表劉康
            (Abraham Liu)開始了在布魯塞爾的檯面下運作,試圖鞏固華為在歐洲這個海外最大市場
            的地位。據法媒報導,華為在歐盟的遊說費用高達280萬歐元(約合2185.76萬人民幣),已經
            成了遊說歐盟花費最多的企業之一。 4.川普:1月15日我在白宮簽第一階段協議 週二
            (12月31日),美國總統川普(特朗普)表示,1月15日,美中將在白宮舉行第一階段貿易協議
            簽署儀式,且他會親自參加。隨後他將赴北京討論第二階段協議。 5.韓國瑜連喊三聲
            習主席 其副手不承認習頭銜 台灣國民黨總統候選人韓國瑜,在總統辯論會上連喊三聲習近平
            「主席」,但第二天,其副手、國民黨副總統候選人張善政公開稱,國民黨不承認同「對岸是
            一個國家,更不承認習近平的國家主席頭銜」。 6.2020注定不平凡 9件事
            陪你跨年 回顧2019,發生了太多重大的新聞事件。在2020新年一開始,就有至少5件大事會
            發生。這一系列事件,注定我們跨入的2020新年,使命不凡。 7.山東偷排污水管深埋
            入海口 污染令人震驚 近日,有大陸網民拍攝視頻,披露山東省龍口市的排污管道深埋於
            入海口處偷排污水,污染狀況令人震驚。 8.金言:2019年末 武漢再現驚魂噩夢 2019年
            最後一天,關於「武漢SARS」,「武漢非典」,「武漢不明原因肺炎」的恐怖消息在網上炸開了
            鍋,傳得沸沸揚揚,人心惶惶。今年以來,中國大陸中部大都市武漢的確極其不平靜,暴雨、
            乾旱、流感、地震和不明肺炎等等天災人禍接連不斷來襲,還有在武漢軍運會期間,習近平險
            遭暗殺的消息也不脛而走...... 9.「人權與生俱來」 英巴士公司老闆讚港人抗爭 「
            一百年後,它們都會變成博物館的收藏品,展現它們的影響力,」安迪(Andy Chalkhay)說,
            「這些藝術品表現了香港年輕人他們的剛毅、創意。」 10.「為新的一年帶來希望」神韻
            舊金山首場爆滿 12月30日,美國神韻環球藝術團在舊金山歌劇院
            (War Memorial Opera House)的首場演出爆滿。在新年即將到來之際,人們都想一睹
            享有「世界第一秀」美名的神韻演出,為自己帶來好運。 11.2019陸企違約逾1400億 遍及
            28省 北京最多 今年大陸企業債務被業界稱為「全面違約」,涉及眾多行業,違約債券數量
            接近180隻,金額超過1400億元,遍布28個省級行政區。民企違約最多,但國企引發的震動
            更大。 12.港人感佩法輪功傳真相 恭祝李大師新年好 香港抗爭運動從6月持續至今,在活動
            現場或網上不時會聽到或看到港人向法輪功團體致歉,表示他們以前因低估中共的邪惡程度
            而誤會法輪功,並感謝法輪功學員這些年堅持傳播真相。有港人恭祝李洪志大師新年好
            。 13.中共監控之十大黑科技 高科技本應為人服務,為人民生活帶來便利,但
            中共不遺餘力地發展高技術,用來監控和鎮壓民眾,為中共獨裁統治服務。這種「社會治理
            模式」被稱之為「黑科技」治國。本文盤點2019年中共迅猛發展的十大黑科技。 14.中共
            利用升旗儀式欲染紅費城 華人斥荒唐 中共利用美國憲法誕生地費城支持多元文化的政策,
            數次舉行升旗儀式,並稱其為「紅色延安」。對此,費城市政府反對,當地華人斥其荒唐。 15.
            台陸委會回擊中共:「倒果為因 惡意扭曲」 台灣立法院三讀通過的《反滲透法》,意在阻止
            中共對台灣的滲透、操縱台灣選舉。但此舉遭到中共攻擊,為此台灣陸委會公開回擊:中共
            「純屬倒果為因、惡意扭曲」。
            '''
        ),
    )
    assert parsed_news.category == '大陸新聞,大陸政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1577808000
    assert parsed_news.reporter is None
    assert parsed_news.title == '2020中共面臨「波濤洶湧」'
    assert parsed_news.url_pattern == '20-1-1-11759265'
