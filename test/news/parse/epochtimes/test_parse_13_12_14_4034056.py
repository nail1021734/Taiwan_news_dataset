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
    url = r'https://www.epochtimes.com/b5/13/12/14/n4034056.htm'
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
            北韓領導人金正恩處決「攝政王」姑丈張成澤,被視為殺大臣、鞏固權力之舉。美聯社報導
            ,其實這種獨裁者的行為不只古代,近代也不乏其例。 史達林 前蘇聯領導人史達林
            (Josef Stalin)可以說是20世紀極權統治的典範。但布爾什維克派(Bolshevik)
            指標人物列寧(Vladimir Lenin)死後,他又花了數年才完全掌握政權。 史達林與其
            黨羽1930年底一手導演公審大戲,常常是以捏造罪名與強迫認罪的手法,將可能崛起的對手
            定罪並處決。 布卡林(Nikolai Bukharin)因為間諜罪遭到槍決,另外2位共產黨
            重要人物卡米尼夫(Lev Kamenev)與齊諾威耶夫(Grigory Zinoviev)涉嫌與
            托洛斯基(Leon Trotsky)共謀叛變而遭到處決。 托洛斯基是史達林最後一個、
            也是知名度最高的政敵。他1940年流亡墨西哥時遭人冰鑽刺腦而死,史達林13年後於
            在位時去世。 毛澤東 毛澤東則藉著文化大革命清除政敵,國家主席劉少奇可能算是他
            最想除去的目標。紅衛兵搗壞劉少奇官邸,並將他與妻子拖出來審訊。紅衛兵指劉少奇是
            帝國主義走狗,不給他治病,導致他1969年死於肺炎。 希特勒 1934年,也就是德國納粹黨
            取得政權次年,希特勒(Adolf Hitler)展開「長刀之夜」
            (The Night of the Long Knives)掃除政敵行動。被害人之一是他的頭號敵人羅姆
            (Ernst Roehm)。 羅姆是衝鋒隊(Sturmabteilung)領導人,被捕後遭到槍決。衝鋒隊
            分裂出來的納粹黨衛隊(SS)成為納粹政權無人能敵且權力最大的工具。 海珊 伊拉克
            前總統海珊2度清理政敵。復興黨(Baath Party)在海珊遠親巴克將軍
            (Ahmed Hassan al-Bakr)領導下,1968年重新取得政權。海珊擔任副手時,剪除黨內
            重要人物。 11年後,海珊逼巴克辭職,數百名復興黨與軍官遭到處決。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1386950400
    assert parsed_news.reporter is None
    assert parsed_news.title == '金正恩殺臣固權 近代不乏其例'
    assert parsed_news.url_pattern == '13-12-14-4034056'
