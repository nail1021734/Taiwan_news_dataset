# Preprocess Scripts

對 parse 完的新聞進行多種前處理.

## 執行範例 Example

```sh
python -m news.preprocess.main   \
    --batch_size 1000            \
    --db_name rel/my.db          \
    --db_name /abs/my.db         \
    --db_dir rel_dir             \
    --db_dir /abs_dir            \
    --save_db_name out.db        \
    --debug                      \
    --function_flag 11111111111  \
    --NER_flag 0110100000        \
    --NER_NeedID_flag 0110100000 \
    --filter_date                \
    --min_length 200             \
    --max_length 1000
```

## 特殊參數介紹

- `function_flag`: 選擇要執行的前處理方法. 總共11種前處理方法分別對應到11個 bit 每個 bit 照順序代表的前處理方法如下
    1. `NFKC`: 對輸入資料集進行 NFKC 正規化.
    2. `url_filter`: 將輸入資料集的 url 過濾掉.
    3. `whitespace_filter`: 將多個空白換成一個.
    4. `parentheses_filter`: 將小括號, 中括號, 以及【】內的句子以及括號一起過濾掉.
    5. `not_CJK_filter`: 將中文, 英文, 數字以及特定標點符號(包含.~<、,。《?>*\-!》:」「+%/()\[\]【】)以外的符號過濾掉.
    6. `length_filter`: 將長度小於 `min_length` 或大於 `max_length` 的文章過濾掉, 預設為小於200或大於1000的文章會被過慮掉.
    7. `ner_tag_subs_flag_version`: 將 NER 辨識出來的某個類別替換為 tag,需給定 `NER_flag` 以及 `NER_NeedID_flag` 參數, 並且預設會將日期類別中的數字替換為 `<num>`, 若不想將日期過濾掉可以設定 `filter_date` 參數為 `False`(預設為 `True`).
    8. `english_to_tag`: 將英文開頭的連續英文, 數字或空白換成 `<en>` tag.
    9. `guillemet_filter`: 將書名號內的詞換為 `<unk>`, 並且留下書名號本身.
    10. `number_filter`: 將阿拉伯數字換為 `<num>` tag.
- `NER_flag`: 選擇哪些 NER 類別要被替換為 tag, 每個 bit 對應到的類別順序如下
    1. GPE 替換為 `<gpe>`.
    2. PERSON 替換為 `<per>`.
    3. ORG 替換為 `<org>`.
    4. NORP 替換為 `<nrp>`.
    5. LOC 替換為 `<loc>`.
    6. FAC 替換為 `<fac>`.
    7. PRODUCT 替換為 `<prdt>`.
    8. WORK_OF_ART 替換為 `<woa>`.
    9. EVENT 替換為 `<evt>`.
    10. LAW 替換為 `<law>`.
- `NER_NeedID_flag`: 選擇要被替換為 tag 的 NER 類別, 相同的詞是否要有相同 id 來表示, 每個 bit 對應到的類別順序如下.
    1. `<gpe>` 後加上 id, 例如： `<gpe1>`.
    2. `<per>` 後加上 id, 例如： `<per1>`.
    3. `<org>` 後加上 id, 例如： `<org1>`.
    4. `<nrp>` 後加上 id, 例如： `<nrp1>`.
    5. `<loc>` 後加上 id, 例如： `<loc1>`.
    6. `<fac>` 後加上 id, 例如： `<fac1>`.
    7. `<prdt>` 後加上 id, 例如： `<prdt1>`.
    8. `<woa>` 後加上 id, 例如： `<woa1>`.
    9. `<evt>` 後加上 id, 例如： `<evt1>`.
    10. `<law>` 後加上 id, 例如：`<law1>` .
- `filter_date`: 當對資料集進行 NER 類別的替換時, 是否將 DATE 類別中的數字轉換為 `<num>`.
- `min_length`: 執行 `length_filter` 時, 要保留的文章最短長度.
- `max_length`: 執行 `length_filter` 時, 要保留的文章最長長度.

## 資料格式

**和 parse 相同.**

- 表格名稱為 `preprocessed_news`.
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
