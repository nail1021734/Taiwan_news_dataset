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
    url = r'https://star.ettoday.net/news/1200511'
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
            自2015年起,統一7-ELEVEn獅隊持續以主題式特別企劃規劃球季行銷活動,豐富多元的活動
            內容搭配獨家主題商品,讓球迷每一年都有不同的驚喜,不但保留受歡迎的經典特色主題,也
            不斷在跨領域的異業結合有所突破,希望能夠讓球迷進場看球之餘,也可以感受到更多屬於
            棒球場的無限魅力與可能性。 職棒29年上半季統一獅主場活動推出,「OPENING DAY台南主
            場開幕戰」結合「大餅林岳平引退儀式」揭開序幕,緊接著是最適合親子同樂的
            「CARTOON & BASEBALL DAY卡通明星瘋棒球」,結合台南在地獨立音樂能量的
            「SWING TAINAN搖擺府城」,以及由女孩擔任主角,每年都不能缺少的重要企劃
            「GIRLS‘ POWER最強女孩」,滿滿的活動企劃等著你進場體驗猛獅主場魅力,每檔活動均
            獲得球迷好評及迴響,尤其六月份首度推出女孩粉紅球衣也造成球迷搶購熱潮。 下半球季
            將於7月11日新莊棒球場熱鬧開打,首週7/14-15延續與埼玉西武獅合作,推出雙獅交流
            主題日活動,而八月主題賽事,統一獅球隊取得円谷製作授權合作,將於8/4、5台南棒球場及
            8/18、19天母棒球場舉辦「超人力霸王X統一獅棒球聯名主題活動」。 9/1及2高雄澄清湖
            主場賽事,球隊將與FOX體育台舉辦棒球派對。 9/16推出Uni Girls女孩日,全部UG女孩將
            和球迷玩在一起。9月22日今年度例行賽最後一場週六賽事,將舉辦JAX劉芙豪榮耀
            引退賽。而9月23日為本季例行賽最終場,同樣賽後推出草地音樂會,回饋球迷到台南棒球場
            聽聽獅王好聲音。本週五、六、日連續三天,將開放統一獅VIP會元優先購票,下週一
            (7/2)將開放一般購票,目前雙獅主題日套票熱賣中,截止至今日已經售出兩千多套,如果
            不想錯雙獅主題日套票球迷,剩下最後兩天,明日晚上23:29截止販售。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530088440
    assert parsed_news.reporter is None
    assert parsed_news.title == '統一下半季主題日!9月底劉芙豪引退後草地音樂會'
    assert parsed_news.url_pattern == '1200511'
