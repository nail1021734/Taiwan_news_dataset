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
    url = r'https://www.epochtimes.com/b5/19/12/15/n11724303.htm'
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
            曾遭受中共非法勞教3年、判刑4年的遼寧省營口市老邊區法輪功學員徐傳德,早於2013年
            黃曆5月17日被迫害離世,年僅46歲。 1999年7月20日,中共江澤民集團開始迫害修煉「真、
            善、忍」的法輪功學員以後,徐傳德為了為法輪功說句公道話而被非法勞教3年;2002年4月,
            在營口市勞動教養院,身患殘疾的徐傳德,仍被逼迫整日坐凳子,從早上6點到晚上9點。 2001
            期間,徐傳德和後來被中共迫害致死的林寶山、錢乃章、張樹鵬、魏立剛等14名法輪功學員從
            營口市勞動教養院集體闖出後,市委書記孟凡利指使營口市「610」(專門迫害法輪功的非法
            機構)、公安局、市國保大隊等警察對他們進行撒網似地追捕。 身有殘疾、駝背、視力在0.1
            左右的徐傳德逃出魔掌後,身無分文,幾經周折躲到鞍山市姐姐家。姐姐在當時鋪天蓋的邪惡
            壓力下不敢收留弟弟,給了弟弟點兒錢,讓他坐車到瀋陽市後再輾轉返回老邊區。可他有家不能
            回,只好躲在山上,卻被人非法構陷。 徐傳德被營口市「610」、公安國保大隊、還有老邊區
            「610」、公安國保大隊、老邊區派出所、老邊區街道辦事處等30多人圍在山上。等視力模糊
            的他發現自己被包圍時已經晚了,他遭綁架,後被非法判刑4年。 徐傳德在遼寧省本溪市監獄
            裡被金明南等十餘名人毒打,肋條骨被打折兩根。徐傳德認為監獄不是法輪功學員呆的地方,
            加上肺病也在折磨他,就申請保外就醫。由於他不能幹活,沒有被利用的價值,被允許保外就醫
            回家了。 沒有經濟來源的徐傳德只有靠撿破爛為生,傷病一直沒有痊癒,又長期處於中共人員
            的騷擾之中,於2013年黃曆5月17日含冤離世。
            '''
        ),
    )
    assert parsed_news.category is None
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576339200
    assert parsed_news.reporter == '明慧'
    assert parsed_news.title == '遼寧法輪功學員徐傳德多年前被迫害離世'
    assert parsed_news.url_pattern == '19-12-15-11724303'
