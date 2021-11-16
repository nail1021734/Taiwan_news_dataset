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
    url = r'https://www.epochtimes.com/b5/20/8/31/n12371094.htm'
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
            美國總統川普(特朗普)簽署兩項行政令,要求中國公司字節跳動(ByteDance)出售和
            剝離TikTok美國業務。中共政府上週發布新的出口限制,多家媒體報導可能會給TikTok
            收購案帶來新的障礙。週一(8月31日),美國國務卿蓬佩奧就此事談到川普政府的立場
            。 週一,蓬佩奧接受華盛頓特區新聞廣播電台WMAL的「Mornings On The Mall
             Radio Show」節目採訪,談到中共、伊朗給世界帶來的威脅、TikTok收購案,以及中共
            利用中國學生竊取美國商業和學術機密等多個議題。 上週五(28日),中共商務部對科技
            出口制定新的管制規定,增加了23項限制類條目,對21項條目的控制要點和技術參數進行
            了修改。新增限制的項目中包括:根據數據分析與人工智能互動接口技術的個人信息推播
            服務,如果要出口這些技術需要最多三十天才能得到初步批准。 隨後多家媒體報導說,中共
            新規可能給TikTok出售造成障礙,或許要獲得北京同意才可出售等等。 蓬佩奧:川普政府
            要確保美國人信息不落在中共手中 在採訪中,主持人提問說,在週末看到消息
            ,中國人(中共)已經在操縱收購,需要中國共產黨許可才可出售,「根據您的估計,TikTok
            是否會在美國被禁止?」 蓬佩奧回答說,他無法回答這個問題。但他接著表示:「我們知道
            的是:無論誰使用TikTok,我們都將禁止中國共產黨竊取你的信息,我的信息,孩子們的
            信息。我們將防止這些信息交由中國(中共)國家安全機構和中國共產黨掌握。」 「總統
            的目的不是要傷害任何一家公司,也不是要傷害想要訪問社交媒體的任何人,而是要保護和
            維護美國的國家安全。」他說。 蓬佩奧表示:「所以我不知道這將如何發展。我們看到了
            中國人(中共)在這個週末做出的決定。我們所知道的是,我們的義務是確保(美國)人民的
            數據不會落在錯誤的地方——地址、姓名、健康信息、面部識別數據集——所有這些億萬美國
            人的信息都是中國共產黨希望擁有的。」 「我們將竭盡所能,以防止他們(美國人)遭受
            這種(個資被盜)痛苦。總統發布的有關技術的行政命令(其中包括TikTok)是其中的核心
            部分。」他說。 中共竊美知識產權 再將產品賣回美國 接下來,蓬佩奧被問有些美國教授
            使用聯邦經費進行研究,然後將他們的研究成果送給中共政府,因為中共政府會給
            他們個人錢,蓬佩奧回答說:「這很瘋狂。」 蓬佩奧說:「然後,它們(中共)轉過身來接手
            這些數據,用它來開發產品,然後補貼這些產品並將它們賣回美國——諸如AI機器學習軟件
            ,像TikTok這樣的公司,這些數據等事宜是它們通過竊取美國知識產權獲知的。」 國務卿
            是在暗示中共商務部出台的技術出口限制,但很多技術是竊取美國知識產權所得。 蓬佩奧
            接著說,「因此,我們進行了全面的應對,包括反情報團隊、聯邦調查局、司法部共同
            努力,還有我們在外交和經濟方面的工作,正如你看到總統提出的要求一樣,這是第一次要求
            與中國達成合理、對等的貿易協議。當然,還有很多工作要做,但川普總統非常重視。」
             8月14日,川普總統簽署行政令,以TikTok可能存在損害美國國家安全的威脅為由,下令
            字節跳動必須在90天內放棄其此前針對美國「Musical.ly」的收購併剝離其資產
            。「字節跳動」公司之前將其中文影片分享應用程序與「Musical.ly」合併後在美國
            推出了TikTok。 8月6日,川普簽署行政令,將在45天後禁止美國司法管轄的任何人或
            企業與TikTok母公司進行任何有關TikTok的交易。 目前有意收購TikTok在美國
            、加拿大、新西蘭和澳大利亞業務的買家包括微軟(Microsoft Corp)
            、沃爾瑪(Walmart Inc.)、甲骨文(Oracle Corp),以及推特等。
            '''
        ),
    )
    assert parsed_news.category == "北美新聞,美國經濟"
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1598803200
    assert parsed_news.reporter == "蘇靜好"
    assert parsed_news.title == '中共新規阻TikTok出售?蓬佩奧談川普立場'
    assert parsed_news.url_pattern == '20-8-31-12371094'
