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
    url = r'https://www.epochtimes.com/b5/13/3/16/n3823858.htm'
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
            有一個山西富商,住在京城信成客店裡,衣着、跟隨的僕人和馬匹,都很華麗,他這次進京的
            目的是捐獻一筆錢買個官做的。 有個窮老漢來拜訪他。僕人們都不願替他通報,那老漢只
            好在大門口等,結果還是等著了。山西富商對老漢很冷淡,招待了一杯清茶後,就再也沒有一
            句寒喧話。 老漢坐了一會兒,遲遲疑疑地表示出一點要求幫助的意思,山西富商馬上放下臉
            來,搖著頭說:「我現在連買官的錢,都沒湊夠數,哪裡有力量來幫助你?」老漢很不服氣,就
            當著眾人,詳細地講了這個山西富商的來歷。 他說:「我過去是做官的,比較清正愛民。這
            個富商從前很窮,生活一直靠我接濟。我幫了十幾年,最後又送給他一百兩銀子去做生意,他
            才慢慢地成了富商。現在我被陷害、罷了官,流落京城,聽說這個富商來了,十分高興,真好
            像遇到了救星。我老漢也沒有過高的要求,只要能得到我從前給他的一百兩銀子,以便我償
            還欠債,剩下的夠我回故鄉的路費,也就心滿意足了。」老漢說到這裡,就抽抽噎噎哭個不停
            。山西富商竟然好像一點也沒有聽到,無動於衷。 忽然,同住在這一個客店裡的江西人站了
            出來,他自稱姓楊,對山西富商拱了拱手,問道:「那位老漢說的都是真的嗎?」山西富商紅著
            臉回答說:「情況確實是這樣,但是現在我無力報答他,實在遺憾。」姓楊的說:「你很快就
            要做官了,不愁沒有地方借錢。如果有人肯借一百兩銀子給你,一年之內歸還,不收分毫利息
            ,你能把這一百兩銀子全部還給他嗎?」 山西客商勉強回答說:「很願意。」姓楊的說:「那
            你就寫一張借據,一百兩銀子我這兒有。」山西客商迫於公論,只好寫了一張借據。姓楊的
            收下借據,打開一隻破箱子,拿出一百兩銀子交給山西富商。山西富商滿臉不高興地把銀子
            遞交給了那位老漢。 姓楊的又置辦了一桌酒席,請那老漢和山西富商一同喝酒。老漢喝得
            很高興,山西富商卻是一肚子氣,草草喝了兩杯就告辭了。老漢向姓楊的表示了感謝,過了一
            會兒也離開了。 那個姓楊的江西人,不久也搬出了客店,從此再沒有消息了。 後來,山西富
            商開箱檢點自己的銀子,發現少了一百兩。然而,箱子上的鎖攀、封條,都還是好好的,根本
            沒有動過,無法向人查問。富商又發現丟了一件狐皮背心,卻在箱子裡找到了一張當票,上面
            寫着當錢二千文。這個錢數,同姓楊的辦酒席的費用完全一致。 山西富商這才知道:「姓楊
            的是一個懂法術的 人,他利用法術取走了我的一百兩銀,讓我還給了那個老漢;還讓我出錢
            辦酒席,招待了他們!」客店裡的旅客和店主等人,知道了這件事後,都暗暗拍手稱快。 那個
            山西富商又慚愧,又沮喪,趕快離開了信成客店。後來,也不知搬到什麼地方去住宿了。
            '''
        ),
    )
    assert parsed_news.category == '文化網,預言與傳奇,神話傳說,中國民間故事'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1363363200
    assert parsed_news.reporter is None
    assert parsed_news.title == '富商還錢'
    assert parsed_news.url_pattern == '13-3-16-3823858'
