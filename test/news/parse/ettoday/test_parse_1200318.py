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
    url = r'https://star.ettoday.net/news/1200318'
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
            蔓越莓與其他植物或水果與眾不同的地方之一,在於它含有豐富的A型原花青素,蘋果、葡萄
            等水果含的是B型原花青素居多。實驗證明,A型原花青素相較於B型原花青素更可以抑制細
            菌附著在泌尿道的上皮細胞,對女性的泌尿道保健效果更佳。 除此之外,蔓越莓也富含其他
            酚類活性物質,例如:類黃酮、花青素、苯甲酸、熊果酸,這些化合物會帶來酸澀味,因此蔓
            越莓產品通常會加糖調味,所以購買市售蔓越莓產品要特別注意避免攝取過多糖份,或查看
            營養標示選購糖量較低的產品。 蔓越莓在加工過程中,成分容易受到破壞,像是加工過程中
            會移除富含植化素的果皮還有種子。蔓越莓的營養成份也會在加工過程中流失,所以在各種
            不同的蔓越莓產品中,多酚的含量都不盡相同。 尤其以花青素最容易受到加工過程的影響,
            流失將達到50%以上,且在製造成粉末的過程中會使用巴氏殺菌法,類黃酮和原花青素可能會
            因此流失30-40%。 蔓越莓的保健功效很多,主要有下列幾項: 延緩動脈硬化: 經實驗證明
            ,每天喝54%蔓越莓汁480毫升。可以提供約835毫克多酚,持續四週後,可以顯著降低動脈硬
            化程度。 影響血小板的功能: 蔓越莓內的delphinidin-3-glucoside和花青素可以抑制血
            栓的形成。 改善血脂異常: 動物及人體試驗都指出,飲用蔓越莓汁含有的原花青素可降低
            LDL膽固醇和增加HDL膽固醇。 降低發炎反應: 動脈粥狀硬化是一種發炎性疾病,蔓越莓在
            體外試驗發現可以抑制巨噬細胞和T-cell的活化反應,除此之外,也可透過這個機制改善牙
            周病的問題。 保護內皮細胞: 心血管疾病的發生和內皮細胞的完整有關係,蔓越莓汁萃取
            物的活性成分可以維持並保護內皮細胞的完整。 此外,蔓越莓乾除了直接吃,還有許多創意
            吃法: 蔓越莓優格 材料: 蔓越莓乾15克、蔓越莓汁50毫升、玉米片15克、堅果10克、無
            糖優格200毫升 做法: 1. 將蔓越莓汁與優格混勻 2. 所有材料加入,即可享用 堅果每日建
            議食用1份(10g),此份點心即符合一日建議量。 蔓越莓餅乾 材料: 奶油80克、糖50克、
            低筋麵粉150克、蔓越莓乾75克、雞蛋1顆 做法: 1. 奶油切丁並與糖粉攪拌 2. 加入麵粉
            和雞蛋拌勻後,揉成團狀 3. 用保鮮膜包起來,放入冷凍庫4小時 4. 取出來後,切成片狀置
            於平鋪有烘焙紙的烤盤上 5. 烤箱以170度烘烤20分鐘,即完成。
            '''
        ),
    )
    assert parsed_news.category == '直銷'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530147600
    assert parsed_news.reporter == '陳建竹'
    assert parsed_news.title == '蔓越莓含A型原花青素 女性保健效果佳'
    assert parsed_news.url_pattern == '1200318'
