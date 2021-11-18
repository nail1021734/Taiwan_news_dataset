# Crawler Scripts

所有爬蟲都以 `news/crawlers/main.py` 為主要呼叫窗口.
支援的新聞網站與爬蟲細節請參考以下檔案:

- 中時: `news/crawlers/chinatimes.py`.
- 中央社: `news/crawlers/cna.py`.
- 大紀元: `news/crawlers/epochtimes.py`.
- 東森: `news/crawlers/ettoday.py`.
- 民視: `news/crawlers/ftv.py`.
- 自由: `news/crawlers/ltn.py`.
- 新唐人: `news/crawlers/ntdtv.py`.
- 三立: `news/crawlers/setn.py`.
- 風傳媒: `news/crawlers/storm.py`.
- TVBS: `news/crawlers/tvbs.py`.
- 聯合報: `news/crawlers/udn.py`.

## 中時 Chinatimes

- 在同一 IP 使用**超過** `2` 個 process 同時進行爬蟲會觸發 `429`.
- 即使使用 `<= 2` 個 process 有時仍然會被 `429`.
- 單次 `429` 約可在 `2 ~ 5` 分鐘恢復.
- 所有的新聞都是**流水號**, 分配到不同的**類別**之下.
- 每天新聞數的最大上限為 `100000`, 真實產出的新聞數為 `5000+`.
- **最早**可以爬到的新聞日期為 `2010-01-01`.
- 觀察到中國時報有兩種網址一種為在 `newspapers` 之下另一種在 `realtimenews` 之下.

```sh
python -m news.crawlers.main --crawler_name chinatimes --db_name chinatimes.db --debug --past_datetime 2010-01-01+0000
```

## 中央社 CNA

- 似乎沒有做爬蟲的防禦.
- 所有的新聞都是**流水號**, 分配到不同的**類別**之下.
  - 但是類別轉換有漏洞, 意即所有流水號都能對到任意類別.
- 每天新聞數的最大上限為 `10000`.
- **最早**可以爬到的新聞日期為 `2014-03-06`.

```sh
python -m news.crawlers.main --crawler_name cna --db_name cna.db --debug --past_datetime 2014-01-01+0000
```

## 大紀元 Epochtimes

- 似乎沒有做爬蟲的防禦
- 所有的新聞都是**流水號**, 分配到不同的**類別**之下
- **最早**可以爬到的新聞日期為 `2001-01-01`.

```sh
python -m news.crawlers.main --crawler_name epochtimes --db_name epochtimes.db --debug --past_datetime 2001-01-01+0000
```

## 東森 ETtoday

- 主站有做爬蟲防禦, 但 `star.ettoday.net` 似乎沒有做爬蟲的防禦, 可以作為跳轉頁面.
- 所有的新聞都是**流水號**, 分配到不同的**類別 + 網域**之下.
- **最早**可以爬到的新聞流水號為 `1`.

```sh
python -m news.crawlers.main --crawler_name ettoday --db_name ettoday.db --debug --first_idx 1
```

## 民視 FTV

- 有做爬蟲防禦, 但一律使用 `200` 作為回覆, 因此不會有 bad request.
- 所有的新聞都是**流水號**, 分配到不同的**類別**之下.
- 每天新聞數的最大上限為 `10000`.
- **最早**可以爬到的新聞日期為 `2017-09-17`.

```sh
python -m news.crawlers.main --crawler_name ftv --db_name ftv.db --debug --past_datetime 2017-09-17+0000
```

## 自由 LTN

- 有做爬蟲防禦, 所以只能使用 API.
- 未來必須改用 selenium 繞過 cloudflare.
- 所有的新聞都是**流水號**, 分配到不同的**類別**之下.

```sh
python -m news.crawlers.main --crawler_name ltn --db_name ftv.db --debug
```

## 新唐人 NTDTV

- 似乎沒有做爬蟲的防禦
- 所有的新聞都是**流水號**, 分配到不同的**類別**之下
- **最早**可以爬到的新聞日期為 `2002-01-01`.

```sh
python -m news.crawlers.main --crawler_name ntdtv --db_name ntdtv.db --debug --past_datetime 2002-01-01+0000
```

## 三立 SETN

- 有做爬蟲防禦, 所以只能使用 API.
- 未來必須改用 selenium 繞過 cloudflare.
- 所有的新聞都是**流水號**, 分配到不同的**類別**之下.

```sh
python -m news.crawlers.main --crawler_name setn --db_name setn.db --debug --first_idx 1
```

## 風傳媒 STORM

- 有做爬蟲防禦, 但一律使用 `200` 作為回覆, 因此不會有 bad request.
- **最早**可以爬到的新聞流水號為 `21016`.
- 對於多頁數的新聞, 使用全文閱讀模式 `mode=whole` 獲取完整文章.

```sh
# The first available index of storm is 21016.
python -m news.crawlers.main --crawler_name storm --db_name storm.db --debug --first_idx 21016
```

## TVBS

- 有做爬蟲防禦, 所以只能使用 API.
- 在同一 IP 使用**超過** `3` 個 process 同時進行爬蟲會觸發 `403`.
- 單次 `403` 約可在 `2 ~ 5` 分鐘恢復.
- 未來必須改用 selenium 繞過 cloudflare.
- 所有的新聞都是**流水號**, 分配到不同的**類別**之下.

```sh
python -m news.crawlers.main --crawler_name tvbs --db_name tvbs.db --debug --first_idx 1 --latest_idx 1611612
```

## 聯合報 UDN

- 有做爬蟲防禦, 所以只能使用 API.
- 未來必須改用 selenium 繞過 cloudflare.
- 所有的新聞都是**流水號**, 分配到不同的**類別**之下.

```sh
python -m news.crawlers.main --crawler_name udn --db_name udn.db --debug --past_datetime 2014-01-01+0000
```
