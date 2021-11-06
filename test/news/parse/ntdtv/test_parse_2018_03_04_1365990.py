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
    url = r'https://www.ntdtv.com/b5/2018/03/04/a1365990.html'
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
            中共外圍組織青關會,近期不斷在香港滋惹事端。一名未成年的學生,因路過時拍打了幾下
            青關會滋事用的器具,遭到青關會成員誣告,而後被警方逮捕。事件引發香港市民的強烈不滿。
            青關會的背景也再次引發關注。 這段視頻點擊率已經過百萬。事件發生在2月27日下午
            深水埗南昌街和汝州街交界處。 一名懷疑有自閉症的15歲學生,拍打了挂在路邊構陷法輪功
            團體的易拉架,被青關會女成員誣告「偷竊」。該名學生因此遭多名警員追捕、抬上警車,
            期間情緒激動。 事發時,印度裔商人JACKY在附近做生意,目睹事件經過,挺身而出踢爆
            大媽造假,並和青關會成員對質,引發網民熱議。 印度裔港人JACKY:「我問她這是你的
            店舖嗎?這不是店舖,你根本講大話,我問她六次,你是否講大話,她沒有話答。她接著問
            我你什麼人,來了多少年?我說50年,她說我來了100年。100年,你都沒有100歲,還是在
            講假話。」 圍觀的人有上百名,但只有JACKY和朋友去和青關會對質。JACKY希望港人
            能夠互相幫助。 印度裔港人JACKY:「我不想做英雄,別人說英雄英雄,香港人全部都是英雄,
            一定要幫人,最重要是幫到人,事情就清楚了。」 青關會成員曾多次誣告法輪功學員,
            對於再次誣告普通學生,有路過的市民批評,青關會是中共非法組織,目地是將黨文化輸出到
            香港。 香港市民陳先生:「我們幾次看到青關會在街上的表演,許多大陸人也很反感。
            共產黨壓制言論自由,但香港人不會,香港還是愛民主、愛自由。」 也有網民直言,青關會是
            「共產黨派來的專打法輪功組織」,「青關會應該在香港消失。」 「香港青年關愛協會」
            簡稱「青關會」,成立於2012年。 多家香港媒體調查發現,青關會主要成員,和中共統戰部
            等官方組織來往密切,青關會就是與中共專職迫害法輪功的非法組織610辦公室有關的中共
            外圍組織。 這幾年,「青關會」成員在香港街頭對和平抗議的法輪功修煉者進行文革式的
            攻擊、謾罵和流氓騷擾,嚴重踐踏、破壞了香港的言論和信仰自由。 唐靖遠:「這個團體
            日復一日在香港街頭,用活生生的行動上演中共階級鬥爭那一套東西,事實上是在用中共特有
            的流氓黨文化在毒化、熏染乃至最終破壞香港既有的中國傳統文化,以及英國給香港留下來的
            紳士文化、公民意識以及法治精神。」 有分析指出,目前香港「一國兩制」嚴重走樣,是通過
            四條線做到的。 唐靖遠:「一是紅道,即安排親信出任與港澳事務相關的各級機構負責人;
            二是黑道,即操縱所謂的「愛國」黑社會,使用暴力流氓手段來打壓、清除障礙人物;
            三是灰色地帶,即以青關會這類以民間團體出現的外圍組織,借「言論自由」之名行打壓言論
            之實,來阻止不利言論或掩蓋中共犯罪真相;四是透明人,即以各種身份安插在各階層的國安
            特務、線人等。」 觀察界認為,過去20年,這四條線全部把控在江澤民和曾慶紅集團手中。
            他們會根據需要,用自己人來扮演敵人,製造亂象,配合北京權鬥的同時,
            攪亂香港局勢。 習近平此前訪港,提出要讓香港「行穩致遠」,隨著江曾集團的衰敗,
            現政權要如何安撫港人情緒,尊重港人意願,各界都在看。
            '''
        ),
    )
    assert parsed_news.category == '法輪功,法輪功人權'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1520092800
    assert parsed_news.reporter is None
    assert parsed_news.title == '誣告學生惹眾怒 青關會再遭起底'
    assert parsed_news.url_pattern == '2018-03-04-1365990'
