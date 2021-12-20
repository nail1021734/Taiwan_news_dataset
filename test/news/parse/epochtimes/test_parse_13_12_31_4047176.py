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
    url = r'https://www.epochtimes.com/b5/13/12/31/n4047176.htm'
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
            據路透社報道,繼今年10月緬甸當局釋放了56名政治犯後,目前在押的大部分政治犯將於
            週二獲得釋放。這使得現任總統吳登盛關於年底前大赦政治犯的承諾得以兌現。預計此次
            將有230名政治犯重獲自由。緬甸當局的改革姿態贏得了國際社會的讚許。 總統特赦令於
            週一晚間在公共電視台MRTV公佈,不過並沒有說明釋放的人數。但是根據一個人權組織
            「政治犯援助協會」的說法,其中的230人將會被釋放。該組織負責人表示,將有38名服刑
            囚犯和192名等待接受審判的被羈押者將被釋放。 在緬甸,有數百名囚犯此前因為政治信仰
            而被剝奪自由。而緬甸政府也因為壓制人權而長期遭受西方國家制裁。吳登盛在2013年7月
            訪問英國時表示,從那時起到年末,緬甸將不會再有政治犯。 今年十月吳登盛前往文萊出席
            東盟峰會之際,緬甸宣佈釋放了56名在押的政治犯。 吳登盛採取的改革姿態也贏得國際
            社會的讚許,使得歐盟和美國取消了大部分制裁措施,並加強了對緬甸的援助。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388419200
    assert parsed_news.reporter == '辛民'
    assert parsed_news.title == '緬甸大規模釋放政治犯 兌現改革承諾'
    assert parsed_news.url_pattern == '13-12-31-4047176'
