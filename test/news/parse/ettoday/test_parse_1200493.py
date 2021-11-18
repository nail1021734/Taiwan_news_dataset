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
    url = r'https://star.ettoday.net/news/1200493'
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
            《四川》長征二號丙火箭成功發射送2衛星進入軌道 西昌衛星發射中心27日用長征二號丙
            運載火箭,成功將新技術試驗雙星發射升空,衛星進入預定軌道,是長征系列運載火箭的第278
            次飛行。據介紹,新技術試驗雙星主要用於開展星間鏈路組網及新型對地觀測技術
            試驗。 《上海》上海55條惠台政策第一砲 台資醫院與醫學院產學合作 現代人除了疾病
            就醫,老齡化帶來的問題日益增加,上海發布55條惠台政策後,台資醫院與上海健康醫學院建教
            合作打響第一砲。台灣擁有健康保健、照護服務技術,未來透過醫校互相實習,催生大陸家
            醫科醫生及老人照護服務制度。同時,醫學院學生也可以透過醫院,最快在2018學年度寒假
            開始,前往台灣醫院見習。 《北京》A股資本市場對外開放全方位提速 今年6月1日,在經歷了
            曲折的過程之後,A股終於正式納入了MSCI。數據表明,隨著中國資本市場開放水平的不斷提升,
            近一段時間以來,海外資金保持此前持續流入中國市場的勢頭,正在進一步加大對於A股市場的
            配置。 《浙江》31項惠台措施再加碼 寧波對台提供上千職位 有關大陸推動31項惠台措施,
            國台辦發言人馬曉光今在新聞發佈會說明最新進度,包括上海市的55條,福建省的66條,
            廈門市的60條等。其中,寧波更釋出上千個職位,全面向台青招手。馬曉光表示,鼓勵台資企業
            在大陸主板、中小企業板、創業板上市,在新三板和寧波股權交易中心掛牌;寧波口岸採取
            「一站式檢驗檢疫」「綠色通道」等便利化措施。 《北京》200萬製造業企業入駐「雙創」
            平台 工業和信息化部最新統計顯示,截至5月底,製造業重點行業骨幹企業「雙創」平台普及率
            達71.5%,中央企業建成各類互聯網「雙創」平台121個,為超過200萬中小微企業提供創新
            創業服務。「雙創」平台正成為技術聯合攻關和人才培養的高地、資源協同與供需對接的核心
            工具。 《北京》復興號運營1週年 發送旅客4130萬人次 截至26日,復興號動車組上線運營
            滿1週年,累計發送旅客4130萬人次,單日最高客座率達到97.6%。一年來,復興號動車組以其
            安全快捷,平穩舒適,高品質的運營服務贏得了廣大旅客青睞,品牌形象深入人心,人民群眾
            旅行滿意度不斷上升。 《北京》報告:2017年中國入境遊達1.39億人次 中國旅遊研究院
            27日在北京發布的《中國入境旅遊發展年度報告2018》指出,中國入境旅遊市場特別是外國人
            入境旅遊市場,進入到了恢復增長的新通道和總體回升的新階段。報告顯示,2017年入境旅遊
            人數為1.39億人次,同比增長0.8%,其中外國人入境市場同比增長3.6%,「一帶一路」沿線
            國家活躍度明顯上升。 《北京》京張高鐵崇禮支線跨京藏高速連續梁合龍 中鐵二十局承建
            的京張高鐵崇禮支線跨京藏高速連續梁合龍。據介紹,該連續梁長185.5公尺。
            '''
        ),
    )
    assert parsed_news.category == '大陸'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530089580
    assert parsed_news.reporter is None
    assert parsed_news.title == '長征二號丙火箭成功發射送2衛星進入軌道'
    assert parsed_news.url_pattern == '1200493'
