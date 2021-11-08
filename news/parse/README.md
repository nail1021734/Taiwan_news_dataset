# Parse Scripts

爬蟲完後所有新聞 HTML 都儲存成 `news.crawlers.db.schema.RawNews` 的格式, 為了進一步取得新聞標題與內文等資訊, 必須對 HTML 進行拆解.

## 執行範例 Example

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

## 資料格式

以下表格為拆解後所得之欄位資訊, 所有資料將會儲存成 `news.parse.db.schema.ParsedNews` 的格式.

- 所有文字都經過 `news.parse.util.normalize.NFKC` 進行標準化.
- 預設為 `NULL` 的資料在 `python` 中為 `None`.

|欄位|型態|限制|意義|
|-|-|-|-|
| `id`         | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` |流水號|
| `article`    | `TEXT`    | `NOT NULL`                  |新聞內文|
| `category`   | `TEXT`    | `DEFAULT NULL`              |新聞種類|
| `company_id` | `INTEGER` | `NOT NULL`                  |新聞公司|
| `reporter`   | `TEXT`    | `DEFAULT NULL`              |記者|
| `timestamp`  | `INTEGER` | `NOT NULL`                  |新聞發佈日期與時間|
| `title`      | `TEXT`    | `NOT NULL`                  |新聞標題|
| `url_pattern`| `TEXT`    | `NOT NULL`                  |新聞 URL|

### `id`

- 資料庫中的流水號, 由於我們使用 SQLite, 因此所有 `id` 皆為正整數.
- 在 python 中 `id` 為內建函數, 因此我們使用 `idx` 存取流水號
- ex: 如果 `isinstance(parsed_news, ParsedNews)` 為真, 則可使用 `parsed_news.idx`.

### `article`

- 新聞的內文, 包含一至多個段落.
- 段落與段落之間以空格區分.
  - 新聞內文品質參差不齊, 有時文章中會有多餘空格, 因此使用空格進行斷句並非 100% 精確.
  - 同理, 使用 `。？！` 等符號進行斷句並非 100% 精確.
- 儘量濾除雜訊 (best effort), 包含
  - 移除記者資訊
  - 移除內容提示
  - 移除圖例與圖片說明
  - 其他移除內容請參考各新聞的解析工具 (ex: 中央社請見 `news.parse.cna`)
- ex: 如果 `isinstance(parsed_news, ParsedNews)` 為真, 則可使用 `parsed_news.article`.

### `category`

- 新聞的種類, 可能包含多個資訊, 所有資訊以 `,` 分隔.
- 並不是所有的新聞都有 `category`, 此案例常見於新唐人.
- ex: 如果 `isinstance(parsed_news, ParsedNews)` 為真, 則可使用 `parsed_news.category`.

### `company_id`

- 以數字代表公司名稱進行儲存, 如此可以節省儲存空間.
- 可用 `news.crawlers.util.normalize.get_company_id` 進行轉換
- `compand_id` 的對照資訊請見 `news.crawlers.util.normalize.COMPANY_ID_LOOKUP_TABLE`.
- ex: 如果 `isinstance(parsed_news, ParsedNews)` 為真, 則可使用 `parsed_news.company_id`.

### `reporter`

- `reporter` 可能包含多個資訊, 所有資訊以 `,` 分隔.
- 並不是所有的新聞都有 `reporter`, 此案例常見於新唐人.
- 在此階段我們無法區隔人名、地名與國名, 所有資訊都會一起納入 `reporter`.
- ex: 如果 `isinstance(parsed_news, ParsedNews)` 為真, 則可使用 `parsed_news.reporter`.

### `timestamp`

- `timestamp` 為整數, 為 POSIX 日期與時間格式, 精確度最多到秒.
- 由與符合 POSIX, 所有時間皆以 UTC 時區表示.
- 可使用 `news.parse.db.schema.ParsedNews.get_datetime` 取得 `datetime` 物件.
- 可使用 `news.parse.db.schema.ParsedNews.get_datetime_str` 轉換成 `YYYY-mm-dd HH:MM:SS+0000`.
  - ex: `1995-10-12 17:59:59+0000`
- ex: 如果 `isinstance(parsed_news, ParsedNews)` 為真, 則可使用 `parsed_news.timestamp`.

### `title`

- 新聞的標題, 包含一至多個片段.
- 片段與片段之間以空格區分.
  - 新聞標題品質參差不齊, 有時文章中會有多餘空格, 因此使用空格進行斷句並非 100% 精確.
  - 標題幾乎不使用標點符號, 因此無法使用 `。？！` 等符號進行斷句.
- 儘量濾除雜訊 (best effort), 包含
  - 移除內容提示
  - 移除圖例與圖片說明
  - 其他移除內容請參考各新聞的解析工具 (ex: 中央社請見 `news.parse.cna`)
- ex: 如果 `isinstance(parsed_news, ParsedNews)` 為真, 則可使用 `parsed_news.title`.

### `url_pattern`

- `url_pattern` 在不同 `company_id` 時具有不同的格式, 但是在相同的 `company_id` 之下具有一致的格式.
  - ex: 如果 `company_id == 1` (中央社), 則 `url_pattern` 的格式為 `YYYYmmddxxxx`, 其中 `xxxx` 為流水號.
  - ex: 如果 `company_id == 6` (中央社), 則 `url_pattern` 的格式為 `YYYY-mm-dd-xxxxxx`, 其中 `xxxxxx` 為流水號.
  - 與 `compand_id` 之間的格式對照請見 `news.crawlers.util.normalize.COMPRESS_URL_PATTERN_LOOKUP_TABLE`.
- ex: 如果 `isinstance(parsed_news, ParsedNews)` 為真, 則可使用 `parsed_news.url_pattern`.
