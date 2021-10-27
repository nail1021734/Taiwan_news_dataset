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
    url = r'https://www.epochtimes.com/b5/13/12/31/n4047555.htm'
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
            搶救德國F1賽車冠軍舒馬赫的醫生在週二(31日)的新聞發佈會上說,做完減輕腦部壓力的
            手術後,舒馬赫的病情有輕微好轉。 醫生說,夜裡做的一個掃瞄顯示,舒馬赫的病情比昨天
            (30日)有一點改善,但是他仍然沒有脫離危險。 曾七次贏得一級方程式賽車冠軍的舒馬赫
            星期天在法國阿爾卑斯山滑雪時摔倒,頭部撞上岩石,目前處於昏迷狀態。 在做完減緩腦部
            壓力的手術之後,醫生對舒馬赫做了又一次掃瞄,結果顯示的「略微改進」狀況,使醫生們
            有了可能為他做第二次腦部手術的機會。 舒馬赫的家人作出了一個被記者稱為的「艱難的
            決定」,同意二次手術。 之後醫生又對舒馬赫做了一次兩小時長的開顱減壓手術。 醫生強調,
            未來數小時對病情發展至關重要,任何情況都可能發生。 德國總理默克爾的發言人說,默克爾
            和她的政府像所有德國人一樣,對舒馬赫的這一事故感到「極其震驚」。 這名發言人還說:
            「我們和舒馬赫的家人一起祝願他能夠戰勝傷情,早日康復。」 2009年在匈牙利大賽中頭部
            受到致命重傷後恢復的舒馬赫在法拉利車隊的前隊友馬薩也為舒馬赫祝福。 馬薩在社交網站
            上寫道:「我一直在為你祈禱,我的兄弟!我希望你儘快康復。上帝保佑你。」
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388419200
    assert parsed_news.reporter is None
    assert parsed_news.title == '舒馬赫病情「輕微好轉但仍未脫離危險」'
    assert parsed_news.url_pattern == '13-12-31-4047555'
