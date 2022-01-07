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
    url = r'https://star.ettoday.net/news/1200029'
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
            克羅埃西亞小組最後一仗面對冰島,雖然下半場一度被冰島追平,但最終仍以2比1獲勝,小組
            取得3連勝晉級16強,這也是克羅埃西亞首次在世界盃小組3連勝。 賽前克羅埃西亞就有消
            息會以二軍陣容出賽,對阿根廷來說相當不利,因為冰島贏球,阿根廷就算擊敗奈及利亞,還
            得比淨球數。果然克羅埃西亞以替補為主體排上先發,但仍有穩定演出,上半場0比0後,下半
            場第53分鐘,巴代利踢進馬賽克軍團首個進球。 但在第76分鐘,洛夫倫禁區手球,冰島獲得
            12碼機會,操刀的古爾森踢進,1比1追平,結果第90分鐘防線被滲透,被佩里希奇踢進超前分,
            傷停時間只有4分鐘,進兩球幾乎不可能。 原本冰島還有最後一波角球攻勢的可能,但裁判
            已吹哨,宣告冰島32強止步,加上阿根廷2比1擊敗奈及利亞,D組就是克羅埃西亞與阿根廷晉
            級。 克羅埃西亞在小組賽拿下3連勝強勢晉級16強,這也是他們參與4屆世足以來,首度在小
            組拿下3連勝的表現。16強的對手將是丹麥,兩國過去交手過5次,各取得2勝2敗1和的成績,
            不過若以世界排名來看,丹麥12名高出克羅埃西亞20名。
            '''
        ),
    )
    assert parsed_news.category == '運動'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530055140
    assert parsed_news.reporter is None
    assert parsed_news.title == '克羅埃西亞宰冰島'
    assert parsed_news.url_pattern == '1200029'
