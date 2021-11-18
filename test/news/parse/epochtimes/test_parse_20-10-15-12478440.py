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
    url = r'https://www.epochtimes.com/b5/20/10/15/n12478440.htm'
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
            湖北省十堰市的李小燕發現,當地政府在多年前用她的名義辦了低保,但她一直不知情,也沒
            領過一分錢。為此,她近日到湖北省信訪局上訪,卻被當地公安抓回,關進精神病院
            。 知情者、十堰市訪民汪素華告訴大紀元,李小燕的丈夫原本是襄陽市某郵政所所長
            。2014年,丈夫因醫療事故死亡,整個家庭的命運發生了巨變。 他們的女兒為父親的事上訪
            ,結果在2017到2018年間被襄陽市公安局關押一年多。期間她受到驚嚇,現在不敢和任何人
            聯繫,也不敢接陌生男子的電話,無業在家。 由於母女倆都沒有工作,李小燕就去申請低保
            。「在報低保的時候,不知道是哪個地方(部門)發現:欸,你有低保啊。就這樣一查,她才知道
            。」汪素華說。 原來多年前,李小燕在老家十堰市房縣青峰鎮的土地被當地政府徵用。當時
            鎮政府沒給出相應的賠償金,只是以辦理低保的方式給予被徵地者補償。然而,李小燕從未
            被告知這件事,當時家庭條件良好的她也未曾留意。 汪素華說,「報了多少年的低保她
            沒拿到過一分(錢)。」「肯定是政府報了她低保,她不知道,給別人吃唄,他們自己貪了唄
            。」 於是,李小燕開始逐級上訪到湖北省信訪局。「不知道是17年還是18年,(省裡)就給
            她發了一個答覆意見,叫她找他們當地青峰政府要,但她回去了一直都沒給她,一年多不給她
            。」汪素華說,「他們一直,推什麼疫情啊,疫情過後又推到10月份。到10月份了,她又找
            他們,青峰不管。」 「有一天晚上我和她聊天,我說怎麼樣啊,十一後他們上班了。她說:
            他們騙我,騙我我就到省裡去上訪,上班了我就去。」 10月11日晚,李小燕坐夜車前往
            武昌火車站,12日早晨到站後再去省信訪局。當天下午,她被青峰派出所攔截,連夜押送回當
            地。 汪素華表示,李小燕在10月13日早上10點左右給她打了個電話,告知自己被關到派出所
            ,且被抓後一直不給飯吃,也不被允許她自己買飯。 下午6點多鐘,李小燕再次給汪素華
            打電話。「她說,『汪姐,你救救我呀,他們已經給我拿到精神病院裡來了,我好好一人,他們
            要當精神病治療。』就說了這幾句話,我只聽到他們可能要把她按倒,也不知道(或是)
            捂住她的嘴,她就一瞬間就(說),『哎呀,我沒有精神病吶,你憑啥子給我打針?』那個
            『針』字都還沒有說出來,就任何聯繫都沒了。」 汪素華隨後給李小燕連撥3個電話,都
            撥通無人接聽,再打第4個電話,已經提示關機。李小燕的女兒和八十多歲的父母得知後
            一直痛哭,希望外界能搭手相救。 14日下午5點過後,記者多次撥打李小燕電話,都處於關機
            狀態。 汪素華確認李小燕精神沒有任何問題,連聲說她是「好好的人,好好的人」
            。她也擔心如果李被長期打治療精神病的針,「沒有精神病也會打出精神病來」。
            '''
        ),
    )
    assert parsed_news.category == "大陸新聞,中國人權"
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1602691200
    assert parsed_news.reporter == "張北"
    assert parsed_news.title == '湖北十堰政府貪污低保 民眾維權被關精神病院'
    assert parsed_news.url_pattern == '20-10-15-12478440'
