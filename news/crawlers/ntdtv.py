import json
from datetime import datetime, timedelta
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from typing import List
from news.db.schema import News
import news.preprocess
from collections import Counter
import news.crawlers

FIRST_PAGE = 2
URL_PATTERN = re.compile(
    r'https://www.epochtimes.com/b5/(\d+)/(\d+)/(\d+)/n\d+\.htm'
)


def get_news_list(
    category: str,
    current_datetime: datetime,
    api: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
) -> List[News]:
    news_list: List[News] = []
    logger = Counter()

    # Get max page of this category.
    try:
        url = f'https://www.epochtimes.com/b5/{api}_2.htm'
        response = requests.get(
            url,
            timeout=news.crawlers.util.REQUEST_TIMEOUT,
        )
        response.close()

        # Raise exception if status code is not 200.
        news.crawlers.util.check_status_code(response=response)

        soup = BeautifulSoup(response.text, 'html.parser')
        max_page = soup.select('div.pagination > a.page-numbers')[-2].text
        max_page = int(max_page.replace(',', ''))
    except Exception as err:
        if err.args:
            logger.update([err.args[0]])

        # Only show error stats in debug mode.
        if debug:
            for k, v in logger.items():
                print(f'{k}: {v}')
        return []

    # Only show progress bar in debug mode.
    iter_range = range(FIRST_PAGE, max_page)
    if debug:
        iter_range = tqdm(iter_range, desc='Find start page loop')

    # Find start page loop.
    start_page = 2
    for page in iter_range:
        page_url = f'https://www.epochtimes.com/b5/{api}_{page}.htm'

        try:
            response = requests.get(
                page_url,
                timeout=news.crawlers.util.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.check_status_code(response=response)

            # Parse date in this page.
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.select(
                'div.post_list.left_col > div.one_post div.text > div.title > a'
            )
            matches = filter(
                bool,
                map(lambda a_tag: URL_PATTERN.match(a_tag['href']), a_tags)
            )
            news_datetimes = map(
                lambda match: {
                    'year': int(match.group(1)),
                    'month': int(match.group(2)),
                    'day': int(match.group(3)),
                },
                matches,
            )
            news_datetimes = list(map(
                lambda n: dateutil.parser.isoparse(
                    f"20{n['year']:02d}-{n['month']:02d}-{n['day']:02d}T00:00:00Z"
                ),
                news_datetimes,
            ))
            # If this page contains valid news, we start crawling from this page.
            news_datetimes = filter(bool, map(
                lambda n: past_datetime <= n <= current_datetime,
                news_datetimes,
            ))

            if news_datetimes:
                start_page = page
                break
        except Exception as err:
            if err.args:
                logger.update([err.args[0]])

    # Only show progress bar in debug mode.
    iter_range = range(start_page, max_page)
    if debug:
        iter_range = tqdm(iter_range, desc='Crawling loop.')

    # Crawling loop.
    is_datetime_valid = True
    for page in iter_range:
        if not is_datetime_valid:
            break

        page_url = f'https://www.epochtimes.com/b5/{api}_{page}.htm'

        try:
            response = requests.get(
                page_url,
                timeout=news.crawlers.util.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.check_status_code(response=response)

            # If `status_code == 200`, parse links in this page.
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.select(
                'div.post_list.left_col > div.one_post div.text > div.title > a'
            )
        except Exception as err:
            if err.args:
                logger.update([err.args[0]])
            continue

        for a_tag in a_tags:
            try:
                news_url = a_tag['href']

                response = requests.get(
                    news_url,
                    timeout=news.crawlers.util.REQUEST_TIMEOUT,
                )
                response.close()

                # Raise exception if status code is not 200.
                news.crawlers.util.check_status_code(response=response)

                # Parse news in this page.
                parsed_news = news.preprocess.epochtimes.parse(ori_news=News(
                    raw_xml=response.text,
                    url=news_url,
                ))

                news_datetime = dateutil.parser.isoparse(parsed_news.datetime)
                if past_datetime > news_datetime or news_datetime > current_datetime:
                    is_datetime_valid = False
                    break

                news_list.append(parsed_news)
            except Exception as err:
                if err.args:
                    logger.update([err.args[0]])

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


CATEGORIES = {
    '國際': 202,
    '港澳': 205,
    '財經': 208,
    '健康': 1255,
    '體育': 211,
    '美國': 203,
    '大陸': 204
}


def main(
    current_datetime: datetime,
    db_name: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
):

    if past_datetime > current_datetime:
        raise ValueError('Must have `past_datetime <= current_datetime`.')

    # Get database connection.
    conn = news.db.util.get_conn(db_name=db_name)
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)

    for category, api in CATEGORIES.items():
        news.db.write.write_new_records(
            cur=cur,
            news_list=get_news_list(
                category=category,
                current_datetime=current_datetime,
                debug=debug,
                api=api,
                past_datetime=past_datetime,
            ),
        )

        conn.commit()

    # Close database connection.
    conn.close()


# def get_links(board, start_page, end_page):
#     result = []
#     for i in range(start_page, end_page):
#         url = f'https://www.ntdtv.com/b5/prog{board[1]}/{i}'
#         try:
#             response = requests.get(url)
#             soup = BeautifulSoup(response.text, 'html.parser')
#         except:
#             break
#         try:
#             all_post = soup.find('div', class_='post_list').find_all('div', class_='one_post')
#         except:
#             continue
#         for post in all_post:
#             try:
#                 title_a = post.find('div', class_='title').find('a')
#             except:
#                 continue
#             data_dic = {
#                 'url': title_a['href'],
#                 'time': None,
#                 'company': '新唐人',
#                 'label': board[0],
#                 'reporter': None,
#                 'title': title_a.text,
#                 'article': None,
#                 'raw_xml': None
#             }
#             # print(data_dic)
#             result.append(data_dic)
#     return result

# def get_data(link, time_bound):
#     result = []
#     for link in tqdm(links):
#         url = link['url']
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         try:
#             time = soup.find('div', class_='article_info').find('div', class_='time').find('span').text
#         except:
#             time = None
#         date = time.split(' ')[0].split('-')
#         date = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
#         if date < time_bound:
#             break
#         try:
#             article = ''.join([i.text for i in soup.find('div', class_='article_content').find('div', class_='post_content').find_all('p')])
#         except:
#             continue
#         data_dic = {
#             'url': url,
#             'time': time,
#             'company': '新唐人',
#             'label': link['label'],
#             'reporter': None,
#             'title': link['title'],
#             'article': article,
#             'raw_xml': response.text
#         }
#         result.append(data_dic)
#     return result

# if __name__ == "__main__":
#     board = [
#         ['國際', 202],
#         ['港澳', 205],
#         ['財經', 208],
#         ['健康', 1255],
#         ['體育', 211],
#         ['美國', 203],
#         ['大陸', 204]
#     ]
#     for b in tqdm(board):
#         for page in tqdm(range(1, 501, 50)):
#             time_bound = datetime.now() - timedelta(days=1)
#             links = get_links(b, page, page+50)
#             data = get_data(links, time_bound)
#             json.dump(data, open(f'crawlers/data/ntdtv/{b[0]}_p{page}-p{page+50}_{time_bound.strftime("%Y%m%d")}.json', 'w', encoding='utf8'))
