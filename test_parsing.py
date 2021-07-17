import news.db
import news.preprocess
from bs4 import BeautifulSoup
from tqdm import tqdm

if __name__ == '__main__':
    dset = news.db.read.AllRecords(db_name='ftv.db')

    res = []
    for i, n in enumerate(tqdm(dset)):
        try:
            # if '120940/5544528' in n.url:
            if n.company == '民視':
                # if any(map(lambda url: url in n.url, ['2021702W0010', '2021702W0111'])):
                res.append(news.preprocess.ftv.parse(n))
        except Exception as err:
            print(err.args)

    conn = news.db.util.get_conn(db_name='test2.db')
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)
    news.db.write.write_new_records(cur=cur, news_list=res)
    conn.close()

    n_article = [r for r in res if not r.article]
    n_category = [r for r in res if not r.category]
    n_company = [r for r in res if not r.company]
    n_datetime = [r for r in res if not r.datetime]
    n_raw_xml = [r for r in res if not r.raw_xml]
    n_reporter = [r for r in res if not r.reporter]
    n_title = [r for r in res if not r.title]
    n_url = [r for r in res if not r.url]

    s = f"""empty count
    article: {len(n_article)}
    category: {len(n_category)}
    company: {len(n_company)}
    datetime: {len(n_datetime)}
    raw_xml: {len(n_raw_xml)}
    reporter: {len(n_reporter)}
    title: {len(n_title)}
    url: {len(n_url)}
    """
    print(s)

    def list_reporter(res):
        return(set([r.reporter for r in res]))
