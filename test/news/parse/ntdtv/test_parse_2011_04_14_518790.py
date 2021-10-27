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
    url = r'https://www.ntdtv.com/b5/2011/04/14/a518790.html'
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
            突尼斯前总统面临多项控罪 据突尼斯媒体星期四(14日)报道,突尼斯当局准备对前总统
            扎因•阿比丁•本•阿里提出18项指控,其中包括故意杀人、阴谋危害国家、非法侵吞财产、
            走私和滥用毒品等。 突尼斯司法部长拉扎尔•卡鲁伊•谢比表示,将对本•阿里及其家人和
            核心集团提起大约44项指控并于近期开始审理这些案件。 突尼斯政府目前正在寻求引渡
            本•阿里回国接受审判的法律途径。本•阿里1月14日离开突尼斯后,流亡沙特阿拉伯。 突尼斯
            已经寻求国际刑警组织的帮助,通缉并逮捕本•阿里及其家庭成员。 突尼斯“茉莉花革命”
            起因于去年12月17日,一名26岁的研究生因无证照销售水果和蔬菜,遭到警察的“耳光”、
            “吐沫”和没收,市政当局又拒绝其对警察打人的投诉,他投诉无门下自焚,引发民众示威抗议;
            当局开枪镇压抗议民众,引发更大的示威潮,终至其独裁总统垮台。
            '''
        ),
    )
    assert parsed_news.category == '國際專題,敘利亞局勢'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1302710400
    assert parsed_news.reporter is None
    assert parsed_news.title == '突尼斯前总统本•阿里面临18项指控'
    assert parsed_news.url_pattern == '2011-04-14-518790'
