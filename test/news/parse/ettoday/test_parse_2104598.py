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
    url = r'https://star.ettoday.net/news/2104598'
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
            今年彩虹10月,台灣同志諮詢熱線與Facebook合作,推出「出櫃夥伴相談室」系列活動,
            更打造「出櫃夥伴相談室」Messenger 聊天機器人,以及Instagram好友相挺濾鏡。
            其中聊天機器人可協助用戶盤點自己的狀態與條件是否適合出櫃,獲得建議、提醒等,讓同志
            在出櫃的過程得到溫暖的指引與陪伴。 「出櫃夥伴相談室」Messenger 聊天機器人
            由 Sanuker 團隊協助打造,進入相談室後,可以一步一步:1.盤點自己的狀態與條件是否
            適合出櫃。2.準備針對不同出櫃對象的風險與挑戰。3.獲得三種出櫃方式的建議與提醒
            。 熱線表示,雖然還無法做到即時線上真人諮詢,仍然相信透過聊天機器人,能夠將熱線針
            對出櫃議題的經驗帶給同志社群,並從社群中真實的出櫃故事獲得更多支持。 熱線與
            Facebook也共同策劃《出櫃相談室》影片,邀請 LGBTQ+ 社群創作者夫夫之道、
            阿卡貝拉、昆蟲擾西 吳沁婕、主持人凱莉,以趣味問答的方式輕鬆暢談出櫃經驗,幫助
            同志族群及其親友共同更理解過程中可能遇到的挑戰。影片將於10月25日在Facebook、
            同志熱線、創作者們的 粉絲專頁正式上線播出。 今年同志大遊行因疫情改為線上舉辦,
            在《出櫃相談室》合作之外,熱線更邀請品牌共同響應,串連Facebook與渣打銀行,以
            三對同志伴侶的真實故事拍攝短片,詮釋「理解愛,家就在」的精神,在渣打銀行粉絲專頁上
            鼓勵大眾共同創造多元共融的友善環境,在多元性別議題上一起勇敢發聲。
            '''
        ),
    )
    assert parsed_news.category == '生活'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1634620920
    assert parsed_news.reporter == '林育綾'
    assert parsed_news.title == '私訊機器人盤點出櫃條件!同志熱線合作臉書推「出櫃夥伴相談室」'
    assert parsed_news.url_pattern == '2104598'
