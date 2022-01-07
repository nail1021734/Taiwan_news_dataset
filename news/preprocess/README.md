# Preprocess Scripts

對 parse 完的新聞進行多種前處理.

## 執行範例 Example

```sh
python -m news.preprocess.main       \
  --batch_size 1000                  \
  --db_name rel/my.db                \
  --db_name /abs/my.db               \
  --db_dir rel_dir                   \
  --db_dir /abs_dir                  \
  --save_db_name out.db              \
  --debug                            \
  --use_min_length_filter 200        \
  --use_max_length_filter 1000       \
  --use_url_filter                   \
  --use_parentheses_filter           \
  --use_brackets_filter              \
  --use_curly_brackets_filter        \
  --use_lenticular_brackets_filter   \
  --use_not_cjk_filter               \
  --use_emoji_filter                 \
  --use_ORG_with_id org              \
  --use_PERSON_with_id per           \
  --use_LOC_with_id loc              \
  --use_GPE_with_id loc              \
  --use_date_replacer                \
  --use_english_replacer             \
  --use_guillemet_replacer           \
  --use_number_replacer
```

## 特殊參數介紹

輸入時只要有輸入前處理方法的名字就會執行此前處理方法, 並且不需要照順序輸入, 程式會自動將輸入的前處理方法照正確的順序執行, 另外在執行預處理時會先進行 NFKC 正規化以及將多個空白合成一個空白的步驟.

- `use_min_length_filter`: 要保留的文章最短長度, 預設為 0.
- `use_max_length_filter`: 要保留的文章最長長度, 預設為 -1 表示不限制文章最長長度.
- `use_url_filter`: 是否將 url 過濾掉.
- `use_parentheses_filter`: 將小括號內的句子以及括號一起過濾掉.
- `use_brackets_filter`: 將中括號內的句子以及括號一起過濾掉.
- `use_curly_brackets_filter`: 將大括號內的句子以及括號一起過濾掉.
- `use_lenticular_brackets_filter`: 將透鏡狀括號(例如: 】)內的句子以及括號一起過濾掉.
- `use_not_cjk_filter`: 將中文, 英文, 數字以及特定標點符號(包含.~<、,。《?>*\-!》:」「+%/()\[\]【】)以外的符號過濾掉.
- `use_emoji_filter`: 過濾掉 emoji 符號.
- `ner_class ORG PERSON LOC`: 選擇哪些 NER 類別要被替換為 tag, 目前總共 10 種類別可以選擇(可多選), 可選的類別請見 **NER 類別**區塊
- `ner_need_id_class ORG PERSON LOC`: 選擇要被替換為 tag 的 NER 類別相同的詞是否要有相同 id 來表示(可多選).
- `ner_device`: 選擇 NER 時使用的設備, 0 代表 cuda:0, -1 表示使用 cpu, 預設為 0.
- `use_date_replacer`: 當對資料集進行 NER 類別的替換時, 是否將 DATE 類別中的數字轉換為 `<num>`.
- `use_english_replacer`: 將英文開頭的連續英文, 數字或空白換成 `<en>` tag.
- `use_guillemet_replacer`: 將書名號內的詞換為 `<unk>`, 並且留下書名號本身.
- `use_number_replacer`: 將阿拉伯數字換為 `<num>` tag.

## NER 類別

使用 `use_{NER類別名稱}` 後加上欲替換的 tag 樣式即可將此 NER 類別的所有實體換成指定的 tag (如需加上各自的 id 請使用 `use_{NER類別名稱}_with_id`)目前可使用的類別如下

- GPE
- PERSON
- ORG
- NORP
- LOC
- FAC
- PRODUCT
- WORK_OF_ART
- EVENT
- LAW

範例: `--use_ORG org` 會將 ORG 類別換成 `<org>`,而 `--use_ORG_with_id org` 會換成 `<org0>`

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
