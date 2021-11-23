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
    url = r'https://www.epochtimes.com/b5/19/11/24/n11677348.htm'
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
            在漫長的音樂史中,「指揮」算是新興行業,約在西元1810年左右,音樂作品變得越來越複雜,
            指揮的需求也開始浮現。在貝多芬時代之前也有指揮,但沒有如此不可或缺。 著名樂評家
            萊布列希(Norman Lebrecht)在他的著作《大師的迷思》(The Maestro Myth)中寫道,
            即使現在網路上有大量現場演出的近距離特寫畫面,這個行業仍充滿神祕感。拉圖爵士
            (Sir Simon Rattle)指揮馬勒(Gustav Mahler)第二號交響曲《復活》就是其中一個
            例子。 就像音樂演出的各種分枝,指揮的工作即是「溝通」,不論是音樂上抑或是超越音樂
            的。 指揮的工作即是「溝通」 一名指揮與觀眾的交流,從他踏上舞台的第一步就展開了:
            他得讓團員在擁擠的舞台上移出一條安全的通道,並微笑地跟觀眾和演奏家們互動,也得完成
            一些音樂會的儀式(如向觀眾及樂團示意、與首席握手並敬禮)。 進行這些動作的同時,他
            還得專心思考接下來開場幾個小節,如何正確又不失音樂性地指揮。 一名合格的指揮至少
            會對一項樂器專精,而他也得對所有樂器,甚至是人聲瞭若指掌。在排練前他必須仔細讀譜,
            了解音樂的內容,很少有指揮能直接臨場識譜。 指揮的服裝會在上台那一刻就與觀眾有所
            交會,主流古典音樂會多是正式著裝,但主題音樂會就會有不同的選擇。因此即使看到扮成
            星際大戰天行者的指揮,其實也不足為奇!我曾穿一雙紅色條紋鞋上台來吸引觀眾的眼光,
            評論家還拿我跟羅馬教宗的服飾相比。 在21世紀,指揮對於介紹音樂演出,變得越來越重要
            ,但指揮終究要轉身背向觀眾(除了坐在合唱席的以外),然後讓音樂展開。 指揮肢體動作的
            意義? 與團員密切的眼神交流是演出成功的要素,而指揮那些看起來煞有其事地手臂舞動,
            又是怎麼回事呢? 這個答案一半跟數學有關,一半跟音樂有關。數學指的是為了讓團員們演奏
            在一起,指揮會精準地打出拍子,以免大家各自為政。 許多指揮用指揮棒來幫忙,也有人選擇
            不用。指揮的選擇與曲子的大小或風格都有關係。指揮會使用慣用手來打拍子,例如:我是
            右撇子,因此就是右手。 小節(bar)是寫在譜上,用來幫助演奏者計算音樂長度的記號。根據
            詮釋及樂曲「理論上的結構」,精準地呈現出每個小節的時值,是指揮主要的工作。 資深的
            愛樂者就會發現,大部分的小節都有固定的指揮方法,因拍子數量而決定(通常是2至4拍),
            由垂直跟水平拍點組成(指揮會左右或上下揮動手臂)。 一個小節的拍子越多,指揮的方式會
            越複雜,拍子的數量通常反映每小節的韻律結構(節奏感)。 幾乎所有小節都有第一拍和最後
            一拍,又稱重拍(downbeat)及弱拍(upbeat)(很少出現一小節只有一拍的情形)。重拍由
            上往下打,弱拍則反之。想像從12點鐘方向到6點鐘方向畫一條線即是重拍,往回畫就是弱拍
            。 重拍與弱拍都是演出中的視覺提示,他們確切地標示出小節及樂譜內的個別拍點。重拍與
            弱拍將音樂的線條視覺化,從數學、算術上幫助音樂順利進行。 雖然大部分曲子整首就一個
            拍號(每小節的拍子數量一樣),但卻不盡然如此,看看史特拉汶斯基(Igor Stravinsky)的
            《春之祭》(The Rite of Spring)演出影片就知道,這首名作有大量的變化拍子,常常
            改變每小節的時長,對指揮的技術與樂感是高度考驗。 揮舞的雙臂不只標示拍子,也會控制
            樂團的音量大小。在大部分的情況下,譜上需要的音量越大,指揮的動作也會變大。 指揮的
            全身都在向樂團甚至是觀眾傳達音樂的訊息,從頭到腳都影響著音樂的每一瞬間,不論是拍點
            提示、力度控制、聲響平衡抑或是樂句雕琢。 不論言語或其它方式,「溝通」才是一名指揮
            的課題。若沒有成功有效地溝通,那演奏音樂與聽音樂的樂趣,都將大大地減少。
            '''
        ),
    )
    assert parsed_news.category == '亞洲,台灣,教育,教育園地'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1574524800
    assert parsed_news.reporter is None
    assert parsed_news.title == '音樂指揮到底在「指」什麼? 專家告訴你'
    assert parsed_news.url_pattern == '19-11-24-11677348'
