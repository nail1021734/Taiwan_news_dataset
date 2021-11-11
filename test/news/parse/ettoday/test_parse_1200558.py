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
    url = r'https://star.ettoday.net/news/1200558'
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
            台南市於26日確診今年登革熱境外移入第7例病例,登革熱防治中心提醒醫療院所,目前正值
            暑假出國探親旅遊之際,應加強有東南亞國家旅遊史之病患通報,方能及早啟動相關防疫機
            制。 登革熱防治中心陳怡主任表示,該病例為居住佳里區禮化里民眾,49歲男性,6月12日至
            6月18日因公務至柬埔寨及越南,於返國後6月19日才開始出現發燒症狀,曾多次就醫,直至6
            月22日開始出現紅疹,個案於6月25日再至醫院就醫,經採檢進行登革熱NS1快篩為陽性,醫院
            通報衛生單位後,於6月26日經疾病管制署確認為登革熱病例。 台南市登革熱防治中心在接
            獲病例通報後,即立刻進行住家環境孳生源巡查清除工作及住家內放置噴霧罐,並於6月26、
            27日完成工作地及住家戶內外環境化學防治措施,現持續加強巡查周圍環境清除孳生源。 因
            病例已於社區活動長達7日,個案曾至工作地及外縣市活動,若於社區遭登革熱病媒蚊叮咬
            ,容易造成社區疫情擴散,因此請佳里區禮化里及永康區永明里民眾加強「巡、倒、清、刷
            」及防蚊措施,另請周圍醫療院所提高警覺並加強通報。 登革熱防治中心呼籲佳里區及永
            康區醫療院所,針對發燒就診病患務必確實詢問病患旅遊史、職業別、接觸史與群聚
            情形 (TOCC)。並提醒院所內醫療相關人員應持續保持警覺,如發現符合登革熱通報之疑似
            病例,應立即進行通報(雖登革熱NS1快篩為陰性,仍請進行通報),並盡量安置病人住院
            (發病日前1日至發病日後5日,可傳染期共7日),俾利衛生單位及早進行相關防治作為,避免
            病毒於社區中擴散。 登革熱防治中心再次呼籲,正值暑假期間,民眾如前往登革熱流行地區
            應做好防蚊措施,穿著淺色長袖衣褲、於皮膚裸露處塗抹衛福部核可的防蚊藥劑、居住在有
            紗窗、紗門或空調設備的房舍,以降低登革熱感染之風險。返國入境時如有發燒等疑似症狀,
            應主動告知機場檢疫人員;返國後兩週內如出現不適症狀應儘速就醫,並主動告知近期旅遊史,
            以利醫師早期診斷、通報及治療。
            '''
        ),
    )
    assert parsed_news.category == '地方'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530092700
    assert parsed_news.reporter == '林悅'
    assert parsed_news.title == '南市確診第7例境外移入登革熱病例 醫療院所加強詢問旅遊史'
    assert parsed_news.url_pattern == '1200558'
