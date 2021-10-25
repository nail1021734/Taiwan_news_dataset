import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201807110178.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            世界盃足球賽,比利時相隔32年再度晉級4強,但10日敗給法國失去奪冠機會,這個有3種
            主要語言的國家,人民自己都很難溝通,是足球這個語言提醒他們是「比利時人」。 7月6日
            在俄羅斯喀山體育場,比利時以2比1讓巴西隊打包回家,相距32年再度進入4強,同步收看轉播
            的球迷愛國心大爆發,街上到處有人揮舞國旗,但10日對戰法國失利,最終無法
            進入決賽。 看球賽的人可能會發現,出場時的國歌時間,近乎一半比利時球員沒開口唱國歌,
            這個舉動正是比利時國情的縮影。 比利時因地理位置及歷經多個民族統治,獨立後國內
            主要分為北部的法蘭德斯(Flanders) 的荷語區、南部瓦隆尼亞區(Wallonia)的法語區,
            此外還有一個少數人口的德語區。這3個地區不同的語言造成不同的文化及價值觀,在這裡
            他們是說自己屬於「佛蘭德斯」或「瓦隆尼亞」人,用來凸顯他們文化、甚至政治認同上的
            差異。 這個語言及文化分裂的國家,過去讓世人有不少驚訝之處,例如2010年大選後因沒有
            黨派取得多數,而各黨也不願妥協組成新國會,結果竟有540天處於無中央政府狀態,但比利時
            民眾在各自的荷語區及法語區政府照顧下,照常生活,社會秩序平順。 有人說比利時是
            愛國主義薄弱的國家,以國歌為例,雖有3種語言版本,但據說大多數人不會唱完整首,2007年
            還曾發生一件糗事,當年來自荷語區的準比利時總理勒德姆(Yves Leterme),受訪時把竟
            法國國歌「馬賽進行曲」當做比利時國歌。 連總理都不知道國歌,球員在世足賽沒開口唱
            國歌也就不奇怪了。 此外,這個有3種語言組成的國家代表隊,今年因為許多在國外職業球會
            的球員回國,包括效力於英超曼城後衛孔帕尼(Vincent Kompany)、曼聯中場
            費萊尼(Marouane Fellaini)、切爾西前鋒哈札德(Eden Hazard)、曼聯前鋒
            盧卡庫(Romelu Lukaku)、切爾西門將庫特華(Thibaut Courtois)等,陣容被稱
            為「黃金一代」。 其中有些人只會說一種語言、有些人則會雙語,更衣室內多語並陳,
            但只會法語的人要如何跟說荷語的隊友溝通呢?據英國媒體近日報導,為了統一指揮及不表
            偏袒任何一種語言,球員是以英語為共同語言交談。 本屆世界盃比利時的「黃金一代」球員,
            是歷屆以來實力最被看好,這股期待隨著從32強一路取勝直至敗給法國,過程中匯聚成
            一股打破語言及文化的藩籬的力量,如同一位法語區的女生安恩(Anne)接受中央社訪問時
            強調,正是因為這次有機會拿到好名次,所以荷語、法語區的人一起支持比利時國家隊,
            是足球這個語言,提醒了他們是「比利時人」。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1531238400
    assert parsed_news.reporter == '唐佩君'
    assert parsed_news.title == '特派專欄 一個國家3種語言 足球讓比利時人團結'
    assert parsed_news.url_pattern == '201807110178'
