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
    url = r'https://star.ettoday.net/news/1200547'
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
            蔡英文總統前幾天接受「法新社」的專訪,兩個訪談的重點是: 1、呼籲世界各國,一起制約
            中國。 2、願意在總統任內,跟習近平見面。 這樣的說法,如同公開批評某家餐廳難吃又貴
            還不乾淨,呼籲大家一起抵制,不要去吃。講完之後,拿起電話,打過去:「喂!請問晚上還有
            位子嗎?我這邊兩大三小,想去用餐」一樣。完完全全,是一種精神錯亂的邏輯。 別的先不
            說,光是你已經公開呼籲全世界各國都去「制約」他,對方還會願意跟你見面嗎? 傻不是罪,
            但一個領導國家的總統如果傻,那就將是台灣的災難。 2015年11月7日,兩岸分治之後首次
            的「領導人見面」,在新加坡上演。當時身為民進黨主席兼總統參選人的蔡英文,對「馬習
            會」提出了五點批評: 1、黑箱,會談過程並未公開透明。 2、未提「中華民國」。 3、傷
            害台灣民主與國家尊嚴。 4、限縮台灣人民的選擇權。 5、沒捍衛台灣人的價值跟權利,令
            人失望。 他日檢討人,今日被檢討,所以請問蔡總統: 1、您現在主動提出要見習近平,是已
            經取得「台灣人民的同意了嗎」? 2、對方已經接受見面時您可以自稱「中華民國總統」了
            嗎? 3、台灣民眾已經告訴您台灣民眾要「如何選擇」了嗎? 如果沒有,萬一沒有,那蔡總統
            「憑什麼」想跟習近平見面?蔡總統「憑什麼」要限縮台灣人民的選擇權?您拿689萬票,馬
            英九也拿689萬票,他見習,不可以;您見習,就好棒棒?這是什麼道理? 呼籲制約中國大陸,是
            種選擇。 蔡政府當然可以選擇要跟大陸對抗,沒問題,畢竟「親美日、抗中國」早就不是新
            聞,眼見未來十年,將是「美中兩強」的競爭局面,台灣選擇加入「美方陣營」,加入「制約
            中國大陸越來越強大」的那個陣營,這是選擇,好壞自己承擔。 但既然已經選擇要「對抗」
            ?朝人揮拳之後,又說可以談一談?要談什麼?人家願意跟你談嗎? 再說一次:「傻不是罪,但
            一個領導國家的總統如果傻,那就將是台灣的災難」。
            '''
        ),
    )
    assert parsed_news.category == '雲論'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530090780
    assert parsed_news.reporter is None
    assert parsed_news.title == '蔡習會?小英總統,您累了嗎?'
    assert parsed_news.url_pattern == '1200547'
