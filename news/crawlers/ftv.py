# from collections import Counter
# from datetime import datetime, timedelta
# from typing import List

# import dateutil.parser
# import requests
# from tqdm import tqdm

# import news.crawlers
# import news.db
# from news.db.schema import News

# # <li> <a href='https://www.ftvnews.com.tw/realtime/'>即時</a> </li>
# # <li> <a href='https://www.ftvnews.com.tw/popular/'>熱門</a> </li>
# # <li> <a href='/tag/快新聞'>快新聞</a> </li>
# # <li> <a href='/tag/政治'>政治</a> </li>
# # <li> <a href='/tag/娛樂'>娛樂</a> </li>
# # <li> <a href='/tag/財經'>財經</a> </li>
# # <li> <a href='/tag/生活'>生活</a> </li>
# # <li> <a href='/tag/國際'>國際</a> </li>
# # <li> <a href='/tag/社會'>社會</a> </li>
# # <li> <a href='/tag/體育'>體育</a> </li>
# # <li> <a href='/tag/健康'>健康</a> </li>
# # <li> <a href='/tag/美食'>美食</a> </li>
# # <li> <a href='/tag/氣象'>氣象</a> </li>
# # <li> <a href='/tag/武漢肺炎'>疫情擴散</a> </li>
# # <li> <a href='/tag/熱門網搜'>熱門網搜</a> </li>
# # <li> <a href='/tag/下雨'>世紀乾旱</a> </li>
# # <li> <a href='https://englishnews.ftv.com.tw/'>英語新聞</a> </li>
# # <li> <a href='/tag/疫苗'>疫苗</a> </li>
# # <li> <a href='/tag/運勢'>運勢</a> </li>
# # <li> <a href='/tag/PLEAGUE'>P.LEAGUE+</a> </li>
# # <li> <a href='/tag/台灣演義'>台灣演義</a> </li>
# # <li> <a href='/tag/新聞觀測站'>新聞觀測站</a> </li>
# # <li> <a href='/tag/民視異言堂'>異言堂</a> </li>
# # <li> <a href='/tag/工商好消息'>工商好消息</a> </li>

# CATEGORIES = {

# }


# def get_news_list(
#     current_datetime: datetime,
#     past_datetime: datetime,
#     *,
#     debug: bool = False,
# ) -> List[News]:
#     news_list: List[News] = []
#     logger = Counter()

#     for channelId in [1, 2]:
#         # Only show progress bar in debug mode.
#         iter_range = range(MAX_PAGE)
#         if debug:
#             iter_range = tqdm(iter_range)

#         time_constraint_violated = False
#         for page in iter_range:
#             if time_constraint_violated:
#                 break

#             url = f'https://udn.com/api/more?page={page}&channelId={channelId}&type=cate_latest_news&totalRecNo=100'
#             try:
#                 response = requests.get(
#                     url,
#                     timeout=news.crawlers.util.REQUEST_TIMEOUT,
#                 )
#                 response.close()

#                 # Raise exception if status code is not 200.
#                 news.crawlers.util.check_status_code(
#                     company='udn',
#                     response=response
#                 )
#             except Exception as err:
#                 if err.args:
#                     logger.update([err.args[0]])
#                 break

#             data_lists = response.json()
#             if 'lists' not in data_lists or not data_lists['lists']:
#                 break

#             for data_obj in data_lists['lists']:
#                 try:
#                     news_datetime = datetime.strptime(
#                         data_obj['time']['date'],
#                         '%Y-%m-%d %H:%M'
#                     ) - timedelta(hours=8)
#                     news_datetime = dateutil.parser.isoparse(
#                         news_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
#                     )
#                     if not (past_datetime <= news_datetime <= current_datetime):
#                         raise Exception('Time constraint violated.')

#                     url = data_obj["titleLink"].split("?")[0]
#                     url = f'https://udn.com{url}'

#                     response = requests.get(
#                         url,
#                         timeout=news.crawlers.util.REQUEST_TIMEOUT,
#                     )
#                     response.close()

#                     # Raise exception if status code is not 200.
#                     news.crawlers.util.check_status_code(
#                         company='udn',
#                         response=response
#                     )
#                     parsed_news = news.preprocess.udn.parse(ori_news=News(
#                         raw_xml=response.text,
#                         url=url,
#                     ))
#                     news_list.append(parsed_news)
#                 except Exception as err:
#                     if err.args:
#                         logger.update([err.args[0]])

#                         if err.args[0] == 'Time constraint violated.':
#                             time_constraint_violated = True
#                             break

#     # Only show error stats in debug mode.
#     if debug:
#         for k, v in logger.items():
#             print(f'{k}: {v}')

#     return news_list


# def main(
#     current_datetime: datetime,
#     db_name: str,
#     past_datetime: datetime,
#     *,
#     debug: bool = False,
# ):
#     if past_datetime > current_datetime:
#         raise ValueError('Must have `past_datetime <= current_datetime`.')

#     # Get database connection.
#     conn = news.db.util.get_conn(db_name=db_name)
#     cur = conn.cursor()
#     news.db.create.create_table(cur=cur)

#     news.db.write.write_new_records(
#         cur=cur,
#         news_list=get_news_list(
#             current_datetime=current_datetime,
#             debug=debug,
#             past_datetime=past_datetime,
#         ),
#     )

#     conn.commit()

#     # Close database connection.
#     conn.close()
