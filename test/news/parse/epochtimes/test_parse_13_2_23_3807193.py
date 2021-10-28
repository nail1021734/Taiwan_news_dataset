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
    url = r'https://www.epochtimes.com/b5/13/2/23/n3807193.htm'
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
            研究:高糖食品、乳製品易引發青春痘 面對青春痘困擾的朋友可要注意了,根
            據最新的研究顯示,吃過多高血糖指數飲食和乳製品,容易生長青春痘,同時發現,醫學營養
            治療(MNT)在治療青春痘方面扮演著重要角色。 據《紐約每日新聞》報導,這項研究報告發
            表於《營養飲食學會期刊》((Journal of the Academy of Nutrition and Diete
            tics)。 早在19世紀,專家就認為青春痘與巧克力、脂肪和糖等食品有關,但是1960年開始,
            科學家卻否定了這種說法。 「這主要因為兩項重要的研究成果被重複引用來反駁飲食和
            青春痘之間的聯繫。」紐約大學營養、食品研究與公共健康系的專家珍妮花‧芭莉絲
            (Jennifer Burris)說。「最近,皮膚科專家和註冊營養師重新檢討飲食和青春痘之間的
            關係,並對醫學營養治療與醫治青春痘的關係越來越感興趣。」 芭莉絲和她的同僚進行了
            一項文獻綜述,評估在三個時期內飲食和青春痘之間的關聯。在排除掉1960年至2012年的
            研究結果之後,研究團隊得出結論,攝取高血糖指數食品和青春痘之間有明顯關聯。他們還發現,
            雖然過去10年的研究成果沒有證明飲食習慣會引發青春痘,但兩者之間確實存在聯繫。 研究
            也指出,除了高血糖指數的食品,牛奶等乳製品也會導致胰島素產生,並含有許多可引發青春痘
            的荷爾蒙。芭莉絲說:「問題是,我們目前還沒有太多的證據證明這一點。目前只有3至4項針對
            這方面的研究,它們全都證明了乳製品和青春痘之間的關聯。」 雖然研究尚未成熟,若大家
            真有面對青春痘的困擾,不妨還是考慮調整飲食習慣,並諮詢皮膚科醫生和營養師的意見。此外,
            保持良好的生活習慣和規律的生活作息,注意肌膚清潔、調整生活壓力等等,也可以減少青春痘
            爆發。
            '''
        ),
    )
    assert parsed_news.category == '視頻集錦'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1361548800
    assert parsed_news.reporter == '李茹嵐'
    assert parsed_news.title == '勵志女孩用自己的故事鼓勵大家 勇敢面對這個'
    assert parsed_news.url_pattern == '13-2-23-3807193'
