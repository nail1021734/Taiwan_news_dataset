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
    url = r'https://www.ntdtv.com/b5/2018/08/06/a1386361.html'
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
            香港前特首梁振英被揭收取澳洲公司UGL約5000萬港元事件,至今已近四年,但香港廉政公署
            一直沒有向公眾交代案情,引發不滿。8月3號,公民黨立法會議員郭家麒與數名黨員到
            北角廉政公署總部請願,要求速查。請看報導。 香港公民黨多名成員上週五到廉政公署總部
            外請願,遞交信件要求廉政專員白韞六,秉公辦理香港前特首梁振英有關UGL的案件。
            廉署派人接收了請願信件。 立法會議員郭家麒表示,前特首曾蔭權因觸犯公職人員行為
            失當罪,上月被判入獄一年。而梁振英收取UGL巨款一事,涉嫌觸犯公職人員行為失當罪,
            但至今案件真相不明,廉政公署應該盡快公開交代案件的調查進度。 立法會議員郭家麒:
            「到現在差不多四年,但廉署及其他相關政府部門仍然含糊其詞,甚至到今年年初有傳聞說
            律政署不作起訴,我覺得這是對香港所有市民的一個恥辱,摑了一大巴掌。」 郭家麒希望廉政
            專員白韞六,不要顧忌梁振英是中共全國政協副主席的背景而包庇他,應該頂住壓力,
            確保香港肅貪倡廉的良好制度不受損害。 2014年10月,澳洲傳媒《Fairfax Media》
            報導,時任香港行政會議召集人梁振英在宣布參選特首後,仍以戴德梁行董事身份與
            澳洲企業UGL簽訂秘密協議,透過提供顧問服務、協助挽留員工、不作競爭等安排,
            在2012和2013年共收取5000萬港元的報酬。 事件爆發後,引發港人關注。 但將近四年
            時間,相關案情至今還是沒有交代,背後隱藏著什麼秘密呢? 旅美時事評論員鄭浩昌表示,
            雖然同為前特首,但梁振英的情況和曾蔭權其實有很大的差異。梁振英在卸任後進京出任
            政協副主席,一方面,令中共中紀委查辦他變得很容易,但換一個角度來看,如果中紀委不動他,
            這個職位又會成為他的保護傘。 旅美時事評論員鄭浩昌:「而且,梁振英和中共的勾連
            其實相當的深,這一點不是曾蔭權可以比的。他在任特首前就已經做了九年多的全國政協常委,
            你想想,如果說曾蔭權的底色是淡紅色,那梁振英絕對是鮮紅色。這樣的地下黨員中共當然
            會保他啦。」 旅美時事評論員唐靖遠:「曾蔭權的腐敗程度,他的數目和梁振英已經被披露
            出來的貪腐的數目,其實是沒法相比的,梁振英的明顯要嚴重了很多。我們看到曾蔭權都
            已經被通過司法的起訴,而且把他判有罪之後把他送到監獄去服刑。為什麼梁振英他到現在
            還依然逍遙法外,我覺得跟廉政公署0810怎麼樣來處理看待梁振英這個案子,就有密切的
            關係了,那麼這個背後我覺得最深層的原因是,他其實是涉及到在中共高層的政治勢力的
            一種博弈。」 就梁振英收取UGL巨款一事,香港民眾多次批評當局迴避問題,
            有包庇嫌疑。 2016年,會計界議員梁繼昌及民主黨尹兆堅提交呈請書,要求成立專責委員會
            調查梁振英UGL巨款事件,獲28名非建制派議員支持通過。 2017年1月11號,民主黨議員
            提出質疑,梁振英涉嫌收取UGL款項事件,仍有不少疑團未解,其中包括行政長官沒有執行
            《基本法》第47條的相關規定,此外,梁振英和政府一直都沒有提交充足資料,
            向公眾交待。 今年4月,民主黨立法會議員林卓廷等也發起「天下為公」眾籌計劃,
            希望集結群眾力量和支持,就梁振英收取UGL巨款一事作進一步調查。結果反應熱烈,
            短短7天就籌得200萬港元。
            '''
        ),
    )
    assert parsed_news.category == '港澳'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1533484800
    assert parsed_news.reporter is None
    assert parsed_news.title == '梁振英涉貪案無交代 港政黨促速查'
    assert parsed_news.url_pattern == '2018-08-06-1386361'
