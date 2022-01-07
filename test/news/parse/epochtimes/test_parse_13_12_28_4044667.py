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
    url = r'https://www.epochtimes.com/b5/13/12/28/n4044667.htm'
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
            電影中食人魚攻擊人類的恐怖場景在現實生活中上演。阿根廷26號發生食人魚大舉出動攻擊
            人類的事件,超過70名泳客被咬傷,傷者包括7個小孩。 現在南半球正值夏天,因此專家研判,
            這起意外可能是連日高溫,魚群活動異常所引起的。 電影中食人魚攻擊人類的恐怖場景,
            在現實生活中上演。26號不少羅薩里奧巿的民眾趁著耶誕假期到附近的巴拉那河游泳消暑。
            沒想到河裡出現了大群食人魚,不少人大喊救命,父母聽到呼救聲急忙衝進水裡將小孩拖上岸,
            不過還是有小朋友掛彩,其中一個七歲的小女孩她的手指被食人魚咬斷一小節,傷勢
            嚴重。 這次發動攻擊的魚群屬於食人魚的近親,牙齒尖銳,性情凶猛,雖然之前就有過咬傷人的
            記錄,不過當地官員表示,這次大舉出動的情況不太正常。 而巴拉納河地區最近氣溫飆到
            攝氏38度,專家研判,連日異常高溫,使得魚類群聚到河面,因而導致了這起攻擊事件。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388160000
    assert parsed_news.reporter is None
    assert parsed_news.title == '恐怖!阿根廷食人魚 咬傷70名泳客'
    assert parsed_news.url_pattern == '13-12-28-4044667'
