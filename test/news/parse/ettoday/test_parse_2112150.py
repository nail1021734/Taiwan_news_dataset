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
    url = r'https://star.ettoday.net/news/2112150'
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
            台北市刑大一陳姓特勤警員,9月23日因精神狀況赴醫院就診,當晚疑似因情緒失控,在大街
            上搶奪林姓外送員餐點後逃逸,事後雖向當事人談和解卻遭質疑態度不佳。北市議員洪健益
            今召開記者會怒轟市警局,北市刑大回應,現已依法處理並向當事人表達歉意,全案於15日
            移送士林地檢署偵辦,並列輔導對象。 洪健益29日陪同該名外送員召開記者會。外送員回憶,
            9月23日深夜騎車送餐時,突然發現遭一男子尾隨,自稱要取餐,他認為有異,男子忽然伸手
            搶餐點,且被對方壓制,雙方發生拉扯。過程中,對方曾出示公務員證件及表明員警身分,他
            趁隙傳簡訊給點餐民眾,才順利脫困,男子搶奪餐點後離去,他當晚就向轄區派出所
            報案。 「為何人民保母變成搶劫犯?」外送員表示,回想起當晚的情況,至今仍心有餘悸。
            外送員說,北市刑警大隊隔天晚間通知前往洽談,才發現搶奪餐點的是員警;且案發約1個月
            後,才被知會前往洽談和解,但一直被對方律師要求簽和解書,動手搶餐的員警卻在一旁吃
            鹽酥雞,一句道歉都沒有,他感到不解。 陪同陳情人召開記者會的洪健益怒批,該員警的行為
            已涉及刑法重罪,嚴厲譴責,要求北市警開除警界毒瘤,畢竟特勤員警平時負責重大維安,這種
            不定時炸彈若留在北市,後果恐不堪設想。 北市刑警大隊長蔡燕明表示,該員警因身體不適,
            案發當天請假就醫,深夜搭計程車時突然下車攔阻外送員;案發後除把員警強制送醫外,並
            列為關懷輔導對象,至於懲處部分,將依人事法規處理。 北市警局督察長翁群能則說,要向
            當事人再次表達歉意,此件個案,經查發現搶餐的為刑警大隊隊員,後續協助家屬把員警強制
            就醫,並依搶奪罪嫌把員警移送士林地檢署偵辦,員警行為確實不恰當。
            '''
        ),
    )
    assert parsed_news.category == '政治'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1635483360
    assert parsed_news.reporter == '陳家祥'
    assert parsed_news.title == '特勤警失控當街搶外送員餐點 議員批:人民保姆變搶奪現行犯'
    assert parsed_news.url_pattern == '2112150'
