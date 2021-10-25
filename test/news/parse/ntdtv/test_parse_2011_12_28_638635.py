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
    url = r'https://www.ntdtv.com/b5/2011/12/28/a638635.html'
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
            朝鮮領導人金正日17日猝逝,今天舉行國葬,由年紀尚輕的兒子金正恩接班。朝鮮擁核子武器
            自重,近年與韓國和列強爭執不斷。以下為朝鮮自二次大戰結束以來重大歷史事件一覽: 1945年:
            日本在二次世界大戰投降後,結束對朝鮮半島的殖民統治。朝鮮半島以北緯38度線劃分?南北
            兩塊勢力範圍,朝鮮與韓國分別獲得蘇聯和美國支持。 1950-53年:蘇聯和美國軍隊撤離
            朝鮮半島後,朝鮮入侵韓國,爆發韓戰。以美軍為主的聯合國部隊介入協助韓國,中國大陸則
            支持朝鮮。韓戰估計約造成400萬人喪生。戰後,美國保留在韓國的重兵部署。 1988年:
            美國把朝鮮列入支持恐怖主義的國家名單後,對朝鮮祭出制裁。 1989年:美國衛星圖片發現
            朝鮮寧邊(Yongbyon)地區的1座核燃料再處理廠。 1994年:美國就移除寧邊核反應爐
            廢燃料棒問題,差點與朝鮮開戰。美國前總統卡特(Jimmy Carter)訪問平壤化解這場危機。
            朝鮮承諾凍結和廢除核子計畫,以換取能源援助。 1998年:朝鮮首度發射長程彈道
            飛彈。 2002年:美國總統小布希(George W. Bush)點名朝鮮是「邪惡軸心」的一環。美國
            指控朝鮮擁有使用濃縮鈾的秘密核武計畫後,雙方的1994年協議破局。 2003年:朝鮮退出
            「禁止核子擴散條約」(NPT),六方核子會談8月於北京展開。 2005年:朝鮮首度承認擁有
            核武。 2006年:朝鮮10月9日進行第1次核子試爆,引發國際社會的譴責和聯合國更多
            制裁。 2007年:朝鮮2月同意放棄核子設施,以交換經濟援助和外交利益。朝鮮7月表示
            已關閉主要核子設施。 2008年:朝鮮6月炸毀位於寧邊的冷卻塔,展現對核子裁軍的
            承諾。美國10月將朝鮮從支持恐怖主義的黑名單除名。 2009年:朝鮮4月5日發射長程
            火箭,在受到聯合國譴責後,宣布將退出六方會談並重新啟動寧邊的核設施。朝鮮5月25日
            進行第2次核子試爆,引發聯合國更嚴厲的制裁。 2010年: 3月26日:韓國天安艦在朝鮮邊境
            沉沒,造成46名士兵喪生。國際調查人員之後表示,元兇是朝鮮魚雷,但朝鮮否認。 11月12日:
            朝鮮向來訪的美國科學家展示濃縮鈾工廠。專家表示,這座工廠經過改造後能製造
            原子武器。 11月23日:朝鮮砲擊韓國延坪島,造成4人喪生。 2011年: 7月22日:兩韓核子
            談判特使在峇里島(Bali)會談,討論重啟六方會談的可能性。 10月24-25日:美國和朝鮮在
            日內瓦舉行第2次雙邊會談,但未取得突破性進展。 12月19日:朝鮮官方媒體報導,金正日
            2天前心臟病發去世,享年69歲,同時呼籲民眾支持他的兒子金正恩接班。 12月28日:金正日
            喪禮於平壤舉行。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325001600
    assert parsed_news.reporter is None
    assert parsed_news.title == '朝鮮一甲子大事紀'
    assert parsed_news.url_pattern == '2011-12-28-638635'
