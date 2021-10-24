import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.ntdtv
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/30/a639270.html'
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
            比利時社會黨魁迪賀波5日就任總理,終結541天無政府的歹戲拖棚。有了政府的比利時順利
            推展財政改革,展現好的開始,但來年的挑戰依然艱鉅。 迪賀波(Elio Di Rupo)坦承自己
            出櫃,加上獨特的紅領結造型成為媒體焦點,不過亟欲有作為的政治領袖,還是在意政績能否
            受到關注。 雖然他就任前兩天,以及就任兩週後,比利時工會2度發動罷工,抗議政府打算
            提出的明年度預算案,將刪減110億歐元(約新台幣4312億元)社會福利經費,卻絲毫沒有
            影響他推動財政改革的決心。 尤其歐洲聯盟正積極研議財政協議,規範各會員國財政紀律
            之際,迪賀波政府主導的預算案,硬是把政府預算赤字降至佔國內生產毛額(GDP)的2.8%,
            符合歐盟成長與穩定公約要求,會員國預算赤字不得超過GDP3%的規定。 對照希臘與法國
            因實施財政緊縮,民眾走上街頭爆發警民衝突,比利時的財政興革在平穩中逐步推展,展現
            令人耳目一新的領導能力。 此外,由於比利時遲遲無法籌組政府,國際信評公司如標準普爾、
            惠普曾質疑恐有政情不穩之虞,相繼調降比利時的信評,而迪賀波就任後發行的10年期債券
            殖利率,由11月接近6%的高點,降至4.02%。 而一片新氣象的氛圍中,來年迪賀波面臨的
            挑戰依舊嚴峻。特別工會組織仍不滿刪減社福經費的財政改革,揚言不排除發動更大規模
            罷工,考驗迪賀波如何求取社會和諧與財政平衡的智慧。 境內的德克夏(Dexia)銀行因
            無法招架歐債危機衝擊,10月間向政府求援尋求紓困,另一家銀行KBC也因股價大跌而傳出
            財務堪慮,金融業的燙手山芋也是迪賀波面臨的難題。 歐盟統計局公布的資料顯示,今年
            第3季比利時的經濟成長率是零,預估來年僅有0.8%,活絡疲軟的景氣及提振比利時經濟的
            活力,並不容易。 加上主張國土分裂的新法蘭德斯聯盟(NVA),並未加入迪賀波領導的
            聯合政府,如何調解朝野之間的角力與對抗,也是迪賀波得克服的難關。 有了政府的比利時,
            在財政改革等方面出現好的開始,但是來年的政經情勢依舊嚴峻,迪賀波仍得步步為營。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325174400
    assert parsed_news.reporter is None
    assert parsed_news.title == '比新政府仍面臨挑戰'
    assert parsed_news.url_pattern == '2011-12-30-639270'
