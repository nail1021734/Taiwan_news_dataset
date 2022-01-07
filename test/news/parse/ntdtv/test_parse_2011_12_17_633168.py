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
    url = r'https://www.ntdtv.com/b5/2011/12/17/a633168.html'
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
            12月16號,法國前總統希拉克,被巴黎一家法院以貪污罪判處兩年監禁緩刑。他是法國二戰
            以來第一位接受法庭審判的總統。大陸人士表示,腐敗與長期執政和獨裁成正比。這對貪官
            遍地的中共政權來說也是很好的警示。 這個案子要追溯到將近20年前,法庭認定,在上世紀
            90年代,希拉克還是巴黎市市長的時候,曾經非法挪用了公共資金,並濫用職權和信任。但是
            如今已經79歲的希拉克仍然逃不開有罪判決。 著名時事評論家伍凡表示,對希拉克進行
            審判,不僅給所有的法國官員敲響了警鐘,對貪官遍地的中共也是很好的警示。 伍凡:「法國
            人20年後判總統,中國同樣,共產黨倒了以後,我們建立一個機制,制定法律,要追所有的貪污
            官員,你走到哪裏我們要追哪裏,要把你判刑,也要讓共產黨的官員們知道,你現在做壞事,
            跑不掉的,你總有一天要追拿歸案。要對你審判,還給老百姓一個交待。」 前中共黨魁江澤民
            不僅治國無方,塗抹歷史,殺人如麻,賣國賣官,同時也是中國最大的貪官,媒體披露,江澤民在
            瑞士銀行存有3億5千萬美元的秘密賬戶,2002年12月9號,江澤民十六大前為自己準備後路,
            一次性轉移了30多億美元的資金到加勒比海中資銀行分支機構。 而前中共黨魁毛澤東在
            大饑荒的60年代,耗資1億2仟萬元,建豪華別墅——滴水洞工程。滴水洞工程從1960年下半年
            開工到1962年完工,建築面積共3,638.62平方米。連同韶山衝至滴水洞的公路。在此期間,
            全國有4,000多萬人死於大饑荒。然而他的罪行到現在也沒有清算。 大陸作家荊楚認為,
            這種正義的審判,只有民主國家才能做到。 荊楚:「這個事情就是民主制度的一個好處,哪怕
            他當了國家領導人,原來犯的罪永遠要追究,表明法國的防範方式方面還是比較有效的,過去
            發生的事情,一旦追查出來,他永遠要執行,永遠要繼續追究,這體現了一種社會公正,對犯罪
            的懲治,也就是社會比較有信心的體現。」 希拉克執政43年。他連續兩屆擔任法國總統,
            任期長達12年。在那之前,他還兩次擔任法國總理,並且連續18年擔任巴黎市市長一職。 荊楚
            認為,腐敗與長期執政和獨裁成正比。 荊楚:「一個人他長期執政,他就脫離了社會,他對
            自己的成果,對社會的認識,都不清楚了,這個權力沒有得到及時的制衡,老百姓沒有權力用
            選票把他選下去,他就是肆無忌憚的,共產黨幾十年的執政,現在成了全球最腐敗,最墮落,
            最殘忍,血腥的黨。」 法官表示,希拉克的行為讓巴黎納稅人蒙受了大約相當於140萬歐元的
            損失。 希拉克是1945年貝當被判定犯有叛國罪之後第一個被定罪的法國前國家元首。貝當
            曾在二戰期間擔任法國國家元首,由於向納粹德國投降而被認定犯有叛國罪,被判處死刑,但是
            由於在第一次世界大戰中的功勞而被赦免死刑。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324051200
    assert parsed_news.reporter == '劉惠,孫寧'
    assert parsed_news.title == '審判法前總統希拉克 對中共的警示'
    assert parsed_news.url_pattern == '2011-12-17-633168'
