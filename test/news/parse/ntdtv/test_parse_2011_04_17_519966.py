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
    url = r'https://www.ntdtv.com/b5/2011/04/17/a519966.html'
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
            星期天(4月17日),利比亞反政府軍和卡扎菲軍在東部重鎮艾季達比耶附近的戰鬥更加激烈。
            反政府軍一直試圖向數十公里外的石油重鎮佈雷加推進。 卡扎菲軍用火箭攻擊了
            艾季達比耶城外的反政府軍,目擊者說10余枚火箭轟炸了該城的西部通道. 在城市東門附近的
            路透社記者聽到城內的多處爆炸聲。 一天前,這座城市以西的戰鬥造成至少7人死亡,27人
            受傷。雙方在該市的激戰已持續數週。 反政府軍一直在向距離艾季達比耶80公里的佈雷
            加推進,想奪回這個石油重鎮。卡扎菲軍連日來一直轟炸從艾季達比耶通往佈雷加的公路,
            造成多名反政府軍傷亡。 艾季達比耶這個曾經擁有10萬人口的繁華城市,如今在戰火之下,
            大部分民眾逃離,成了一座鬼城。 卡扎菲部隊被指使用違禁集束炸彈攻擊反對派陣營 米蘇拉塔
            這個長期遭圍困城鎮,近日再度遭到猛烈攻擊。米蘇拉塔居民柴德(Hazam Abu Zaid)形容
            指出,昨晚集束炸彈「象雨般落下」。 集束炸彈也稱“子母彈”,炸彈在空中爆炸後,散射出
            足以穿透裝甲車的殺傷力極強的數百枚小炸彈,並在碰擊地面時爆炸。集束炸彈爆炸後的碎片,
            可以在足球場大小的範圍內產生巨大殺傷力,而落地後沒爆炸的小炸彈則成為當地安全的
            長期隱患。因集束炸彈破壞性極強,已經被世界上1百多個國家禁止使用。 利比亞政府今天
            否認卡扎菲(Moamer Kadhafi)的部隊動用國際社會禁用的集束炸彈,來對付米蘇拉塔
            (Misrata)的反抗軍。 總部設在美國的人權團體「人權觀察」(HumanRights Watch)說,
            它的調查人員報告指出,卡扎菲部隊使用國際社會禁用的集束炸彈轟炸米蘇拉塔。米蘇拉塔是
            反抗軍位於利比亞西部的主要大本營。 法國外長居貝(Alain Juppe)昨天表示,不需要新的
            聯合國決議來逼迫利比亞領導人下台;德國經濟部長布魯德爾(Rainer Bruederle)建議把
            已凍結的利比亞資產移交給聯合國,用來援助衝突中受害者。 卡扎菲軍使用違禁集束炸彈
            攻擊 星期六(4月16號),人權觀察指出,有證人和證據確認,卡扎菲軍在攻擊米蘇拉塔時,
            使用了已經被1百多個國家禁止使用的集束炸彈。當天,利比亞至少有三個城市發生了激烈的
            戰鬥。 週六(4月16號),總部設在紐約的人權觀察表示,該組織的一名攝影師在米蘇塔拉,
            看到利比亞軍朝居民區,至少發射了3枚集束炸彈。而從殘片中,能看出炸彈是西班牙製造
            的。 與此同時,米蘇塔拉醫院的醫生說,在卡扎菲軍炮擊後,有很多人被彈片擊傷住院,其中
            大部分是平民。 隨着卡扎菲軍包圍時間的延長,米蘇塔拉的生活條件持續惡化。目擊者表示,
            緊密的炮擊造成大部分城市被遺棄,在停水停電中,數百戶家庭被迫擠在一起生活。 在東部的
            艾季達比耶,卡扎菲軍和反對派軍發生了激烈衝突,據報,反對派軍奪取了通向佈雷加的一些
            陣地。 集束炸彈也稱“子母彈”,炸彈在空中爆炸後,散射出數百枚小炸彈,並在碰擊地面時
            爆炸。集束炸彈爆炸後的碎片,可以在足球場大小的範圍內產生巨大殺傷力,而落地後沒爆炸的
            小炸彈則成為當地安全的長期隱患。因集束炸彈破壞性極強,已經被世界上1百多個國家禁止使用。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1302969600
    assert parsed_news.reporter == '王晨光,任浩'
    assert parsed_news.title == '艾季達比耶激戰 利反政府武裝向石油重鎮推進'
    assert parsed_news.url_pattern == '2011-04-17-519966'
