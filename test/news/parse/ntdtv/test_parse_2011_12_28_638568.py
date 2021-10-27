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
    url = r'https://www.ntdtv.com/b5/2011/12/28/a638568.html'
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
            2012台灣大選在即,「首投族國政觀察團」於28號公布民調,如果明天就是投票日,有
            21.4%的首投族會投給馬英九、18%會投給蔡英文,但是有34.5%的首投族還沒決定要投誰。
            觀察團在同時發表的青年政策請願書中,還提出多項建議,希望競選各方予以回應。 來自
            各大專院校學生組成的「首投族國政觀察團」公布民調。如果明天就是投票日,有21.4%的
            首投族會投給馬英九、18%投給蔡英文,[9.1%投宋楚瑜],但是有34.5%的首投族還沒決定
            要投誰,而且有17%的人已經決定不去投票。 臺大政治研究所徐維遠同學:「我們觀察選舉
            到現在,我們非常非常的懷疑,當我們投下那一張薄薄的選票的時候,上面所承載的,我們
            青年人的心聲還有我們對未來的希望,候選人你們感受到了嗎?」 觀察團列出青年人最關切的
            五大議題,依序是教育 、就業、居住、環境和兩岸。花了近四個月的時間彙整資料、寫成
            120頁青年政策請願書,要送給各候選人陣營。 首投族國政觀察團團長陳乙棋:「在未來的
            17天的競選選戰裡面,可以停止口水了,不要再宇昌案、也不要再富邦案,是要去真正的回歸
            我們台灣,不管是年輕人,不管是我們台灣的民眾,究竟需要的是甚麼希望他們能夠看到這份
            請願書之後,能夠去真正看一看,年輕人的需求是甚麼,然後也做出一些具體的回應。」 為了
            吸引更多首投族提高投票意願,觀察團和客運公司推出在校生返鄉優惠專案。 首投族
            國政觀察團發言人林聖像:「1月9日的中午12點到1月12日的中午12點為止,所有從臺北、
            臺中發出去的車跟開回來的車的路線,都是採用客運愛心票,半價的方式做優惠。」 觀察團
            呼籲,128萬多個首投族,不要放棄用自己的選票,決定國家的未來。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1325001600
    assert parsed_news.reporter == '曾奕豪,張明筑台灣臺北'
    assert parsed_news.title == '首投族民調 近3成5仍未表態投誰'
    assert parsed_news.url_pattern == '2011-12-28-638568'
