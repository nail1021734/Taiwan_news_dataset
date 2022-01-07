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
    url = r'https://www.epochtimes.com/b5/13/12/7/n4028971.htm'
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
            美國官員表示,85歲的美國老兵梅裡爾•紐曼(Merrill Newman)被朝鮮獲准離境後踏上
            返回美國的途中。根據朝鮮中央通信社(KCNA)報導,朝鮮政府考慮到紐曼「真誠的悔過書」
            以及他的年齡和健康狀況, 出於「人道主義的立場」,做出了這個決定。 在平壤宣佈這個
            消息的當天,美國副總統拜登(Joe Biden)正在對韓國進行訪問,韓國是拜登此次亞洲三國行
            的最後一站,此前他已對日本和中國進行了訪問。 在本週六(12月7日)前往韓朝邊界
            非軍事區的途中,拜登對朝鮮此舉表示歡迎,不過他也向平壤政府發出敦促,希望後者
            能夠釋放另外一名美國人——45歲的美籍傳教士裴俊浩(Pae Jun Ho/美國名Kenneth Bae)。
            裴俊浩去年被朝鮮當局逮捕,今年3月,他被以從事敵對行動為名判處15年勞教。 拜登稱,對
            裴俊浩的監禁「無任何理由」,要求朝鮮方面「應立即釋放」裴俊浩。來自加州的紐曼患有
            心臟方面的疾病。今年,他作為旅遊團成員進入朝鮮境內,根據他家人的介紹,在10月紐曼結
            束觀光準備乘坐飛機從朝鮮飛往北京時,在航班起飛前被帶下飛機。 回家過聖誕 拜登的辦
            公室透露副總統已與紐曼通過電話。紐曼在北京機場接受媒體採訪時表示自己:「很高興能
            回家了......想見到妻子。」 從在北京機場拍攝的照片上,紐曼看來起來很健康。 美國國
            務院發言人哈夫(Marie Harf)在一份聲明中說:「我們很高興地看到紐曼先生被允許離開朝
            鮮並與家人團聚。」她還呼籲平壤釋放裴俊浩,「顯示人道主義姿態,讓他也可以與家人團
            聚。」 裴俊浩的家人在一份聲明中也對紐曼獲釋的消息表示歡迎:「我們一直在為他祈禱,
            很高興他能與家人共渡聖誕假日。......我們相信,我們的裴俊浩也會儘快
            回到家裏。」 韓國外交部對朝鮮允許紐曼離境的決定表示歡迎。首爾的分析人士指出,平壤
            此舉是力圖促進與華盛頓展開對話。首爾東國大學教授金永鉉(Kim Yong-Hyun)向法新社
            表示:「朝鮮清楚,扣下一個生病的老人會惡化朝鮮和美國的關係。」他還補充說;「釋放
            紐曼反映了平壤希望促進與華盛頓對話的意圖。」 上個星期,朝鮮首次正式承認扣留紐曼,
            表示其「假扮觀光客」,入境之後從事「敵對行為」。朝鮮稱,紐曼在1950至1953年的朝鮮
            戰爭期間參與殺害平民的行動,而且進行間諜活動。 「道歉視頻」 紐曼是一位退休財務
            顧問。朝鮮之前公佈了一段紐曼表示懺悔和道歉的視頻片斷。在這段錄像中,紐曼身穿藍色
            襯衫和淺色、有些皺紋的褲子宣讀了標注日期為2013年11月9日的道歉書。 平壤方面聲稱,
            紐曼此行打算要會見當年的「倖存戰友,並告慰死去戰友的靈魂」。 朝鮮當局是世界上
            最不透明的政府之一,獨立核實官方報導非常困難。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386345600
    assert parsed_news.reporter == '周雅'
    assert parsed_news.title == '美老兵「朝鮮歷險記」終畫句點 拜登道賀'
    assert parsed_news.url_pattern == '13-12-7-4028971'
