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
    url = r'https://star.ettoday.net/news/1200134'
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
            北韓駐日內瓦代表部參事官朱容哲26日參與聯合國裁軍會議
            (Conference on Disarmament)時指出,因日本沒有簽署《板門店宣言》和「川金會」
            共同聲明,無權參與協商朝鮮半島無核化問題,「應該自制一些,不要干涉別人的事情比較
            好。」 朱容哲也直言,在他們決定盡速實踐無核化以後,奧地利、澳洲、阿根廷等國都引用
            《板門店宣言》和「川金會」共同聲明的條文來批評北韓,令人無法容忍。 據《韓聯社》報導
            ,朱容哲會如此狠嗆日本,或許是因為在他發言以前,日方代表在會議上大肆發表他對北韓核
            武議題的意見,且強調若北韓決定確實履行「川金會」聲明內容,必將需要南韓、美國及日
            本的協助。 在此之前,日本首相安倍晉三16日參加《讀賣新聞》節目時提到,為了完全的無
            核化,願意為國際原子能總署(IAEA)負擔到北韓驗證的費用,但條件是先解決北韓綁架日人
            問題。 對於安倍的言論,北韓則利用官方媒體《朝中社》指責,「不論是過去還是現在,朝
            日關係的基礎都是轉型正義。日本不該握著一點籌碼就耍小手段,而應以誠實的態度來彌補
            過去違法和不正義的行為。」
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530086520
    assert parsed_news.reporter == '陳宛貞'
    assert parsed_news.title == '自制一點!北韓狠嗆日本「無權干涉無核化協商」'
    assert parsed_news.url_pattern == '1200134'
