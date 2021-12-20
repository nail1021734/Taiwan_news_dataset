import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/13/12/19/n4037847.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            今年七月瑞士和中國簽訂了《中國–瑞士自由貿易協定》。由於該協定沒有任何文字涉及人
            權問題,最近兩周繼續在瑞士國會引起辯論,受到媒體和各非政府組織的強烈批評。 歐洲和
            中國的經濟交流不僅使歐洲人看到中國在經濟上對於歐洲的重要性,而且也越來越多地看到
            中國日益惡化的人權狀況和嚴重的環境問題。 七月,瑞士政府和中國簽署了《中國-瑞士自
            由貿易協定》,這一協定被瑞士政府作為保證自由貿易交流,發展瑞士經濟,保障就業的一項
            重要成就。但是該協定由於沒有任何字句涉及中國的人權問題,從簽訂時就受到瑞士的一些
            政界人士、媒體和人權、環境團體的強烈批評。 最近兩周,這個問題更在瑞士國民議會及
            媒體受到強烈的質疑。 在這一波爭論中,瑞士電視台推出了一部涉及中國勞工狀況及權利
            問題,環境問題的專題片,影片記錄了瑞士記者專門到中國惠州等地區進行的採訪報告;很多
            非政府組織再次對政府的這個政策提出明確的批評。 丹妮埃拉‧蕾瑙德代表幾個人權和環
            境組織批評這個協定是一個「絕對的後退」。 她認為,整個協議中沒有任何字詞涉及人權
            問題,為此也就不可能在這方面有任何約束力和義務。中國的人權狀況和環境問題繼續惡化
            ,對此,人們必須回答的是,在這個協議中,有多少中國勞工的權益被犧牲掉。 關於這個協議
            ,蕾瑙德還特別強調說,我們不能夠允許,在以後的貿易協定中現在的瑞士作為如此一個負面
            的榜樣出現。 七月份到親自到中國簽署這個協議的經濟部長施耐德-阿曼則不得不公開在
            媒體上回答了質疑。他雖然承認在把人權問題寫進協議問題上,瑞士政府失敗了,但是對此
            辯解說,瑞士政府在和中國政府的談判中已經盡了一切努力。雖然協議中沒有涉及人權的字
            句,但是中國簽署了聯合國人權憲章,他們知道自己的應該遵守什麼,所以「自由貿易協定」
            也不會給瑞士在人權問題上留下壞的名聲。 針對批評,施耐德-阿曼甚至還反擊說,在這個
            協定中有一節涉及了環境問題,與協定平行的另外一個協定中也談到了勞工條件問題。他認
            為,在過去二十五年中中國在人權問題、勞工條件問題和環境問題上已經取得了巨大的進步
            。為此,他對成功地簽署這個協定感到驕傲。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1387382400
    assert parsed_news.reporter == '李明'
    assert parsed_news.title == '《中瑞自由貿易協定》不談人權 引各方批評'
    assert parsed_news.url_pattern == '13-12-19-4037847'
