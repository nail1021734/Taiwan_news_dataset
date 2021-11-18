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
    url = r'https://star.ettoday.net/news/2104515'
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
            前一篇文章寫了國父的四個謊言,許多人恍然大悟,才知道從小被騙;於是就有人問:國父騙人
            ,那蔣公有沒有騙人呢? 有的有的,而且不遑多讓,且容我一一道來: 1.「蔣公繼承國父
            遺志完成革命事業」 從頭到尾,孫文心中的接班人不出以下三位:汪精衛、胡漢民、宋教仁,
            蔣介石只是一介武夫,孫文讓他當黃埔軍校的校長,是為了培植自己的軍力,至於國家大計
            則從來不找他商量。 但是蔣介石的專長就是權力鬥爭,上述三個人死的死、逃的逃、被逼反
            的反,最後就只剩蔣介石還在孫文身邊——其實孫蔣兩人看似親密的一些照片
            (例如在火車窗口對望的那張)有很多張是假的,如果他真是孫文屬意的接班人,又何必
            作賊心虛、變造假證據呢? 還有一位國史館長更誇張,他竟然說送孫文臨終時喊的是:
            「和平、奮鬥、救中國、介石、介石...」。不惜編造假歷史來彰顯蔣介石的「正統」地位,
            你覺得會是誰讓他這麼幹的? 2.「蔣公領導北伐成功打敗軍閥」 蔣介石帶兵打軍閥是真的,
            問題是他並不是合法的政權代表,他自己也是個軍閥,所以這一整個就是南方和北方的
            軍閥大混戰,殺來殺去、血流成河、民不聊生,簡直和歷史上的五代十國沒什麼兩樣。
            這就好像流氓打架、殃及無辜,根本沒什麼好「成功」的。 3.「蔣公領導八年對日
            抗戰勝利」 蔣介石不情不願的被迫對日宣戰之後,像台兒莊大捷這樣的勝仗少之又少
            ,￼八年來幾乎沒打贏過,基本上就是從南京一路敗退、再敗退、一直退到了重慶,再差一步
            就要退到西藏去了...要不是美國丟了兩顆原子彈,逼得日本投降,蔣介石的「勝利」
            根本是撿來的、不是自己打出來的! 4.「蔣公領導光復台灣、重回祖國懷抱」 台灣
            原本屬於清國,後來割讓給日本,中華民國成立的時候,根本沒有將台灣列入版圖,那麼中國
            怎麼會是台灣的祖國? 中國人如果有把台灣人當作同胞,就不會有二二八事件那麼血腥殘暴
            的屠殺,「台灣重回祖國懷抱」根本是個天大的謊言,是被「強占」而不是被「光復」! 5.
            「共匪竊據大陸,蔣公領導政府播遷來台」 國民黨政府貪污腐敗,人民怨聲載道,以致
            兵敗如山倒,日本人八年打不下的江山,共產黨不到四年就風捲殘雲,由此可知當時的
            人心向背,何「竊據」之有? 真正的小偷是蔣介石:那時他已經下台,沒有任何政府職位,
            卻偷偷搬運國庫黃金和故宮文物,逃到台灣來占地為王,蔣介石才是「竊據」台灣好嗎?——
            明明是個喪家之犬,還來扮演民族救星,真是超級可笑! 6.「蔣公領導我們
            反攻大陸解救同胞」 早就回不去了!卻還在欺騙人民:政府明明流亡台灣,卻能選出
            大陸各地的國大代表,「假裝」有一天還要回去。更可惡的是發給老兵們「戰士授田證」,
            騙說將來回鄉可以分到土地,讓他們就抱著這個幻想在台灣孤獨終老,甚至沒能建立
            自己的家庭。 而政府明明已經跟美國簽訂了中美協防條約,絕對不允許向大陸出兵,
            卻還是在媒體上日日喊口號、在學校裡天天寫作文,永遠都是「大陸同胞生活在
            水深火熱之中,等待我們早一天去解救他們」,或是「明年的今天,我們要把青天白日滿地紅
            的國旗,插在南京城上」...這樣計劃性、全面性、長期性的散播謊言,蔣介石應該可以列入
            世界金氏記錄了! 被騙那麼久、被騙那麼多,竟然還有人必恭必敬的稱他為「公」——
            什麼蔣公?我還「碗公」咧!
            '''
        ),
    )
    assert parsed_news.category == '雲論'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634623980
    assert parsed_news.reporter == '苦苓'
    assert parsed_news.title == '有關蔣公的六個謊言'
    assert parsed_news.url_pattern == '2104515'
