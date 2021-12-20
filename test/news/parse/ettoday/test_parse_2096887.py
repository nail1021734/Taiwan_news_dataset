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
    url = r'https://star.ettoday.net/news/2096887'
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
            華特迪士尼公司的線上影音串流服務「Disney+」將於11月12日正式登台,屆時台灣將與
            香港、南韓等亞洲地區同步上線。Disney+在8日舉辦在台上市記者會,公布收費細節和
            相關內容。 記者會由Sandy(吳姍儒)主持,記者會上也宣布台灣訂閱價格,為一個月
            270元、一年2790元,一年的價格大約是9張電影票的價錢,並支援同時四台裝置上線。內容
            除了迪士尼近期的電影外,也會有《小姐與流氓》等過去的經典動畫和電影。漫威總裁
            凱文費吉也透過視訊,與台灣媒體連線。 Disney+內容除了迪士尼外,還包含皮克斯、
            漫威、星際大戰、國家地理頻道和Star Channel。包括海莉史塔菲德、《叢林奇航》
            男女主角巨石強森和艾蜜莉布朗,都透過VCR和台灣觀眾打招呼。包含觀眾期待已久的
            《洛基》等漫威系列影集、《星際大戰》首部影集《曼達洛人》等,也都會在台上架。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1633660680
    assert parsed_news.reporter == '蕭采薇'
    assert parsed_news.title == 'Disney+登台價格確定!9張電影票價看一年 同時4裝置上線'
    assert parsed_news.url_pattern == '2096887'
