import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201911080011.aspx'
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

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            費玉清在台北舉辦告別演唱為歌唱生涯畫上休止符,在結尾時費玉清數度哽咽,但仍不改幽默
            本色說,「我的喉嚨管也硬了」,坦言因歌迷的厚愛,靠著歌聲走過許多地方。 費玉清的
            「2019告別演唱會」在昨天深夜劃下句點,也象徵他的歌唱事業的路途,由他親手填上了
            休止符。 費玉清在最後一段演唱後,本已要跟觀眾道別,但一聽到觀眾喊安可,費玉清立刻
            表示,最後一場確實應該多唱一點,他說,「歌手被喊安可是多大的榮幸,今天晚上真的是一
            個難得的夜晚」。 費玉清說畢竟是最後一場,「不聊聊不過癮」,與觀眾說了許多心裡的話,
            甚至還因此超過時間9分鐘,在晚間11時9分才結束演唱會,也因此要被罰款新台幣
            5萬2500元。 去年9月宣布將於今年封麥的費玉清,當時表示,本是他精神支柱的父母過世
            之後,他的生活重心沒了依靠,因此希望能夠回歸簡單的生活,好好過日子。 在台北最終場
            的告別演唱會上,費玉清數度回憶起父母,表示父親在世時曾告訴他,「年輕時應該多去一些
            地方,像台灣好像很多地方你都沒有去過,我這個年紀的人玩的地方都比你多」,他說如果早點
            注意到,應該在2年前就放下麥克風暫別舞台,好好陪伴父親。 費玉清說因此接下來希望回歸
            簡單的生活,好好過日子,他坦言這個決定也跟家人分享過,但是哥哥張菲卻不這樣認為,張菲
            對他說,「觀眾的掌聲是一種滋養,過幾年後人就不記得了」。 費玉清也說,張菲雖然這樣
            跟他講,但對於費玉清將告別歌壇,張菲也感到不捨,張菲對費玉清說,「你一定感慨萬千,
            回到家裡我煎個荷包蛋給你吃」。 費玉清坦言,因為歌迷的厚愛、不嫌棄,「(讓我)藉著
            這個歌聲的翅膀,走到了好多的地方」,他最後也呼籲觀眾,日後要是在街上遇到他,千萬
            不要害羞與他打招呼,甚至說「我們也可以喝杯咖啡好好聊聊」。 在結尾後,費玉清一連
            演唱5首安可歌曲,有「我只在乎你」、「今宵多珍重」、「何日君再來」、「但願人長久」、
            「南屏晚鐘」。在安可曲的段落中,也加碼清唱與周杰倫所合唱的經典歌曲
            「千里之外」。 期間費玉清數度哽咽,看得出要告別舞台心中也相當不捨,他在正式結束後,
            站在台上看著歌迷離場,不斷說著謝謝,然後才走入後台,也宣告歌唱生涯正式畫上休止符。
            '''
        ),
    )
    assert parsed_news.category == '重點新聞'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1573142400
    assert parsed_news.reporter == '陳秉弘台北'
    assert parsed_news.title == '費玉清告別舞台數度哽咽 歌唱生涯最後一曲謝歌迷'
    assert parsed_news.url_pattern == '201911080011'
