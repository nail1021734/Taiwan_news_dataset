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
    url = r'https://www.ntdtv.com/b5/2011/12/20/a634655.html'
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
            朝鮮獨裁者金正日去世,官方仆告:「金正日於19日在巡視一線工作的列車上因勞累過度而
            猝死。」但金正日的死因是否是朝鮮官方公布的這樣,網友們驚訝之余提出了幾大疑點。 19
            日朝鮮時間中午,朝鮮中央通訊社、中央電視臺等官方媒體發出消息:鮮國防委員長金正日
            已於當地時間12月17日8點30分在巡視一線工作的列車上因勞累過度而猝死。 網友在
            《鐵血網》發帖說,金正日死了,身後卻留下了一堆迷團。. 其一:根據金正日的身份與地位,
            在正常的情況下,終年都應該有貼身醫護專家組陪同,假如近來金正日身體狀況欠佳,為什麽
            還要對外出巡?這些醫護專家組的成員為什麽沒有一個人對金正日的身體近況進行正確的
            會診?並且事後也沒有人提到過醫療專家組當時的任何意見! 其二:為什麽金正日的死亡地點
            是在列車上?在正常情況下任何國家領導人幾乎都是死在醫院的病床上,或者死於家中!而
            金正日卻偏偏死於列車的包廂內,莫非金正日隨身沒有攜帶醫療專家小組嗎?而這些醫療專家
            小組的成員為什麽在金正日出現臨死前癥狀的第一時間,沒有對他進行及時搶救?然後轉入
            地方大醫院進行救治呢?難道這些醫療小組的專家們當時都不在金正日身邊嗎?那麽金正如
            當時的陪同人員就很有問題! 其三:金正日的正確死亡時間被定為巡視的列車上,這個移動
            的地點存在很多不確定的因素! 1:當時金正日身邊有哪些人在現場?這個死亡空間很小,現場
            人員很局限,是否為了演示某種內幕? 2:金正日在列車上進行過搶救嗎?如果進行過搶救
            難道連堅持到轉醫院的時間都沒有嗎?莫非金正日在火車上搶救的醫療設備及條件比正規醫院
            還好嗎?正常人不會認為金正日的專列沒有搶救時的必須用藥! 3:為什麽非要對外宣布
            第一死亡時間是在列車上?而不是在人人可見人人可以證實正規場合?正常的情況下領導人
            一旦出現生命垂危,也應該及時的送往附近的正規醫院進行搶救,哪怕是死於途中,也該由
            醫院方面的負責人出具有效的死亡證明.而草率的在列車上搶救不及時送交正規醫院而直接
            宣布死亡,這樣做不符合正常邏輯.難道說送到醫院會有什麽顧慮嗎? 4:朝鮮剛剛宣布最近
            即將試射能夠攜帶核彈頭打到美國的遠程洲際導彈 , 為什麽核計劃說停止就停止了呢?
            洲際導彈即將發射而金正日卻在試射前猝死 ,死後核計劃就變卦了呢? 5:金正日生前始終
            堅持進行核試驗 ,為什麽在金正日死後第二天就宣布與美國簽署停核計劃?為什麽在死前的
            剎那突然改變主意了?是誰在金正日死後的第二天替他簽署停核計劃 ? 6:金正日死前就有
            媒體報道 ,有一夥朝鮮軍人集體偷渡中國而朝鮮當局 竟然窮追不舍當場還擊斃兩名朝鮮
            軍人 ,難道這些偷渡的軍人知道了什麽內幕嗎?或者是這些偷渡的軍人想傳遞給中國什麽信息
            '''
        ),
    )
    assert parsed_news.category == '國際,時政'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1324310400
    assert parsed_news.reporter is None
    assert parsed_news.title == '網曝:金正日猝死幾大疑點'
    assert parsed_news.url_pattern == '2011-12-20-634655'
