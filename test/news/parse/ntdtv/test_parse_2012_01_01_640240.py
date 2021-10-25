import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2012/01/01/a640240.html'
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
            菲律賓民眾狂歡作樂迎接新年,衛生官員今天表示,全國有近500人因爆竹或流彈而受傷。
            首都馬尼拉一處貧民窟因爆竹引發火災,燒燬30棟房屋,而爆竹的濃煙還影響機場航班。 馬尼拉
            地區民眾徹夜燃放鞭炮與煙火,全市被濃厚的煙霧籠罩,宛如霧都,視線只有數百公尺,也迫使
            國際機場關閉跑道,十餘航班受到影響,包括2架來自美國的班機。煙霧到早上9時才散去。 衛生
            部監控中心表示,全國迎接新年之際,各醫院收治454個因爆竹而受傷的傷患,有些人的傷勢有
            生命危險。許多傷者是兒童和飲酒過量的成人,他們都無視政府的警告。 衛生部長歐納
            (Enrique Ona)說:「我看到一個小孩眼睛被鞭炮炸到,他以後可能提早罹患白內障,這些
            傷害會導致身心障礙,對勞動謀生能力造成重大影響。」 兩家醫院回報,傷者中有兩名兒童
            手受重傷,可能必須截肢。 雖然警方反覆宣導,使用武器者會遭囚禁,但還是有人亂開槍,至少
            18名民眾因而受傷。 菲律賓民眾大多信奉天主教,但仍有人很迷信,包括相信巨大聲響能
            為新的一年驅除惡靈與厄運。
            '''
        ),
    )
    assert parsed_news.category == '國際'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325347200
    assert parsed_news.reporter is None
    assert parsed_news.title == '菲人狂歡迎新年 爆竹傷近五百'
    assert parsed_news.url_pattern == '2012-01-01-640240'
