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
    url = r'https://www.ntdtv.com/b5/2014/01/01/a1034743.html'
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
            煙花在新西蘭、澳大利亞和香港的夜空綻放,揭開了全球歡慶2014年新年的
            序幕。 在整個亞太地區,主要城市的廣場上聚滿人群,他們歡天喜地,燃放禮花,迎接
            新年的到來。 在新西蘭,歡慶的人群在大街上載歌載舞之際,奧克蘭的天空塔開始放
            煙花。在澳大利亞悉尼,100多萬人觀看10多年來首次從著名的悉尼歌劇院帆形建筑上施放
            的煙花。在香港摩天大樓的上空,隨著隆隆的爆炸聲綻放出朵朵盛開的禮花。 莫斯科、倫敦
            和紐約等大都市都舉行辭舊迎新的盛大慶典。預計紐約時報廣場上將有100萬人翹首以待,
            期盼巨大玻璃球隨著午夜鐘聲落下的那一刻。迪拜正努力打造世界上最大型的施放煙花
            活動。 在日本,人們在新年到來之際吃麵條和海鮮,認為這會在2014年帶來好運。他們還
            絡繹不絕地前往寺廟和神社祈福。 菲律賓今年的新年慶祝活動相對安靜。當局說,新年前
            有大約260人因煙花或流彈而受傷。菲律賓11月遭受臺風海燕襲擊,有數千人死亡,目前災區
            還在恢復當中,人們心情憂鬱。 南非開普敦今年的慶祝活動將有令人感傷的時刻,他們將向
            12月5日去世的反對種族隔離運動的領袖曼德拉表示敬意。
            '''
        ),
    )
    assert parsed_news.category == '國際,社會'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1388505600
    assert parsed_news.reporter is None
    assert parsed_news.title == '世界各地喜迎2014年'
    assert parsed_news.url_pattern == '2014-01-01-1034743'
