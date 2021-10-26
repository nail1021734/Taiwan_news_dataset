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
    url = r'https://www.ntdtv.com/b5/2011/04/11/a517227.html'
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
            澳洲财政部长引用经济思想家约翰?梅纳德?凯恩斯的思想理论——赤字预算,来辩解下个月联邦
            预算急剧缩减政府开支。财政部长斯万在今天先驱报发表的文章中表示,全球金融危机后私营
            部门重新健康发展,政府需要限制其开支,减少债务并返回预算盈余。 “就如在全球金融危机
            期间,我们采取正确步骤来支持经济需求,而在私人部门恢复中,正确的做法就是后退一步。”
            他写道。“这就是为什么我们首次整理出经济刺激计划时,我所采用的座右铭是:在经济低迷时
            我们是凯恩斯主义者,那么在经济复苏中我们也一样,这意味着迅速回转到有盈余。” 内阁
            支出审查委员会一直致力于为2011至2012年度预算消减开支,预算案将在5月10日下达,
            斯万先生的文章正好发表在此际。去年11月发布的财政部年中预算审查,估计政府将在本财政
            年度赤字达415亿元,明年為 123億元,在2012至2013年則盈餘31億元。 但是由於自然災害
            和強勁的澳元,使得政府把預算變為盈餘的挑戰變得非常艱鉅。政府需要花錢修復在夏季颶風
            和洪水災害中損壞的基礎設施,此外,日本地震也會限制出口。強勁的澳元消減稅收,因為
            貨幣漲價抑制出口行業利潤,以及和進口公司間的競爭。 斯萬先生和總理茱莉亞?吉拉德
            最近警告需要「強硬」措施來確保2012年至2013年的預算盈餘。斯萬先生在文章中加強這個
            信息,表達政府財政策略就如凱恩斯主義一樣,在2008年末的全球金融危機爆發時工黨使用
            大量消費刺激措施。「自經濟大蕭條的80年來,凱恩斯認為政府應避免經濟衰退,確保繁榮和
            在進步中發揮作用,這理論已變成工黨經濟事務指南,幫助我們在動蕩洶湧的大海中
            把穩托盤。」 「凱恩斯理論的核心是,政府應該在經濟衰退時增加花費,一旦經濟復甦,就應
            限制開支,預算盈餘和減少債務。」 沒有必要因夏季的自然災害而改變預算策略,因為經濟
            現發展強勁並蒸蒸日上。
            '''
        ),
    )
    assert parsed_news.category == '海外華人'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302451200
    assert parsed_news.reporter is None
    assert parsed_news.title == '澳财长警告:联邦财政预算将急剧缩减'
    assert parsed_news.url_pattern == '2011-04-11-517227'
