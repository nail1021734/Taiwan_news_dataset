# Parse Scripts

爬蟲完後所有新聞 HTML 都儲存成 `news.crawlers.db.schema.RawNews` 的格式, 為了進一步取得新聞標題與內文等資訊, 必須對 HTML 進行拆解.

以下表格為拆解後所得之欄位資訊, 所有資料將會儲存成 `news.parse.db.schema.ParsedNews` 的格式.

|欄位|型態|限制|意義|
|-|-|-|-|
|id|INTEGER|PRIMARY KEY AUTOINCREMENT|流水號|
|article|TEXT|NOT NULL|新聞內文|
|category|TEXT|DEFAULT NULL|新聞種類|
|company_id|INTEGER|NOT NULL|新聞公司|
|reporter|TEXT|DEFAULT NULL|記者|
|timestamp|INTEGER|NOT NULL|新聞發佈日期與時間|
|title|TEXT|NOT NULL|新聞標題|
|url_pattern|TEXT|NOT NULL|新聞 URL|

- `compand_id` 的對照資訊請見 `news.crawlers.util.normalize.COMPANY_ID_LOOKUP_TABLE`.
  - 以數字代表公司名稱進行儲存可以節省儲存空間.
  - 可用 `news.crawlers.util.normalize.get_company_id` 進行轉換

## 範例 Example

```sh
python -m news.parse.main \
    --batch_size 1000     \
    --db_name rel/my.db   \
    --db_name /abs/my.db  \
    --db_dir rel_dir      \
    --db_dir /abs_dir     \
    --debug               \
    --save_db_name out.db
```
