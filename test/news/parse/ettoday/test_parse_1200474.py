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
    url = r'https://star.ettoday.net/news/1200474'
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
            暑假即將在下周開始,漫長的暑假學校營養午餐也放假,新竹市政府看見弱勢家戶孩童
            暑假餐食的需要,持續透過「愛心福利社」、「社區愛享冰箱」及「呷熊飽」「早安!飽貝
            」餐食券3個方案,支持著有需要的家庭,新竹市長林智堅表示,市府3大用心撐起愛的保護傘
            ,期盼讓弱勢家庭免於餐食煩惱。 林智堅表示,市府團隊因為看見弱勢家庭的多元需求,也
            感受到臨時陷困民眾需要伸手拉一把的救援, 105年整合「呷熊飽」及「早安!飽貝」餐食
            補助,106年成立愛心福利社,並且推動設立6個社區愛享冰箱,整合各界愛心資源,藉由提供
            不同的餐食選擇,讓弱勢家庭可以依照需求、自主選擇需要的物資,並且更進一步為提升福
            利可近性,這樣的愛心服務接力賽一棒傳一棒,累計服務超過10萬人次。 年僅13歲的琪琪(
            化名),一出生爸爸就離家出走,媽媽邊做清潔工邊把琪琪及小他3歲的弟弟祥祥(化名)帶大,
            琪琪的媽媽為了能夠賺更多的錢養家活口,兼職2份清潔工作,往往一早不到七點就出門,直
            到晚上七八點才回來,所以姊弟倆每天早上都是自己起床,啃著前一天媽媽放在桌上的白吐
            司,再去學校上學;而學校的營養午餐則是一天中最期待最豐盛的一餐,因為只有這一餐可以
            盡情的吃飽。由於租屋處沒有瓦斯爐等設備,無法烹煮食物,所以晚餐是外帶便當回家。因
            為家中經濟不寬裕,常常是三個人吃兩個人份的便當。 最近琪琪的媽媽因為擦窗子爬高摔
            傷,以致手骨折無法工作,家中頓失經濟來源,三餐不繼,更令人擔心的是暑假即將來臨,沒有
            學校的營養午餐,熱心的里長把琪琪一家人的情形告訴社會處社工,社工員家訪了解後,提供
            琪琪一家人餐食券,讓琪琪一家人可以持餐食券,就近在便利商店、麵包店、早餐店及便當
            店,兌換熟食與便當,獲得基本溫飽,也提供愛心福利社的愛心福利卡,讓琪琪一家人可以兌
            換日常需要的民生用品,還有罐頭、八寶粥、乾糧及保久乳等可以存放較久的食品。琪琪的
            媽媽表示,雖然現在手受傷,清潔工作也沒了,但還好有社工員的陪伴以及餐食券與愛心福利
            社等資源,協助她度過人生的低潮,她相信一切都會越來越好。 新竹市社會處代理處長魏幸
            雯表示,「愛心福利社」、「社區愛享冰箱」及「呷熊飽」「早安!飽貝」餐食券3個支持方
            案,除了可以減輕弱勢家庭的負擔,也更為全面照顧本市需要民眾,從餐券的兌換、實體愛心
            福利社店面的物資選購到社區式的服務輸送,6個分享續食的社區愛享冰箱,已分享超過
            17,823公斤食物,服務超過86,884人次,而愛心福利社及「呷熊飽」及「早安!飽貝」餐食補助,
            累計服務18,559人次。 新竹市社會處表示,感謝各界愛心串連,讓我們的寶貝可以平安無憂
            長大,也呼籲市民朋友多多關心社區鄰居及學童生活狀況,若有發現身旁有學童或鄰居三餐
            不繼或生活困難,需要餐食券、物資等協助者,請聯繫社會處,讓社工員評估家庭狀況,社工
            員會儘速結合本市資源,讓弱勢家庭與學童的獲得基本生活穩定。
            '''
        ),
    )
    assert parsed_news.category == '地方'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530096180
    assert parsed_news.reporter == '蔡文綺'
    assert parsed_news.title == '竹市「3個愛的保護傘」 守護弱勢童暑假餐食'
    assert parsed_news.url_pattern == '1200474'
