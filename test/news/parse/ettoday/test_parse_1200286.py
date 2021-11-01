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
    url = r'https://star.ettoday.net/news/1200286'
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
            現在房價寸土寸金,不少人都是住在「螞蟻窩」中,但是其實只要掌握了視覺延伸
            的概念,就算在同樣大的地方也會有看起來非常開闊的錯覺,來看看是哪幾樣小物起到了神
            奇的效果! 1.明亮色系物件 如果墻面是白色,那麼可以考慮使用白色的物件來延伸空間感,
            視覺上會有放大空間的錯覺,同時也會讓人覺得乾淨整潔。 2.圓形茶几 圓形茶几是必備的
            小空間家具,因為形狀的優勢,所以不管放在哪邊都能完美融合,並且圓滑的形狀讓人感到十
            分舒服。 3.透明物品 同樣能夠放大空間的物品就是透明物件了,就算找不到透明花瓶也可
            以把牛奶瓶回收再利用,插上綠色植物,馬上就有大空間的錯覺,誰說小房間沒辦法養花,小
            植物更可愛! 4.幾何收納籃 現在非常流行這樣的幾何收納籃,不管是用來當做洗衣籃或是
            一般擺設,都很美觀實用,其實它也能夠創造出放大空間的錯覺,試想一下如果不是中空的設
            計,而是實木的設計,那空間感會立馬變小並且沉重很多。但這樣的幾何設計還能在上面放
            置物品,真的是一物多用。 5.向上收納 比起把物品放在平面,可以嘗試把物品向上收納,不
            僅一目了然,也能產生空間放大的錯覺,放在上面也能起到裝飾作用。 6.照片墻設計 還停
            留在把照片放桌上就真的落伍了,其實照片墻不光是節省空間,產生美感。也能夠在同樣的
            一面墻上產生放大的錯覺,只要挑選尺寸中偏小的照片,就能夠放下許多照片,讓人覺得墻面
            似乎很大,這一招必學啦。
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530176460
    assert parsed_news.reporter == 'Ann'
    assert parsed_news.title == '小房間專屬!6個視覺詐欺術讓「螞蟻窩」瞬間放大'
    assert parsed_news.url_pattern == '1200286'
