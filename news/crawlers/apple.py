from collections import Counter
from datetime import datetime
from typing import List

import dateutil.parser
import requests
from tqdm import tqdm

import news.crawlers
import news.db
import news.preprocess
from news.db.schema import News


def get_news_list(
    category: str,
    current_datetime: datetime,
    api_url: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
) -> List[News]:
    news_list: List[News] = []
    logger = Counter()

    try:
        api_response = requests.get(
            api_url,
            timeout=news.crawlers.util.REQUEST_TIMEOUT,
        )
        api_response.close()

        # Raise exception if status code is not 200.
        news.crawlers.util.check_status_code(response=api_response)

        links = api_response.json()['content_elements']
    except Exception as err:
        if err.args:
            logger.update([err.args[0]])

        # Only show error stats in debug mode.
        if debug:
            for k, v in logger.items():
                print(f'{k}: {v}')

        return []

    # Only show progress bar in debug mode.
    if debug:
        links = tqdm(links)

    # Each news were stored as `content_elements`.
    for link in links:
        try:
            news_url = 'https://tw.appledaily.com' + link['canonical_url']

            # Only consider news which display time is bounded by constraint.
            news_datetime_str = link['display_date']
            news_datetime = dateutil.parser.isoparse(news_datetime_str)
            if past_datetime > news_datetime or news_datetime > current_datetime:
                raise Exception('Time constraint violated.')

            response = requests.get(
                news_url,
                timeout=news.crawlers.util.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.check_status_code(response=api_response)

            parsed_news = news.preprocess.apple.parse(ori_news=News(
                datetime=news_datetime_str,
                raw_xml=response.text,
                url=news_url,
            ))

            news_list.append(parsed_news)
        except Exception as err:
            # Skip parsing if error.
            if err.args:
                logger.update([err.args[0]])

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


CATEGORIES = {
    '娛樂': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query={%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A\%22%2Frealtime%2Fentertainment\%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A[now-48h%2Fh%2BTO%2Bnow]%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22}&d=230&_website=tw-appledaily',
    '社會': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Flocal%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-48h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=230&_website=tw-appledaily',
    '生活': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Flife%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-48h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=230&_website=tw-appledaily',
    '財經地產': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fproperty%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-48h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=230&_website=tw-appledaily',
    '國際': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fproperty%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-48h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=230&_website=tw-appledaily',
    '政治': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fpolitics%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-48h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=230&_website=tw-appledaily',
    '3C車市': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fgadget%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-48h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=230&_website=tw-appledaily',
    '吃喝玩樂': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fsupplement%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-48h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=230&_website=tw-appledaily',
    '體育': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fsports%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-48h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=230&_website=tw-appledaily',
    '蘋評理': r'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22(taxonomy.primary_section._id%3A%5C%22%2Frealtime%2Fforum%5C%22)%2BAND%2Btype%3Astory%2BAND%2Bdisplay_date%3A%5Bnow-48h%2Fh%2BTO%2Bnow%5D%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_no_show_for_web%2BAND%2BNOT%2Btaxonomy.tags.text.raw%3A_nohkad%22%2C%22feedSize%22%3A100%2C%22sort%22%3A%22display_date%3Adesc%22%7D&d=230&_website=tw-appledaily',
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

    for category, api_url in CATEGORIES.items():
        news.db.write.write_new_records(
            cur=cur,
            news_list=get_news_list(
                category=category,
                current_datetime=current_datetime,
                debug=debug,
                api_url=api_url,
                past_datetime=past_datetime,
            ),
        )

        conn.commit()

    # Close database connection.
    conn.close()
