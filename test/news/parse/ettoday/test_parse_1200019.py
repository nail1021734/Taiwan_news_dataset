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
    url = r'https://star.ettoday.net/news/1200019'
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
            第二屆WE愛兩岸青年短片大賽落幕,前三名的短片有兩部是動畫片,《屋子心》聚焦社會變
            遷過程中,人與物的情感變化;《平小》則探討大陸三、四線城市中愛情與鄉愁的衝突;《鮮
            蔬香烤嫩雞佐蜜漬青檸醬》片名很長,評審認為,簡單的烤雞過程,反映出人生的全部,光鮮
            亮麗的進場到最後成為盤中飧,如同人生必將走入最後的結局一般,發人省思。 得到銅獎的
            《鮮蔬香烤嫩雞佐蜜漬青檸醬》是台灣科技大學蔡辰郁的畢業製作作品。這部動畫短片利
            用卡通化的手法呈現烤雞的流程。蔡辰郁希望用單純的表達方式,讓觀眾能迅速看懂,她表
            示,為了完成這部短片,花了很多功夫和老師討論,希望大家看完之後可以有不同的想法,有
            些人覺得很可愛、或是很可憐,留給觀眾不同的想像空間。 銀獎作品《平小》導演裴俊是
            個不擅言詞的人,對影像特別熱愛,希望能透過影片表達自己的情感。故事主角平小是個猶
            豫不決的人,朋友的妻子是他心愛的對象,比他早做出離婚的決定,即便如此,平小仍舊顧慮
            很多,直到最後一幕說出「我跟你一起走」,完成對自己的救贖。導演用三、四線城市小人
            物的愛情故事為題材,表達主角雖然最終難逃宿命,仍勇敢向愛前行的正向力量。 《屋子心
            》從50部入圍影片中脫穎而出得到金獎,有別於2D、3D動畫,是一部紙片定格動畫。故事講
            述房屋的一生,與人的相遇到分離,從原本熱鬧非凡的氣氛到人去樓空的孤寂,呈現今非昔比
            的落差感。時間流逝的過程中,透過老屋「擬人化」的內心感受,將人與房屋之間的情感交
            織,傳遞時代的溫度與人文關懷。製作團隊對於「台南老屋」的議題很感興趣,在走訪民間
            探詢許多關心老屋的工作者後,發想出這部動畫短片。
            '''
        ),
    )
    assert parsed_news.category == '大陸'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530053640
    assert parsed_news.reporter == '魏有德'
    assert parsed_news.title == '兩岸青年電影人追夢 動畫短片脫穎而出'
    assert parsed_news.url_pattern == '1200019'
