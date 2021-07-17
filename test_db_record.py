import news.db
from bs4 import BeautifulSoup
from tqdm import tqdm

if __name__ == '__main__':
    dset = news.db.read.AllRecords(db_name='test.db')

    res = []
    for n in tqdm(dset):
        if n.company == '新唐人':
            res.append(n)

    print(f'number of news: {len(res)}')
    n_article = [r for r in res if not r.article]
    n_category = [r for r in res if not r.category]
    n_company = [r for r in res if not r.company]
    n_datetime = [r for r in res if not r.datetime]
    n_raw_xml = [r for r in res if not r.raw_xml]
    n_reporter = [r for r in res if not r.reporter]
    n_title = [r for r in res if not r.title]
    n_url = [r for r in res if not r.url]

    s = f"""empty count
    article:  {len(n_article)}
    category: {len(n_category)}
    company:  {len(n_company)}
    datetime: {len(n_datetime)}
    raw_xml:  {len(n_raw_xml)}
    reporter: {len(n_reporter)}
    title:    {len(n_title)}
    url:      {len(n_url)}
    """
    print(s)
