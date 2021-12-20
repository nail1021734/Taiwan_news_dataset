# Split

將一個大型 SQLite 資料庫切割成多個小 SQLite 資料庫.
由於單一 SQLite 檔案過大無法一次讀入記憶體, 因此我們可以切成多個大小等分的小檔案.

## TL;DR.

如果你不是開發者, 則你不需要使用與了解 `news.split` 此模組的功能.

## For Developers

聰明的你一定會問: 為什麼不要用 `SELECT * FROM table LIMIT 100` 這種語法進行讀取部份資料?
理由是: 我們在進行 parsing 程式撰寫的過程中, 如果修改一次程式細節就需要進行**所有**資料的測試, 則必須等待**非常長**的時間.
因此我們希望只針對檔案較小的資料庫進行測試, 避免等待過久與加速開發流程.

## 執行範例 Example

```sh
python -m news.split.main        \
        --db_name rel/my.db      \
        --db_name /abs/my.db     \
        --db_dir rel_dir         \
        --db_dir /abs_dir        \
        --db_type raw            \
        --debug                  \
        --records_per_split 1000
```
