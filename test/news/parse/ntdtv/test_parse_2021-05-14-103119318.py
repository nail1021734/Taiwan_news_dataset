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
    url = r'https://www.ntdtv.com/b5/2021/05/14/a103119318.html'
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
            以色列和加沙衝突不斷升級,以色列猶太人和阿拉伯人之間頻爆內亂,以色列的政治局勢
            或發生戲劇性的轉變,總理內塔尼亞胡(Benjamin Netanyahu)的主要政治對手
            拉皮德(Yair Lapid)計劃推翻內塔尼亞胡,組建新政府的努力受到嚴重打擊。 以色列總統
            5月5日宣布,正式授權中左翼政黨「擁有未來」黨領導人拉皮德組建新政府。在本週
            巴以衝突爆發之前,已擔任總理12年的內塔尼亞胡似乎即將失去他在以色列政治中的
            權威地位。 拉皮德和右翼政治人物貝內特(Naftali Bennett)輪流擔任總理
            的「輪換」協議已經提出。在拉皮德輪換上任之前,貝內特將任兩年總理。除了貝內特
            ,拉皮德還需要阿拉伯議員的支持才能獲得議會多數。 但在與加沙的戰鬥以及以色列境內
            猶太人與阿拉伯人之間的衝突中,貝內特週四(13日)宣布,替代政府已不在考慮之列,並表示
            他將與內塔尼亞胡就潛在的右翼政府進行談判。 貝內特列舉了包括有以色列公民和
            阿拉伯公民的城市的「緊急狀況」,這「要求使用武力並派軍隊進入城市」,但這在
            阿拉伯政黨領導人所支持的政府中是不可能發生的。 與此同時,內塔尼亞胡正在加強他的
            聲譽。作為與巴勒斯坦激進份子強力對抗的領導人,內塔尼亞胡表示,要給哈馬斯以致命的
            打擊,全力以赴的保護以色列不受外部敵人和內部暴亂者的影響。 以色列-加沙的跨境戰鬥
            伴隨著來自以色列境內猶太人和阿拉伯人混合社區的暴力。猶太教堂遭到襲擊,街頭鬥毆
            事件頻發,以色列總統甚至發出內戰警告。 在以色列總統給拉皮德的28天授權中,拉皮德
            還有3週時間嘗試組建一個執政聯盟,在這段時間裏,如果能得到120名議員中的61名的
            支持,他就可以組建新政府。 以色列政治評論家認為,拉皮德取得成功的可能性很小。如果
            他失敗了,有可能會舉行新的選舉,這將是以色列兩年來的第5次選舉。 在此期間,預計
            內塔尼亞胡將試圖通過一項法律來改變選舉制度,以允許總理經直接選舉產生。
            '''
        ),
    )
    assert parsed_news.category == '國際,時政'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1620921600
    assert parsed_news.reporter == "李昭希,李佳"
    assert parsed_news.title == '巴以衝突加內亂 內塔尼亞胡有望保住政治地位'
    assert parsed_news.url_pattern == '2021-05-14-103119318'
