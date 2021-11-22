import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.storm


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='風傳媒')
    url = r'https://www.storm.mg/article/600064?mode=whole'
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

    parsed_news = news.parse.storm.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            世足球賽一直是全球矚目的賽事,近年來隨著全民觀看世足賽風氣盛行,也因此昇恆昌有感於
            台灣足球推廣需要挹注更多新動力,今年於世足賽事期間獨家與FIFA合作,捐贈1300顆
            2018 FIFA紀念足球給予桃園市足球隊,同時為機場打造賽事直播、趣味互動射門體驗及
            公共藝術等裝置,讓台灣機場充滿濃厚的世足熱血氛圍。 今年也特別邀請「台灣隊長」
            陳柏良擔任昇恆昌年度公益大使,同時贊助此次「2018 BE HEROES國際高中足球四校
            邀請賽」,於11月5日於台北市太平國小舉辦「昇恆昌助夢想起飛 陳柏良足球公益分享會」,
            活動安排陳柏良足球經歷分享、有獎徵答及熱血友誼賽,活動結束後更帶領小球員們參與
            「2018 BE HEROES國際高中足球四校邀請賽」記者會,記者會上F.C.Vikings球隊也代表
            太平國小、重慶國中及大理高中,感謝昇恆昌及陳柏良一直以來為足球推廣努力頒贈
            感謝狀。 世足熱潮再台灣掀起一陣熱潮,昇恆昌身為國門的第一線,今年世足賽期間與國際
            足球總會獨家(FIFA)合作,為了帶給台灣機場來往百萬的旅客感受全方位的世足熱情氣氛,
            設置數十台大型電視直播及轉播世足賽事不間斷,讓旅客不會錯過任何一場精采賽事,
            並展出各式足球及以2018 FIFA紀念足球組成巨型足球牆,成為國內外旅客熱門拍照打卡
            勝地,更打造體感互動裝置,讓搭機旅客能夠親自體驗屬於足球射門的魅力及快感,也感受到
            屬於台灣的足球熱情與創意。 此次昇恆昌更特別準備足球作為有獎徵答獎勵,獲得獎勵的
            小球員表現的欣喜若狂,並安排了一場與台灣隊長難得的友誼賽,可以同時感受與台灣隊長
            同隊及競爭時不可多得的難忘經驗,分享會結束之後也帶領小球員們參與
            「2018 BE HEROES國際高中足球四校邀請賽」記者會,讓小球員們見習賽事記者會的
            浩大場面,記者會現場 F.C.Vikings球隊為感謝昇恆昌一直以來為足球推廣不遺餘力,
            特別代表太平國小、重慶國中及大理高中頒贈感謝狀給予昇恆昌及陳柏良。
            '''
        ),
    )
    assert parsed_news.category == '國內,運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1541387340
    assert parsed_news.reporter == '余柏翰'
    assert parsed_news.title == '陳柏良參與足球分享會 積極投入扎根計畫'
    assert parsed_news.url_pattern == '600064'
