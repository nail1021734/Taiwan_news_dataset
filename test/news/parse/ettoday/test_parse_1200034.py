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
    url = r'https://star.ettoday.net/news/1200034'
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
            華裔美籍導演楊紫燁拍的香港紀錄片《爭氣》,透過一個四校聯合製作、帶有融
            合教育理念的音樂劇,讓不同身心狀況與家庭背景的中學生(包括盲校視障學生),利用課餘
            集訓半年,透過藝術訓練與集體生活形塑人格,是值得研究推廣的案例。 原來香港初高中多
            是同一間學校辦學,學校被分級為Band1、Band2、Band3。不同階層的各校,再自己分出校內
            菁英班和放牛班。片中有女生因為自己比不上朋友的學校而哭泣,但也有一位胖胖的男同學
            這麼說: 「唸Band1、Band2不一定代表很好,你只會讀書,我問你,你試過打架沒有?試過玩
            樂團沒有?我問他們懂不懂怎麼搭地鐵,他們不會,他們說我司機來接我,我不懂怎麼搭車回
            家。我說那你死定了,世界末日要逃命時,你怎麼辦?」 這段反詰開朗又實際,不是出自老師
            勸導,而是他本人的自我開解。我覺得這段話一點都不酸。 爸媽讓小孩光讀書讀到中學還
            不會搭公車回家,真的好嗎?當然,喜歡階級決定論的人,會說:好。 不是光反駁明星學校就
            是對,身為Band3學生,片中一個女生說,以前覺得沒希望,但參與這齣戲之後,感覺環境對人
            的影響不是死的。尤其看到比他們條件更差的視障學生還比他們認真拼命,受到很大
            啟發。 其中一位才失明一年的學生,心態有更大轉變。從唱歌跟蚊子叫沒自信,到勇敢表現
            自己,還在片尾被選為致詞代表之一,跟爸媽說:「我只是沒有眼睛,又不是沒有命。」更逼出
            滿場的笑聲與淚光。 最讓我心有戚戚焉的,本片借助的教育形式是音樂劇,這讓一直從事音樂劇
            編劇與作詞的我,倍感親切與鼓舞。當看到本來內向怯懦或桀傲不馴的青少年,最後上台搬
            演音樂劇,唱跳不輸台灣一般劇場演員,真的很感人。 陳樂融 知名創作人、媒體人、策劃人。
            遊走於作詞家、作家、主持人、編劇、文化評論家、品牌及營銷顧問、人文心靈講師等多種角色。
            '''
        ),
    )
    assert parsed_news.category == '星光'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530056400
    assert parsed_news.reporter == '陳樂融'
    assert parsed_news.title == '紀錄片《爭氣》:用音樂劇教育青少年'
    assert parsed_news.url_pattern == '1200034'
