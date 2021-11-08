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
    url = r'https://www.ntdtv.com/b5/2013/03/25/a869138.html'
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
            全民公投我必勝 中國最窮乞丐PK中共黨魁。劉紅霞,我是遭受中共腐敗最殘酷的
            維權者,對當局的腐敗理解的最深刻。自己是被中國腐敗強迫變為乞丐,可在中國這片
            國土上,無論我採取何種方式維權都沒有用。反而結果是犯罪者逍遙法外、維權者坐牢坐監!
            乞丐PK中共黨魁的原因是我的訴求文章,在國內遭到百度公司屏蔽,我的訴求各部委
            不予理睬,我反抗地方來威脅,我面對活生生的搶劫、面對貪腐無度...... 劉紅霞願意PK
            中共黨魁,願意改筆名為中國自由黨,願意跟習近平來競選。當然前提是全民公投,在中共
            把選舉權交還給中國民眾後;另外是新聞自由,開放報禁、網禁。劉紅霞僅自己一人,而
            習近平總書記身後有8000餘萬中共黨員。我不怕,我的親身經歷就是中共當局殘忍的最好
            證據。我願意勇敢地站出來挑戰習總書記,當然是被中共腐敗逼迫的。我不願意再下跪、
            不願意再祈求、不願意再向腐敗妥協...... 習總書記反腐阻力大尊敬的習總書記,即便
            是我要PK您,也是對你懷著萬分崇敬的心情,雖然我遭受貴黨腐敗的襲擊幾近死亡。我要
            PK您,也只是想讓您明白腐敗對我的傷害,請您治療好自己的“遠視病”不能只看到老農家
            燈光昏暗,也得看到我的人權狀況!僅僅一事,您面對的反腐阻力就有金水丁配傑、
            鄭州黃保衛​​、河南秦玉海、公安部劉金國、中央政法委孟建柱,還有法院系統、檢察院系統
            、政府系統等等。更別說與筆者有相似心境、處境的無數人...... 習近平總書記,
            您知道嗎?當群眾維權開始,就面對的不是一個人而是一個國家機器,您知道那是一種什麼
            心情嗎?是的,你的反腐言論讓我在內的全國百姓都很高興,但我們需要看到實際的行動。
            我們河南方面把洛陽裸女放入看守所、多次揚言要再把我放入勞教所三年。我冤枉、
            真的冤枉!在中國的境地內居然找不到一塊清明之地,讓我在內的全國訪民訴冤。如果
            您願放開言論,讓新聞自由,沒有報禁、網禁,我願意做一次陪襯和你來一次公平競爭,
            看我的才能到底能不能做國家主席。
            '''
        ),
    )
    assert parsed_news.category == '大陸專題,中國人權'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1364140800
    assert parsed_news.reporter is None
    assert parsed_news.title == '中國最窮乞丐女士PK中共黨魁'
    assert parsed_news.url_pattern == '2013-03-25-869138'
