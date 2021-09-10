# Taiwan News Data project

## README link

- [crawlers](news/crawlers/README.md)
- [formatter](news/formatter/README.md)
- [merge](news/merge/README.md)
- [migration](news/migration/README.md)
- [parse](news/parse/README.md)
- [preprocess](news/preprocess/README.md)
- [split](news/split/README.md)

## File Directory

```sh
news
|-formatter
|    |-README.md
|	 |-formatter.py
|    |-schema.py
|-crawlers
|    |-README.md
|    |-company.py
|    |-main.py
|    |-db
|    |    |-read.py
|    |    |-write.py
|    |    |-schema.py
|    |    |-util.py
|    |-util
|    |    |-normalize.py
|    |    |-date_parse.py
|    |    |-pre_parse.py
|    |    |-status_code.py
|-parse
|    |-README.md
|    |-company.py
|    |-main.py
|    |-db
|    |    |-read.py
|    |    |-write.py
|    |    |-schema.py
|    |    |-util.py
|-split
|    |-README.md
|    |-split.py
|    |-main.py
|    |-db
|    |    |-create.py
|    |    |-read.py
|    |    |-write.py
|    |    |-util.py
|-preprocess
|    |-README.md
|    |-company.py
|    |-main.py
|    |-db
|    |    |-read.py
|    |    |-write.py
|    |    |-schema.py
|    |    |-util.py
|-merge
|    |-README.md
|    |-merge.py
|    |-main.py
|    |-db
|    |    |-read.py
|    |    |-write.py
|    |    |-schema.py
|    |    |-util.py
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