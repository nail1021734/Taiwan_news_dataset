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
    url = r'https://www.ntdtv.com/b5/2013/12/19/a1026801.html'
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
            印度當局和民眾就一名外交官被捕被搜身事件繼續向美國政府表達強烈不滿。
            分析人士認為,事件可能會損害美印安全關係。 反美遊行在巴基斯坦司空見慣,但在鄰國
            印度,如此激昂的反美抗議活動並不多見,因此星期三發生在美國駐新德里大使館外的這場
            民眾示威格外引人注目。 一天前,印度當局將原本放在美國大使館大門前阻擋未授權車輛
            進入的安全路障挪開,還要收回美國外交官們的印度身份證,取消他們的機場通行證。 印度
            對美國的強烈不滿源自她的一名外交官在美國受到被印度人視為無可忍受的羞辱。印度
            駐紐約副總領事科巴拉加德女士因涉嫌編造簽證申請文件12月12號被美國聯邦法警逮捕,期間
            她曾被搜身,還被關在關押普通犯罪嫌疑人的拘留所。 針對當局目前對美國駐新德里大使館
            採取的相應措施,印度外長庫爾希德星期三在國會表示,當局採取的行動是適當的
            。 庫爾希德:“我認為,從國內民眾和國會的反應來看,我們採取的行動是適當。我想,尊貴
            的議員們的意見是,我們必須堅持下去,直到我們達到目的。” 印度要求美國道歉 美國
            稱逮捕程序合法 新德里要求美國政府對印度外交官受到羞辱事件公開道歉,否則雙邊關係
            會受到負面影響。 美國國務院發言人瑪麗•哈夫星期二表示,從目前了解的情況來看,美國
            有關當局在逮捕科巴拉加德女士的過程當中採取了適當的措施。她說這是一起個別事件,希望
            不會影響兩國關係。 在此之前,美國和印度政府都聲稱兩國關係發展良好。印度總理辛格
            9月27號在白宮會晤歐巴馬總統的時候稱,印度和美國是兩國以及整個世界不可或缺的夥伴
            。 美印防務合作可能受影響 9月17號和18號,當時的美國國防部副部長卡特在與印度政界
            人士和軍方官員會談時著重討論了兩國在國防領域的合作,包括美國向印度提供先進的武器
            裝備。 巴拉特•維爾馬(Bharat Verma) 是印度一位資深防務專家。 維爾馬:“這個事件
            將會損害印度與美國的關係。在此之前,兩國關係正以良好的速度發展,並即將帶來良好的
            成果。” 印度是與中國有領土主權爭端的幾個國家之一,兩國在邊境地區經常發生摩擦
            。新德里正謀求與美國合作,強化自己的軍事能力。與此同時,美國正在實施亞洲再平衡
            戰略,並積極謀求與中國周邊的印度等國家發展和強化軍事合作。 作為美國國防部副
            部長,卡特今年9月在華盛頓智庫美國策進中心(Center for American Progress)說
            ,作為世界兩個最大的民主國家, 美國和印度注定是夥伴,即使兩國在某些領域立場
            不完全一致。
            '''
        ),
    )
    assert parsed_news.category == '美國'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1387382400
    assert parsed_news.reporter is None
    assert parsed_news.title == '外交官被捕事件或損美印安全關係'
    assert parsed_news.url_pattern == '2013-12-19-1026801'
