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
    url = r'https://star.ettoday.net/news/1200403'
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
            瘋言瘋語: 標準商業電影,劇情有驚喜,節奏明快,視覺用心,整體感是好看的,電影語言強非
            普通商業片,雖然沒有太多的舖艮,但信任的內涵稍微淡薄了些,結局是個漂亮的安排,好看
            。 很喜歡這部電影雪景安排的部分,有強大的電影質感而非電視也可達到的劇情片,雖然有
            猜到結局,但仍不失精彩連連,攝影鏡位視覺語言高強的好作品。 劇情大綱 深入亞洲最大
            販毒組織,追擊操控一切的幕後黑手! 在一場可疑的爆炸事件後,長期鎖定販毒組織的刑警
            元浩(趙震雄 飾)面前,突然出現了被組織拋棄的前組員「樂」(柳俊烈 飾)。在眾人的幫助
            下,他們見到了亞洲毒品市場的大人物陳河霖(金柱赫 飾),以及隱藏於組織中的角色「布萊
            恩」(車勝元 飾)。面對這龐大的販毒組織,元浩雖然掌握了足以扳倒整個組織的關鍵線索,
            但整起事件背後,似乎隱藏著巨大的陰謀......
            '''
        ),
    )
    assert parsed_news.category == '名家'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530491400
    assert parsed_news.reporter == '賴賴'
    assert parsed_news.title == '信徒 殺人償命的鐵道理'
    assert parsed_news.url_pattern == '1200403'
