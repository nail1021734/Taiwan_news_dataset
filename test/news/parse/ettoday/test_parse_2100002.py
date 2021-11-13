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
    url = r'https://star.ettoday.net/news/2100002'
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
            10月13日是世界保健日,新北市政府動保處與飼主分享毛寶貝健康生活2秘訣,第一是保持
            動物活動力,每日花10分鐘時間散步,第二是避免攝取高油脂高鹽分食物,可讓毛寶貝保有
            長久健康與飼主一起快樂生活。動保處提醒飼主應依動物傳染病防治條例每年施打狂犬病
            疫苗,將可避免被罰最高15萬元罰金,並保護毛寶貝遠離人畜共通狂犬病。 中和動物之家
            獸醫師黃繼霆表示,14日同時是重陽節,維持動物活力是保持健康秘訣,動物之家動保員上班
            第一件事,觀察動物健康狀況,年齡較大犬隻會讓牠在室內自由活動,其它所內動物,今年起
            每週3次由人員帶出籠外活動,讓犬隻能有適度活動時間曬太陽,並藉由戶外散步學習社會化,
            配合訓犬師改善吠叫等行為,提高民眾認養意願,他也建議家犬每日出門散步10分鐘將有助
            動物健康發展。 第2項毛寶貝健康秘訣,毛小孩飲食方面超重要。動保處說,飲食保健須避免
            高油脂、高鹽分食物,過多蛋白質會增加肝臟及腎臟代謝負擔,應減少攝取,水果蔬菜例如
            蘋果、香蕉、木瓜等,可以適當提供幫毛寶貝強化腸胃,增加免疫力,但需注意不可過量,以免
            造成胃腸不適,更不可提供葡萄、巧克力、洋蔥跟大蒜等禁忌飲食。動保處表示,「毛寶貝
            與人一樣飲食需定時定量,配合均衡的飲食及定期運動,讓毛寶貝陪飼主健康度過
            每一天。」 動保處提醒,寵物除平日良好生活習慣外,每年亦須完成狂犬病疫苗預防
            接種,可有效防止致死率近100%人畜共通傳染病,動物傳染病防治條例規定,寵物未定期
            施打疫苗,可處3萬至15萬元罰鍰。
            '''
        ),
    )
    assert parsed_news.category == '寵物'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634104920
    assert parsed_news.reporter == '林韋辰'
    assert parsed_news.title == '每天散步10分鐘!把握「毛孩健康2秘訣」 定期打預防針超重要'
    assert parsed_news.url_pattern == '2100002'
