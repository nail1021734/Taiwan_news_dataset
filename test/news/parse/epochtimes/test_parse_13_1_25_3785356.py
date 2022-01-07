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
    url = r'https://www.epochtimes.com/b5/13/1/25/n3785356.htm'
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
            2013年1月24日,諾基亞在發佈的公司財報中表明,去年發佈的諾基亞808PureView將是公司
            最後一款以塞班系統為平台的手機。這標誌著諾基亞官方正式宣告塞班系統的死亡。 諾基
            亞公司稱:「2012年我們向Windows Phone過渡時,一直在出售塞班系統手機。然而去年中發
            佈的808PureView將是我們最後一款塞班手機。」 塞班系統作為當年市場份額一度超過50%
            的智能手機操作系統,曾深深地融入了人們的生活,影響了全球的消費者。 2008年是塞班系
            統最為輝煌的一年,2008年12月2日,塞班公司被諾基亞收購。但同一年,蘋果IOS系統和谷歌
            Android系統開始崛起。 從2009年開始,眾多手機廠商開始拋棄Symbian,最終唯諾基亞一家
            留守。如今諾基亞的退出意味著塞班系統已經正式宣告死亡。 塞班系統江河日下 諾基亞
            深受打擊 隨著蘋果IOS系統和谷歌Android系統在市場上高歌猛進,塞班系統江河日下,短短
            4年間,在當前所有手機出貨量中,塞班系統手機已經降至只佔2.6%的市場份額,而安卓達到7
            2%。 諾基亞發佈的財報顯示,2012年第四財政季度售出的塞班手機為220萬部,只有Lumia手
            機的一半,而且占諾基亞智能手機總出貨量(1590萬)不到14%的比例。 塞班系統的日趨式微
            令諾基亞這個手機巨頭遭到幾乎致命的打擊,鐵了心投靠微軟並等待windows phone系統出
            台的諾基亞幾年來眼看著大力採用android系統的三星公司徹底取代其市場第一的位置,而
            諾基亞眼中的競爭對手蘋果則再沒有把諾基亞這個公司放在眼裡。 諾基亞坐看
            三星崛起 有消息稱,諾基亞因選擇Windows Phone系統而非Android系統,每季度從微軟
            獲得2.5億美元淨收益。兩家公司曾達成協議,微軟將向諾基亞支付平台支持費,而諾基亞
            作出了年度最低軟件版稅承諾,並按季度支付版稅。諾基亞稱,在協議期限裡,其從微軟獲得
            的支付款將略微超過其支付的軟件版稅。但諾基亞沒有透露協議的期限。 但事實上,諾基亞
            得到了每季度2.5億美元的小利,但失去的卻是幾乎整個智能手機市場。三星的四季度財報
            顯示,手機產品為三星帶來了245億美元的的收入,比上一季度增長4%,其中Galaxy SIII和
            Galaxy NoteII的銷售銷售量分別突破3000萬和500萬台的大關。 塞班系統曾經
            輝煌 1998年6月,Psion公司聯合手機業界巨頭,諾基亞、愛立信、摩托羅拉組建了Symbian
            公司。Symbian隨後推出了白金合作計劃吸引了包括ARM、Motorola SPS Real Net
            works、TI德州儀器等大量的廠商加入。 接著,眾多手機生產商加入生產採用Symbian系統
            的手機。2004年第一季度,LG、Arima和聯想成為最新取得Symbian授權協議的手機製造商,
            從而使得獲得授權的廠商總數達到了18家,幾乎囊括了全球所有重量級的手機製造商。
            '''
        ),
    )
    assert parsed_news.category == '科技新聞,IT 動向'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1359043200
    assert parsed_news.reporter == '高科,姜斌'
    assert parsed_news.title == '諾基亞停止開發塞班手機 宣告塞班系統死亡'
    assert parsed_news.url_pattern == '13-1-25-3785356'
