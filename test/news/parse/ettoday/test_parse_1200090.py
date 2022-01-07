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
            在影集《冰與火之歌:權力遊戲》飾演重要角色「北境之王」Jon Snow的英國演員
            基特哈靈頓Kit Harington,與交往五年訂婚的同劇演員蘿絲萊斯莉Rose Leslie,於
            6月23日於蘇格蘭亞伯丁郡完婚。 同劇演員龍后Emilia Clarke、珊莎Sophie Turner與
            艾莉亞Maisie Williams等人皆到場祝福,同時齊聚其他好萊塢名人及親友。身穿
            Elie Saab婚紗的Rose Leslie與父親攜手走入教堂,證婚儀式後小倆口接受眾人撒花
            祝福,留下甜蜜的美好畫面。 婚禮賓客:蘇菲透納Sophie Turner 婚禮前一天便抵達
            蘇格蘭的「珊莎」蘇菲透納Sophie Turner,於機場以一身輕便運動服裝現身。戴著墨鏡的
            她,邊走邊以手機視訊。 蘇菲透納Sophie Turner & 梅西威廉斯Maisie Williams 婚禮
            當天,這對史塔克(Stark)家族的高人氣姐妹花以相應的配色一同出席。Sophie Turner
            穿著大紅西裝外套搭配黑色高筒靴,戴著眼鏡的Maisie Williams則以黑色連身褲配上亮紅
            高跟鞋。 梅西威廉斯Maisie Williams 21歲的Maisie Williams以連身褲與手拿包的
            搭配,展現得體卻又不失個人風格的婚禮賓客穿搭。 約翰布拉德利John Bradley、喬丹普斯
            Joe Dempsie、班克朗普頓Ben Crompton 在劇中飾演Kit Harrington好兄弟山姆
            威爾(Samwell Tarly)的英國演員John Bradley,與「詹德利」Joe Dempsie、
            「守夜人」Ben Crompton一同出席。 班克朗普頓Ben Crompton 換下打鬥的鎧甲與
            守夜人皮草,婚禮上的西裝打扮令人看見演員們的另一面! 彼得汀克萊傑
            Peter Dinklage & 艾蜜莉亞克拉克Emilia Clarke 近日剛結束所有 《冰與火之歌》
            角色戲分的「龍后」Emilia Clarke,以俏麗短髮與粉色系裙裝出席。 彼得汀克萊傑
            Peter Dinklage 角色粉絲不少的「小惡魔」Tyrion Lannister演員
            Peter Dinklage,也穿著西裝搭配灰色領帶現身。 連恩康寧漢Liam Cunningham 飾演
            Sir Davos的愛爾蘭演員連恩康寧漢Liam Cunningham,黑西裝搭配的綠領帶更顯
            搶眼。 傑克唐納利Jack Donnelly & 瑪琳艾珂曼Malin Akerman BBC
            影集 《Atlantis》男主角Jack Donnelly與 《毀滅大作戰》女星
            Malin Akerman。 英國樂團成員Marcus Mumford 英國民謠搖滾(Folk Rock)樂團
            Mumford & Sons團長Marcus Mumford。 新郎基特哈靈頓Kit Harington 身為今天
            婚禮主角,現年31歲的新郎Kit Harington以英倫紳士風情的三件式西裝亮相。 新娘
            蘿絲萊絲莉Rose Leslie 新娘蘿絲萊絲莉Rose Leslie在
            父親Seb的陪同下現身。全程洋溢笑容的她,亦不忘對場外圍觀的民眾打招呼。選擇的
            Elie Saab純白蕾絲洋裝,細緻的透視細節搭配白色花朵頭飾,清新、優雅,又不帶有過度的
            距離感。於教堂內的結婚儀式結束後,新娘與新郎接受眾人撒花祝福,慶賀正式結為
            夫妻。 ​蘿絲萊絲莉Rose Leslie​ & 基特哈靈頓Kit Harington 新娘Rose Leslie為
            Kit Harington撥下頭髮上的花瓣。走過眾人環繞的通道後,這對新人坐上吉普車離開教堂,
            繼續後續的婚宴準備。全程帶著笑容,從照片中便能感受到整場婚禮的幸褔氛圍——祝福這對新人!
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530083820
    assert parsed_news.reporter is None
    assert parsed_news.title == '《冰與火之歌》劇組大集合!基特哈靈頓、蘿絲萊斯莉古堡浪漫完婚'
    assert parsed_news.url_pattern == '1200090'
