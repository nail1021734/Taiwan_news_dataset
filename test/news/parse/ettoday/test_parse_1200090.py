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
    url = r'https://star.ettoday.net/news/1200090'
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
            在影集《冰與火之歌:權力遊戲》飾演重要角色「北境之王」Jon Snow的英國演員基特哈靈
            頓Kit Harington,與交往五年訂婚的同劇演員蘿絲萊斯莉Rose Leslie,於6月23日於
            蘇格蘭亞伯丁郡完婚。 同劇演員龍后Emilia Clarke、珊莎Sophie Turner與艾莉亞
            Maisie Williams等人皆到場祝福,同時齊聚其他好萊塢名人及親友。身穿Elie Saab婚紗
            的Rose Leslie與父親攜手走入教堂,證婚儀式後小倆口接受眾人撒花祝福,留下甜蜜的美好
            畫面。 婚禮賓客:蘇菲透納Sophie Turner 婚禮前一天便抵達蘇格蘭的「珊莎」蘇菲透納
            Sophie Turner,於機場以一身輕便運動服裝現身。戴著墨鏡的她,邊走邊以手機視訊(畫面
            顯示對象為未婚夫喬強納斯Joe Jonas)。 蘇菲透納Sophie Turner & 梅西威廉斯
            Maisie Williams 婚禮當天,這對史塔克(Stark)家族的高人氣姐妹花以相應的配色一同
            出席。Sophie Turner穿著大紅西裝外套搭配黑色高筒靴,戴著眼鏡的Maisie Williams
            則以黑色連身褲配上亮紅高跟鞋。 梅西威廉斯Maisie Williams 21歲的
            Maisie Williams以連身褲與手拿包的搭配,展現得體卻又不失個人風格的婚禮
            賓客穿搭。 約翰布拉德利John Bradley、喬丹普斯Joe Dempsie、班克朗普頓
            Ben Crompton 在劇中飾演Kit Harrington好兄弟山姆威爾(Samwell Tarly)
            的英國演員John Bradley(左),與「詹德利」Joe Dempsie、「守夜人」Ben Crompton
            一同出席。 班克朗普頓Ben Crompton 換下打鬥的鎧甲與守夜人皮草,婚禮上的西裝打扮
            令人看見演員們的另一面! 彼得汀克萊傑Peter Dinklage & 艾蜜莉亞克拉克
            Emilia Clarke 近日剛結束所有 《冰與火之歌》角色戲分的「龍后」Emilia Clarke,
            以俏麗短髮與粉色系裙裝出席。 彼得汀克萊傑Peter Dinklage 角色粉絲不少的
            「小惡魔」Tyrion Lannister演員Peter Dinklage,也穿著西裝搭配灰色領帶
            現身。 連恩康寧漢Liam Cunningham 飾演Sir Davos的愛爾蘭演員連恩康寧漢
            Liam Cunningham,黑西裝搭配的綠領帶更顯搶眼。 傑克唐納利
            Jack Donnelly & 瑪琳艾珂曼Malin Akerman BBC影集 《Atlantis》男主角
            Jack Donnelly與 《毀滅大作戰》女星Malin Akerman。 英國樂團成員
            Marcus Mumford 英國民謠搖滾(Folk Rock)樂團Mumford & Sons團長
            Marcus Mumford。 新郎基特哈靈頓Kit Harington 身為今天婚禮主角,現年31歲的
            新郎Kit Harington以英倫紳士風情的三件式西裝亮相。 新娘蘿絲萊絲莉
            Rose Leslie 新娘蘿絲萊絲莉Rose Leslie在父親Seb的陪同下現身。全程洋溢
            笑容的她,亦不忘對場外圍觀的民眾打招呼。選擇的Elie Saab純白蕾絲洋裝,細緻的透視細
            節搭配白色花朵頭飾,清新、優雅,又不帶有過度的距離感。於教堂內的結婚儀式結束後,新
            娘與新郎接受眾人撒花祝福,慶賀正式結為夫妻。 ​蘿絲萊絲莉Rose Leslie​ & 基特哈靈頓
            Kit Harington 新娘Rose Leslie為Kit Harington撥下頭髮上的花瓣。走過眾人環繞
            的通道後,這對新人坐上吉普車離開教堂,繼續後續的婚宴準備。全程帶著笑容,從照片中便能
            感受到整場婚禮的幸褔氛圍——祝福這對新人!
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530083820
    assert parsed_news.reporter is None
    assert parsed_news.title == '《冰與火之歌》劇組大集合!基特哈靈頓、蘿絲萊斯莉古堡浪漫完婚'
    assert parsed_news.url_pattern == '1200090'
