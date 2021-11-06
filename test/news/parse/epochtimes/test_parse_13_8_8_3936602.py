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
    url = r'https://www.epochtimes.com/b5/13/8/8/n3936602.htm'
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
            澳洲《新聞週刊》(News Weekly)八月三日登載澳洲全國公民委員會主席彼得•維斯特摩爾
            (Peter Westmore)的文章,標題為〈對法輪功的迫害是群體滅絕罪
            (Persecution of Falun Gong is genocide)〉。 文章說,最近在澳大利亞和
            世界各地都在舉行集會,抗議中共政權長達十四年對法輪功的迫害。以下是維斯特摩爾於
            七月二十日在墨爾本城市廣場舉行的集會上的發言: 中國是一個有著數千年歷史的
            文明古國。我曾去過中國,發現那裏的人們禮貌、友善、勤勞,並對在世界其他地方正在
            發生的事情非常感興趣。同樣的,很多中國人來到澳大利亞定居。我很高興你們來到這裡,
            把你們的禮物帶到了這裡,及你們本身的存在,豐富了我們的國家。 然而,中共政權在繼續
            虐待中國人民,迫害那些有勇氣呼籲言論自由、信仰自由及尊重人權的人們。人權無國界、
            人權觀察等西方的非政府組織,在持續記錄著中共對人權的踐踏。 中共政權在過去六十多年
            中沒有進行過一次選舉,因為那個政權是由中共控制的。 儘管中共聲稱有數千萬的黨員,但是
            它本身不是一個民主的組織。它是一個自我延續
            的寡頭政治,從最高層開始運行。它自一九四九年奪取了這個國家的政權以來,就從來沒有
            放鬆過權力。 對法輪功修煉者的迫害是中共鎮壓政策的一部份。相對而言,在西方很少談
            論這個。您可能會問為甚麼會這樣。 在我看來,我們自己的政府,例如外交部和外貿部,擔
            心得罪中國,因為中國是澳大利亞最大的貿易夥伴。媒體的沉默,可以部份歸因於媒體專注
            於當地的問題。發生在遙遠的國家,如中國、朝鮮和越南的事件,讓他們感到太遙遠以致不
            感興趣。 但我認為,澳大利亞的媒體也希望在中國保持及擴大它們的存在。他們知道,一直
            批評中共政權的人權記錄將導致北京對他們施加限制,就像北京限制互聯網、限制博客,監
            禁那些批評其人權記錄的記者們那樣。 在所有領域,中共政權的人權記錄都是駭人聽聞的,
            這應當受到國際關注。它不再僅僅是中國的「內政問題」。 中共政權迫害法輪功,證據確
            鑿。同樣清楚的是,被監禁的法輪功修煉者遭受了最令人毛骨悚然的對待,包括未經審判被
            關進勞教所,及被殺害,僅僅是為了獲取他們的腎臟、肝臟、心臟、肺和眼角膜等器官。 中
            共強制摘取人體器官駭人聽聞的做法已被加拿大前內閣成員大衛•喬高(David Kilgour)和
            加拿大人權律師大衛•麥塔斯(David Matas)在他們開創性的報告中所記載。該報告《血腥
            的活摘(Bloody Harvest)》在互聯網上有,並已出版成書。 直到今天,中共仍在變相地繼續
            逮捕、監禁和殺害法輪功修煉者。 對於我們這些不是中國文化或中國這個民族的人們,我
            們覺得有義務與我們的中國兄弟姐妹們站在一起,要求結束這場可怕的迫害。
            '''
        ),
    )
    assert parsed_news.category == '國際要聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1375891200
    assert parsed_news.reporter is None
    assert parsed_news.title == '澳媒:對法輪功的迫害是「群體滅絕罪」'
    assert parsed_news.url_pattern == '13-8-8-3936602'
