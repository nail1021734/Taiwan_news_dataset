import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201903240113.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            中華人民共和國主席習近平21日至26日訪問歐洲,同時中華民國總統蔡英文出訪南太平洋,
            兩岸領導人不只同日出發,也剛好都一次走訪三國,分庭抗禮拚外交的意味濃厚。 不過
            兩岸領導人走訪友邦,傳遞出截然不同的氣氛。中國「大國外交」風風火火,出發之前,
            已引起美國和歐盟高度警戒,美國公開警告義大利加入中國「一帶一路」提案的風險,
            歐盟各國也破天荒共同定調新的中國政策,把中國視為
            「經濟競爭者」與「體制對手」。 相對蔡總統出訪則充滿與友邦「搏感情」的人味,
            帛琉總統雷蒙傑索(Tommy E. Remengesau, Jr.)親自駕船帶她參訪海豚灣,她戲稱
            教她開船的雷蒙傑索是「老師」,當海豚把水花濺到蔡總統的褲腳,雷蒙傑索也親切地替她
            擦拭。 從現實主義角度衡量,習近平今年第一次出訪選擇歐洲極具戰略意義。雖然
            義大利總理說中義簽署的備忘錄沒有實質法律約束力,但義大利仍是第一個附議「一帶一路」
            政策的G7國家,被視為中國以新絲路進軍歐洲的跳板。 但也正因中國的戰略企圖心太明顯,
            消息一出,在義大利政壇就掀起「疑中派」強力反彈。 組成義大利聯合政府的兩大政黨
            為此鬧翻,南義大黨「五星運動黨」支持與中國合作,北義大黨「聯盟黨」主席、
            義大利副總理薩維尼(Matteo Salvini)卻醜話說盡,他除公開嘲笑中國沒有自由市場,
            揚言義大利反對中國殖民,還直接拒絕出席歡迎習近平的總統國宴。 為了緩和劍拔弩張的
            輿論氛圍,習近平訪歐前夕,曾試圖為這趟國是訪問添加人情味。 官方媒體「人民日報」
            19日特別在頭版放了一封習近平親自回給羅馬中文學習生的信,營造親民形象,隨後習近平
            又在義大利第一大報投書一篇「東西交往傳佳話、中義友誼續新篇」,強調中義關係不只是
            經貿合作。 然而在習近平訪義獲得的高規格接待背後,還是處處可看出兩國間的
            相敬如「兵」或「冰」。義國總統馬塔雷拉(Sergio Mattarella)除強調絲路必須是
            「雙向的」,也呼應人權團體的要求,在習近平面前提了人權。習近平與
            義總理孔蒂(Giuseppe Conte)簽的備忘錄,內容更完全是條列式的
            「在商言商」。 反觀蔡總統在南太出訪,暢談的是生態復育、氣候變遷、跨國醫療農業
            合作等,台灣關注的全球議題,早已超出了狹隘的雙邊利益關係。 大、小國的定義
            或許取決於客觀政治經濟實力,視野的大小卻未必,小國也可以有大國胸襟。中國每逢出訪
            必重申「一個中國」,此次訪義也不例外,但對比兩岸領導人出訪的內涵與氛圍,一個大而霸,
            一個小而美,正好可印證兩岸的思維差距已不可以道里計。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1553356800
    assert parsed_news.reporter == '黃雅詩羅馬'
    assert parsed_news.title == '兩岸領導人分頭拚外交 大而霸對上小而美'
    assert parsed_news.url_pattern == '201903240113'
