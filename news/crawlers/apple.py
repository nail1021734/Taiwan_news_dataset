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
):
    news_list: List[News] = []
    api_response = requests.get(api_url)
    logger = Counter()

    if api_response.status_code != 200:
        # Got banned.
        logger.update(['Got banned.'])
        news.crawlers.util.after_banned_sleep()

        # Only show error stats in debug mode.
        if debug:
            for k, v in logger.items():
                print(f'{k}: {v}')
        return []

    # Only show progress bar in debug mode.
    links = api_response.json()['content_elements']
    if debug:
        links = tqdm(links)

    # Each news were stored as `content_elements`.
    for link in links:
        news_url = 'https://tw.appledaily.com' + link['canonical_url']

        # Only consider news which display time is bounded by constraint.
        news_datetime_str = link['display_date']
        news_datetime = dateutil.parser.isoparse(news_datetime_str)
        if past_datetime > news_datetime or news_datetime > current_datetime:
            logger.update(['Time constraint violated.'])
            continue

        response = requests.get(news_url)

        if response.status_code != 200:
            logger.update(['Got banned.'])
            # Got banned.
            news.crawlers.util.after_banned_sleep()
            continue

        try:
            parsed_news = news.preprocess.apple.parse(ori_news=News(
                datetime=news_datetime_str,
                raw_xml=response.text,
                url=news_url,
            ))
        except Exception as err:
            # Skip parsing if error.
            if err.args:
                logger.update([err.args[0]])
            continue

        news_list.append(parsed_news)

        # Sleep to avoid banned.
        news.crawlers.util.before_banned_sleep()

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


def main(
    current_datetime: datetime,
    db_name: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
):
    categories = {
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

    # Get database connection.
    conn = news.db.util.get_conn(db_name=db_name)
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)

    for category, api_url in categories.items():
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

        # Sleep to avoid banned.
        news.crawlers.util.before_banned_sleep()

    # Close database connection.
    conn.close()
