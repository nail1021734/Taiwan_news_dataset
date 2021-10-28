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
    url = r'https://www.epochtimes.com/b5/13/8/3/n3932270.htm'
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
            新西蘭恆天然奶製品公司今天早些時候對外發佈,2012年5月在新西蘭同一生產地出產的三
            批乳清蛋白濃縮製品受到肉毒桿菌感染。有此影響嬰幼兒奶粉和運動飲料的質量。但新鮮
            牛奶,酸奶,奶酪等不受影響。 恆天然已通知相關客戶緊急調查受污染的乳清蛋白濃縮製品
            是否已進入產品供應鏈。需要時應緊急召回產品。 目前還沒有報告由此帶來的感染
            病例。 恆天然總裁Theo Spierings今天說:「食品質量是恆天然的首要。公眾健康是
            嚴肅的問題。恆天然儘可能幫助客戶將受污染的產品從市場下架,並讓公眾知道此事。恆天然
            已經和紐西蘭相關部門協調,以儘快通知海外機構。」 恆天然在今年三月發現潛在質量問題,其中一
            產品發現肉毒桿菌感染。肉毒桿菌有百多種,大多數是無害的。 這種乳清蛋白濃縮製品主
            要用於生產嬰幼兒奶粉及運動飲料。 附:肉毒桿菌: 肉毒桿菌(學名:
            Clostridium botulinum)是一種生長在常溫、低酸和缺氧環境中的革蘭氏陽性細菌。
            肉毒桿菌在不正確加工、包裝、儲存的罐裝的罐頭食品或真空包裝食品裡,都能生長。
            肉毒桿菌廣泛分佈在自然界各處,比如土壤和動物糞便中。人體的胃腸道也是一個良好的
            缺氧環境,很適於肉毒桿菌居住。 根據所產生肉毒桿菌毒素抗原性的不同,肉毒桿菌分為
            A、B、Ca、Cb、D、E、F、G這8個型,
            能引起人類疾病的有A、B、E、F型,其中以A、B型最為常見。 肉毒桿菌芽孢具有很強的抵
            抗力,在180°C下乾熱5-15分鐘,100°C 下濕熱5小時,或高壓蒸氣121°C 30分鐘,才能殺死肉
            毒桿菌芽孢。 肉毒桿菌食物中毒(clostridium botulinum food poisoning),亦稱肉毒中
            毒(botulism),是因進食含有肉毒桿菌外毒素的食物而引起的中毒性疾病。臨床上以噁心、
            嘔吐及中樞神經系統症狀如眼肌及咽肌癱瘓為主要表現。如搶救不及時,病死率較高。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1375459200
    assert parsed_news.reporter == '陶韻新西蘭奧克蘭'
    assert parsed_news.title == '新西蘭恆天然奶製品公司再出質量問題'
    assert parsed_news.url_pattern == '13-8-3-3932270'
