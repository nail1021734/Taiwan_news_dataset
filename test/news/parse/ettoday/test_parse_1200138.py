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
    url = r'https://star.ettoday.net/news/1200138'
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
            南澳阿得雷德46歲的單親媽媽麗莎(Lisa Bridger)遭到許多網友攻擊,因為她還在餵母乳給
            7歲的兒子伽斯(Chase),她說,孩子患有自閉症,在哺乳的過程中能得到安全感,她對於自己
            的舉動感到自豪。儘管分享溫馨的理念,但麗莎卻被不少家長指責是在「虐童」。 據《每
            日郵報》報導,麗莎育有7歲的伽斯與4歲的菲尼克斯(Phoenix),她總共生下5名孩子,自從她
            公布自己還在餵7歲兒子母乳後,她被用「虐童」、「戀童」等言詞辱罵。但她強調,母奶能
            提供健康益處給孩子們,幫助提升他們的免疫系統,對抗疾病,「男孩們只感冒過兩次,他們
            從沒服用抗生素。菲尼克斯有乳糖不耐症,他不能喝太多牛奶,所以他喝我的奶,那給了他鈣
            和鐵。」 自有一套育兒方針的麗莎說,即使遭受批評,她仍會繼續哺乳,直到兒子主動拒絕
            的那天。她說,那些罵她的人們,完全不懂親餵的好處,不然就是自己不能餵,感到內疚而把
            氣出在她身上,「我孩子的舒適度是最重要的。」 麗莎形容,如果她的孩子走過來詢問「媽
            媽,可以給我一個擁抱嗎」時,她回答「不,你現在長太大了,你不能抱抱」,這樣的回應宛如
            拒絕餵奶,她實在不忍心推開兒子。 其實,麗莎選擇一直餵母乳,除了考量到孩子的身體狀況,
            也是注意到伽斯跟別的孩子不太一樣,像是他不願意留在嬰兒車裡,不喜歡全身緊抱,但特別
            著迷哺乳的過程,「除非我餵他,否則他就會歇斯底里。」 伽斯與弟弟都患有自閉症,為了
            安撫他們的情緒,麗莎通常會在睡前餵奶,希望帶給他們安全感,而在外面時,只有伽斯大崩潰,
            她才會考慮到哺乳。這名母親坦承,先前在英國度假時,有幾名路人看到她在餵奶,都稱讚
            「很棒」;但隨後有名社工表示,「你是在虐待兒童。」 麗莎無奈表示,網路上有很多酸民,
            指點別人的家務事。她強調,除了哺乳,她也有準備其他策略來應對伽斯的自閉症,包括飼養
            小動物、練習呼吸等,目前,她在家教導伽斯的學業,孩子表現很好。 根據世界衛生組織建議,
            孩子出生6個月內,應餵哺母乳,接下來母奶搭配固體食物再2年,期間可隨著母親與嬰兒的需求調整。
            '''
        ),
    )
    assert parsed_news.category == '新奇'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530070020
    assert parsed_news.reporter is None
    assert parsed_news.title == '只感冒兩次!男童7歲還吸母乳 媽被轟「虐待」:我在給安全感'
    assert parsed_news.url_pattern == '1200138'
