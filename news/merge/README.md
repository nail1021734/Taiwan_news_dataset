# Merge

## Parameters

- `dir_path`: Select a directory that contain databases which we want to merge into single database.(Path root: `data`)
- `save_db`: Specify database to save result.(Path root: `data`)
- `reserve_id`: Specify if reserve origin id.

## example

```sh
python -m news.merge.main --dir_path ftv_split --save_db ftv_merge.db --reserve_id False
```