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
    url = r'https://www.epochtimes.com/b5/13/12/31/n4047058.htm'
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
            《教授新聞》日前挑選「倒行逆施」作為總結2013年的成語。這句成語原本被韓國的教授們
            用來批評樸槿惠總統的施政,認為,她在執行暴政。但是,相對於韓國來說,朝鮮金正恩對
            張成澤的肅清反而更接近倒行逆施。 倒行逆施出典與《史記》的《伍子胥列傳》, 原本是
            伍子胥對鞭屍譴責的辯白,原文是「吾日暮途遠,故倒行而逆施之。」 這句話後來發展成為了
            對政府暴政的批評,韓國的《教授新聞》根據對622名教授的問卷調查,將「倒行逆施」選為
            總結2013年的成語。 該《新聞》介紹說,樸槿惠總統上任至今,他所採取的政策和人事都與
            民意的期待背道而馳。倒行逆施是對樸槿惠政府政策開倒車的批評。 去年年底當選,今年2月
            就任的樸槿惠總統,在外交和對朝鮮應對方面獲得輿論的好評,支持率曾高達六成多。但是在
            國內政治問題、應對工會的罷工、和履行選舉期間承諾的福利等方面,遭到在野黨的攻擊和
            輿論的撻伐,因此才出現上述「倒行逆施」的評語。 壇國大學教授徐明濟對此表示,他說:
            「倒行逆施的確是批評樸槿惠政府的評語。但是,對於一個未滿一年的新政府,該評語未免
            有點誇張。」 韓國是一個激進和保守非常分明的社會,包括年輕人和大學生的激進團體
            主張國家對人民的福利,和工會罷工的權利;而保守陣營卻強調政府的財政健康,他們認為,
            沒有稅收支持的福利,最終將會導致國家財政崩潰。他們還主張經濟發展,要求政府制止工會
            示威。所以,上述的「倒行逆施」更多地反應了激進團體的意見。 另一方面,朝鮮本月初
            逮捕並處決二號人物張成澤。據瞭解,張成澤是領導人金正恩的姑父,曾是顧命大臣,並且還
            積極地幫金正恩接掌政權,坐穩江山。 金正恩接掌政權2年來,糧食依然短缺,物資仍然匱乏,
            在民生方面毫無建樹。所以「倒行逆施」雖然是對韓國樸槿惠總統的批評,但不少人認為,更
            適合朝鮮領導人金正恩。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388419200
    assert parsed_news.reporter == '辛民'
    assert parsed_news.title == '韓國總結2013年的成語'
    assert parsed_news.url_pattern == '13-12-31-4047058'
