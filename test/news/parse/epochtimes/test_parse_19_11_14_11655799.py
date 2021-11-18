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
    url = r'https://www.epochtimes.com/b5/19/11/14/n11655799.htm'
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
            很難相信嗎?千百年來,《易》的本義究竟是什麼一直是個懸而難解的謎,既然象數派與義理派
            兩大類的解釋都不夠令人滿意,那麼本文的標題有可能就是答案! 《禮記.禮運》篇的大同
            章節寫道:「大道之行也......,是謂大同。」其後的小康章節又寫道:「今大道既隱」;而
            《道德經》亦言:「大道廢」。也就是說,實行「大道」才能夠實現「大同」世界,但是自古
            以來,對於所謂「大道」的實際內容則因「隱、廢」而不知。 如果《易》就是「大道」,那麼
            為什麼每天在大家眼皮底下卻無所識? 那是因為詮釋的觀點問題,例如<家人>卦,若以「家人
            」之意含為「待世人如家人,則世人何必對他人巧取豪奪,反倒應該和平相處、彼此助益,那不
            就是「大同」世界的景況嗎?而《易》的六十四卦之內含真義,就是建構「大同」世界的各種
            原則與規範。 先說基本的「八卦」,其卦名為「乾、坤、離、坎、震、艮、兌、巽」,其所象
            分別是自然界的「天、地、火、水、雷、山、澤、風」。 以「火」而言,火燃起後,會循著
            可燃物向周圍擴開散離。而許多人際社會有關「火」的詞語,如火災、戰火、怒火、妒火等,
            其結果也常常可能導致人們彼此間的生離死別,因此以「離」為卦名。所以「離」卦其實就是
            在告誡人們,要注意與克制各種「火」所可能引發的別離憾恨。 類同此理,「八卦」的卦名皆
            是由其對應自然界所象之性德而推得其名。而由八單卦重成六十四易卦的過程也有其原則,
            就是所謂「易之三名」的「不易、變易、簡易」。「不易」是指由相同單卦所重成的純卦為
            相同不變,所以八純卦的卦名和意含皆與八單卦相同。 「變易」是指除了八純卦以外的五十
            六個易卦的卦名與意含都變化了,其上下卦雖由不同的單卦所重成,卻變得別異於八單卦的性質
            。而這些變異所依循的方法相當「簡易」,就是「卦、象、數」這三個法則。 六爻的形成順序
            是先有初爻,其後二、三爻,而後有四、五爻,最後有上爻。也就是說,是先有下卦,然後有上卦
            。而「卦」法則就是指由下卦到上卦的有機關聯推理。 例如<師>卦,一般記作「地水師」,其
            上卦所象為「地」,下卦所象為「水」。而「師」意指大軍,再由下卦「水」到上卦「地」的
            關聯就可以推解為,大軍相戰就像水漫大地的景況,必致災難。所以<師>卦是在告誡人們,戰爭
            是災難,應該要避免,而另外尋求其他可能的和平解決方式。 再例如<姤>卦,一般記作「天風
            姤」,其上卦所象為「天」,下卦所象為「風」。「姤」意為遘遇,由下卦到上卦的關聯為,風
            悠遊於天下,可以無所不遇,也就是「自由」。由此可知,大同世界是個尊重自由的社會,能夠
            有充分的思想、言論、結社、信仰等等眾人合意約定的自由,才是真正的大同世界。 由上述
            三法則還可推得:<咸>卦有關環境,<恆>卦有關氣候,<蒙>卦有關教育,<損、益>兩卦有關
            經濟,以及其他等等。 《易》是遠古時代流傳下來的經典,因此有可能與《禮記.禮運》篇中
            孔子所述及遠古時代的大同社會傳說有所關聯。只是古之《三易》傳至今日僅有周朝初期完成
            的《周易》尚存,更早期的《連山易》與《歸藏易》早已佚失,對於《易》之真義的比較研究
            更形困難。 透過法則性的系統化推理,解得《易》的各卦內含為包括了個人修身、人際社會
            、乃至人與環境、生態、資源等依存關係的原則與規範。這絕非巧合,可以合情合理的推想其
            原先設計就是如此。而且其範圍相當廣泛,正可對應到現今人類社會所面臨的人口膨脹、科技
            躍進、環境污染、族群繁雜、信仰有別、貧富懸殊等等嚴峻複雜的情勢,可說正是大同世界
            建構之道。 《易》有六十四卦,雖字數簡少,卻意蘊沛然,如此言簡意賅,正契合古來所言「
            大道至簡」一語。也因為是如此簡要,若可能在基礎教育中就早早將此全面性原則讓人們知曉
            ,必定會對於社會整體走向更和善健全的發展有所助益。
            '''
        ),
    )
    assert parsed_news.category == '文化網,文化百科,游藝•命理•武術,命理五行,周易八卦'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1573660800
    assert parsed_news.reporter is None
    assert parsed_news.title == '《易》就是大同世界建構之道的「大道」'
    assert parsed_news.url_pattern == '19-11-14-11655799'
