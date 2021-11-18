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
    url = r'https://star.ettoday.net/news/1200521'
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
            耀眼的陽光灑進房間,沒有時間壓力的週末早晨,正是好眠一整夜,體力恢復滿格的時刻。起
            床後與戀人來個久違的Morning Kiss,來點激情口味的麥片,今天的早午餐,絕對給你超乎想
            像的開胃! 1.Morning sex 是男人的共同嚮往 根據調查顯示「早上6點到9點是男人性慾的
            高峰期。」以生理觀點來說,男性荷爾蒙睾丸酮分泌最多的時間在早晨,這也是男人早晨總
            是堅挺Get Ready的原因(羞)。 如果妳特別在意自己的口氣、髮型、形象問題,不妨與心愛
            的男人來一場「浴室性愛」,充滿香氣的甜蜜氛圍,宛如成人世界的DisneySea,讓人徹底擺
            脫夜晚的疲憊感,用獨處的時光好好點綴迷人的早晨。 2.晨間運動一舉兩得 別以為激情的
            後遺症,會讓接下來的美好假日活力打折,Morning sex原理與清晨運動的效果相同,可以讓
            你一整天精神奕奕! 最重要的是,愛愛60分鐘等同於慢跑30分鐘所燃燒的卡路里,把健身的
            樂趣搬到床上,幫助你將身體的注意力從飢餓感轉移到情慾的美好,有效降低食慾,激情與瘦
            身好處兼得,與另一半共同享受吧! 3.擦上高潮腮紅,擁有素顏好氣色 高潮能讓一個女人變
            得更美、更性感。激情過後,女生的臉頰會散發出自然紅潤的好氣色、由內而外透出絕美的
            蘋果肌光澤感。 一枚「最天然的化妝品-高潮腮紅」即刻入手,再高貴的化妝品牌都無法
            100%複製這種美,妳絕對會愛上鏡子裡素顏的自己! 4.半夢半醒之間,___比咖啡更醒腦 想像
            一下,熟睡中的妳突然被男人緩緩地從背後擁抱。他的手掌開始一點、一滴的化身為史上最
            銷魂鬧鐘,侵入妳私密赤裸的領地... 妳優雅的呻吟是他耳邊最甜的糖果,他的喘息聲是妳
            身為女王奪下的首等獎勵。Morning sex不只能減少生活壓力,也能阻止大腦焦慮的反應、
            增強免疫系統、讓腦下垂體與松果更為活躍,醒腦效果比咖啡更有效! 5.情侶間越愛越深的
            終極秘密 放點輕柔的音樂,令人期待的Morning sex,此刻的我們遠離酒精作祟的草率性愛
            、沒有工作的沈重壓力帶來的疲憊感,腦袋沒有雜念打擾、得以將注意力專注在「性愛裡最
            單純的小美好」。 窗外光線相襯,他性感的肩線與肌肉更有魅力,最喜歡的姿勢與溫柔愛撫
            通通都有了絕對充足的時間體現,我們願意為了彼此賴床,舒緩感情裡起伏的每個辛苦時刻。
            '''
        ),
    )
    assert parsed_news.category == '健康'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530981300
    assert parsed_news.reporter is None
    assert parsed_news.title == '盡情吃我吧! 「晨間愛愛」5好處...做1小時就瘦了'
    assert parsed_news.url_pattern == '1200521'
