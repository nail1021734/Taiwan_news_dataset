# Taiwan News Data project

蒐集台灣新聞網站與文字處理工具，主要應用於產生大量具有結構的繁體中文文本。

## Tools' Links

- [crawlers](news/crawlers)
  - 爬蟲腳本，用於蒐集新聞內容原始資訊（XML）
  - 新聞網站列表請見 [crawlers](news/crawlers/README.md)
- [formatter](news/formatter/README.md)
- [merge](news/merge/README.md)
- [migration](news/migration/README.md)
- [parse](news/parse/README.md)
- [preprocess](news/preprocess/README.md)
- [split](news/split/README.md)

## Project Directory

```sh
news
|- formatter
|    |- README.md
|	   |- formatter.py
|    |- schema.py
|- crawlers
|    |- README.md
|    |- company.py
|    |- main.py
|    |- db
|    |    |- read.py
|    |    |- write.py
|    |    |- schema.py
|    |    |- util.py
|    |- util
|    |    |- normalize.py
|    |    |- date_parse.py
|    |    |- pre_parse.py
|    |    |- status_code.py
|- parse
|    |- README.md
|    |- company.py
|    |- main.py
|    |- db
|    |    |- read.py
|    |    |- write.py
|    |    |- schema.py
|    |    |- util.py
|- split
|    |- README.md
|    |- split.py
|    |- main.py
|    |- db
|    |    |- create.py
|    |    |- read.py
|    |    |- write.py
|    |    |- util.py
|- preprocess
|    |- README.md
|    |- company.py
|    |- main.py
|    |- db
|    |    |- read.py
|    |    |- write.py
|    |    |- schema.py
|    |    |- util.py
|- merge
|    |- README.md
|    |- merge.py
|    |- main.py
|    |- db
|    |    |- read.py
|    |    |- write.py
|    |    |- schema.py
|    |    |- util.py
```

## DB Schema

### Crawler

|field|type|Constraint|
|-|-|-|
|id|int|primary key|
|company_id|tinyint||
|raw_xml|text||
|url_pattern|text||

### Parse

|field|type|Constraint|
|-|-|-|
|id|int|primary key|
|article|text||
|category|text||
|company_id|tinyint||
|datetime|int||
|reporter|text||
|title|text||
|url_pattern|text||

### Merge

|field|type|Constraint|
|-|-|-|
|id|int|primary key|
|article|text||
|category|text||
|company_id|tinyint||
|datetime|int||
|reporter|text||
|title|text||
|url_pattern|text||

### Pre-process

|field|type|Constraint|
|-|-|-|
|id|int|primary key|
|article|text||
|category|text||
|company_id|tinyint||
|datetime|int||
|reporter|text||
|title|text||
|url_pattern|text||

## Testing

```sh
# 執行測試
pipenv run test

# 觀看測試覆蓋範圍
pipenv run test-coverage
```
