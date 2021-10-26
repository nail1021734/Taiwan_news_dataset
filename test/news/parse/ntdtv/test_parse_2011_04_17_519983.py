import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/04/17/a519983.html'
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

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            17日下午,陽光普照,馬來西亞退黨服務中心來到吉隆坡熱鬧的購物區,與民眾和游客們一起
            慶祝9300萬中國人脫離中共。 退黨慶祝活動一開始,絡繹不絕的行人馬上被天國樂團的
            開場演奏所吸引,很多游客和民眾高興的拿起相機拍照和圍觀。 接著,馬國退黨服務中心義工
            和支持者在集會現場面對大路舉起“國際法庭起訴江澤民等酷刑罪群體滅絕罪”、“天滅中共,
            天佑中華”、“中共不等於中國,中國不等於中共”、 “《九評》解體共產黨;9300萬人退出
            中共”、“中共假惡鬥危害全人類;讀九評明真相拋棄中共”等,中文、馬來文、英文的
            橫幅。 退黨服務中心發言人彭先生在集會中呼籲可貴的中國人為了平安和美好的未來,退出
            中共及其相關組織。 他說:“三退保平安的例子很多,例如在2008年汶川地震發生時,北川
            中學初中一個畢業班正在課堂外上體育課,體育老師是法輪功學員,在危急中他告訴學生只有
            明白真相、退團退隊才能保命。全班二十三個學生明白真相後,全部鄭重聲明三退,結果
            全班學生在地震中成功逃生。” 彭先生鼓勵還沒有閱讀“九評共產黨”一書的人們,應當仔細
            閱讀來了解中共的邪惡。他說:“當了解到中共在剝奪信仰自由的權利、虐殺和活摘法輪功
            學員的時候,你是否能從道義上站在人權和正義的一邊呢?是的,茫茫人海中,就有這樣清醒而
            勇敢的人群,在了解真相後,破除了共產邪靈多年來的思想禁錮,用真名或化名公開聲明退出
            中共黨團隊。” 一場由《九評共產黨》引發的波瀾壯闊的“三退”大潮,近七年來在中國迅速
            發展,至今已有接近9300萬各界人士退出中國共產黨、共青團、少先隊(三退),其中包括很多
            中共高官、軍人和民眾。與此同時,這場精神覺醒大潮也得到更廣泛的國際社會關注與支持,
            很多國家的政要和民眾紛紛加入聲援三退、唾棄中共的行列。
            '''
        ),
    )
    assert parsed_news.category == '九評及退黨,九評及退黨浪潮'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1302969600
    assert parsed_news.reporter == '張建浩'
    assert parsed_news.title == '吉隆坡鬧市中慶祝9300萬人退出中共'
    assert parsed_news.url_pattern == '2011-04-17-519983'
