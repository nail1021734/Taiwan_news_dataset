python -m news.preprocess.main --source ftv_split --function ner_tag_subs --target ftv_ner_subs --NER_format '[{"type":["ORG"],"tag":"org","NeedID":true}]' --NER_result ftv_NER_result

python -m news.preprocess.main --source ftv_split --function NER_dataset --target ftv_NER_result

python -m news.preprocess.main --source ftv_split --function length_filter --target ftv_len --min_length 200 --max_length 1000