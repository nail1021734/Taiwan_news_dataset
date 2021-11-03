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
    url = r'https://star.ettoday.net/news/1200387'
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
            打卡拍照熱潮正夯,為了吸引旅客,許多觀光業者紛紛發揮巧思,無論是實現自己的夢想,或
            是因為擁有得天獨厚的地理優勢,結合夢幻的童話風格打造民宿、拍照景點,成為網友熱門
            討論話題。想要拍出彷彿置身在童話世界中的歐風美照不用出國,全台就有3處蘑菇屋景點,
            不但好拍,更有機會能實際入住,享受住在童話故事裡。 新竹 竹東動漫園區 以動漫為主題
            的竹東動漫園區,開幕後就成為內灣地區的觀光亮點,除了不定時有不同漫畫主題限定活動外,
            園內各處的造景也超好拍!其中充滿童話色彩的蘑菇屋更是必拍地標之一,搭配周邊隨著季節
            不斷變化的花海、裝置藝術,讓整個園區就像是走進歐風童話世界中一般,是大人小孩都適合的
            玩樂好去處。 地址:新竹縣竹東鎮雞林里東林路196-1號 苗栗 南庄蘇維拉莊園 想暢遊莊園
            不須遠赴歐洲,與大自然相伴的「蘇維拉莊園」座落苗栗南庄山上,結合景觀餐廳與民宿,
            依山而建的木造歐風建築,外觀相當吸睛,繼2017年打造號稱全台最長的75公尺抿石子溜滑梯
            成為打卡亮點後,現在再在園區內打造蘑菇屋造型民宿,讓人彷彿置身在童話世界般。 可愛的
            蘑菇屋民宿均走粉嫩系列,共分為4人、6人與8人房,且每棟均為樓中樓設計,圓胖的蘑菇造型
            建築外觀,加上夢幻童話風的造景妝點,讓整座莊園夢幻程度再升級! 地址:苗栗縣南庄鄉
            田美村16鄰四灣92號 花蓮 花見幸福民宿 被網友暱稱為「蘑菇屋」的花見幸福莊園,是主人
            為了一圓兒時的公主夢,特別在自家土地上打造出全台獨一無二的「蘑菇屋」,隱身在樹林、
            湖泊,紅白配色的蘑菇屋相當可愛、夢幻,彷彿把童話故事中白雪公主與七矮人的家搬到現實
            世界。 獨棟的蘑菇屋,擁有自己的庭院、停車位,最多可以住4個人。一走進蘑菇屋,樓中樓的
            設計,裡面備有白雪公主、小王子、超級瑪莉的衣服可供旅客換穿,滿足公主夢!走上樓梯,
            二樓有兩張大床,還配有投影設備,提供白雪公主、藍色小精靈、冰雪奇緣的電影,彷彿走進
            童話世界。
            '''
        ),
    )
    assert parsed_news.category == '旅遊'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530079680
    assert parsed_news.reporter is None
    assert parsed_news.title == '夢幻童話世界就在台灣!全台3座「蘑菇屋」好拍還能入住'
    assert parsed_news.url_pattern == '1200387'
