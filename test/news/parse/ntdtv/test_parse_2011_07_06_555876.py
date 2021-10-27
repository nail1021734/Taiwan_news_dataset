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
    url = r'https://www.ntdtv.com/b5/2011/07/06/a555876.html'
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
            滿頭銀髮、辯才無礙的拉加德(Christine Lagarde)身為7國集團(G7)會員國的首位女性
            財政部長,令人印象深刻。在全球經濟危機期間,她贏得了遭受抨擊仍不失優雅的
            美名。 拉加德今天就任國際貨幣基金(IMF)總裁,成為這個全球緊急貸放機構的第1位
            女總裁。 曾擔任貨幣基金總裁的經濟學家羅格夫(Kenneth Rogoff)曾告訴「紐約時報」
            (New York Times),拉加德在財金會議中極受歡迎,「實際上被當成搖滾巨星一般
            看待」。 現年55歲、律師出身的這名巴黎女性,成為法國在職最久的財長,自2007年
            迄今。 拉加德英語流利,2008年成為歐洲因應金融危機的領袖人物,當時宛如歐元各國
            財長之首。 由於法國現為全球各大經濟體20國集團(G20)輪值主席國,因此拉加德也就成了
            對抗危機效應和改革全球金融制度的尖兵。 她是國際舞台上的熟面孔,因巧妙處理危機而
            獲某些人士肯定,也因堅持而遭另一些人批評。 英國「金融時報」(Financial Times)
            2009年評選拉加德為「年度最佳財長」,理由是她在面對戰後最嚴重的世界性衰退時,決心
            堅定。同年她並被「富比世」雜誌(Forbes)評選為世界最有權勢女性第17名。 拉加德雖
            研讀法律和政治,但工作後不久即邁入商業和金融界。 法國總統沙柯吉
            (Nicolas Sarkozy)在2007年就職後,即任命她出任農業部長,並在其後令人意外的人事
            改組中,調任她為財長。 她使財政部進入1990年代後即已消失的穩定狀態,因而成為沙柯吉
            總統任期內的關鍵人物。在她之前,法國7年曾更換7名財長。 拉加德的失誤多半與財金
            問題無關,但總會觸及法國的政治敏感神經。比如她將法國勞動法規指為「複雜、多如牛毛」
            並使就業機會成長受阻時,就引發了風波。 再如油價飆漲時,她呼籲法國人民騎自行車外出,
            這都使她背負上和社會脫節的罵名。但這些問題都未使她下台。 倒是近來她被指涉及利益
            衝突,使她的政治生涯蒙上了陰影。不過她反駁說:「我的良知清白無瑕。」
            '''
        ),
    )
    assert parsed_news.category == '財經'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1309881600
    assert parsed_news.reporter is None
    assert parsed_news.title == 'IMF新總裁拉加德'
    assert parsed_news.url_pattern == '2011-07-06-555876'
