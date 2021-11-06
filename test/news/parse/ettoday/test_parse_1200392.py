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
    url = r'https://star.ettoday.net/news/1200392'
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
            其實紅酒不光是飲品,也代表了社會地位,生活品味。所以很多人會假裝自己會喝紅酒,但是
            懂紅酒的人馬上就能發現這些破綻。在喝酒之前,先看看這幾件關於紅酒的事,不要被別人
            發現你在不懂裝懂,當一個真正懂酒,品酒的人吧。 1.喝酒時不一定要點評 喝一口酒,抿一
            抿,再點評一句「Dry or Bitter」。似乎成為喝紅酒的標準流程,其實這樣只會彰顯你不懂
            酒,因為你不見得知道紅酒的甜度和單寧。且喝酒其實是享受,不需要一直說話,所以下次喝
            酒不妨安靜一會,好好品味真正的紅酒。 2.侍者倒完酒,我該做什麼? 到高級餐廳的各位應
            該都會遇到侍者對你倒酒,倒了一點後就微笑看你。想必你不知道自己該做什麼來回應他。
            80%的人選擇微笑回應,並且喝一口來彰顯自己的氣質。而萬萬沒想到的是,這樣做是在浪費
            大家的時間。因為侍者做出這個動作其實是代表酒是新開的,且需要一段時間與空氣作用來
            「醒酒」。 這時候真正的作法是聞一下酒的氣味,並且淺嘗一口有沒有腐壞,接下來就可以
            示意侍者繼續倒酒,完成倒酒步驟。 3.喝紅酒一定要配冰塊? 這個爭議存在已久,其實紅酒
            裝瓶出廠後,一切就像是釀酒師已經做好了原廠設定,擁有自身的屬性,包括香味、色澤、口
            味。如果飲用時加冰塊,會稀釋紅酒的濃度,也就失去了釀酒師原本精心調配的比例。 下次
            喝酒可以先將酒,由酒櫃降溫至攝氏18度,開瓶後慢慢品嚐讓溫度回升到室內溫度,這樣最容
            易感官到酒體的變化。 4.不要聞軟木塞 相信大家或多或少都有聞過軟木塞,其實這是沒有
            意義的動作,因為你不僅聞不出酒的風味,而且只會彰顯你不懂紅酒。真正遇到餐廳遞給你
            軟木塞時,只要觸摸底部是否有潮濕,來判斷紅酒的存放方式正確與否,隨後就可以結束這個
            過程,真的不需要聞軟木塞。 5.搖晃酒杯的意義 沒喝過紅酒至少也看過搖晃酒杯的動作,
            大多數人晃完酒杯然後看著杯子,腦海中其實什麼事情也不知道,卻流露一副專業人士的模
            樣。而搖晃紅酒讓它滑落杯壁的動作叫做「淚腳」(Tears / Legs),通過觀察「淚腳」的持
            續時間來判斷紅酒的濃度,「淚腳」越多,酒精濃度越高。 但是其實現在很多常見紅酒的濃
            度都在 12 到 16 度之間,「淚腳」都會十分明顯,因此這個動作是沒有太大的意義。
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530086940
    assert parsed_news.reporter == 'Ann'
    assert parsed_news.title == '喝紅酒時晃酒杯、聞軟木塞 這5種動作洩露你不懂酒還裝懂'
    assert parsed_news.url_pattern == '1200392'
