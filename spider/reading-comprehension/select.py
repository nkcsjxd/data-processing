# https://huggingface.co/datasets/BAAI/COIG/tree/main
# 筛选出exam_instructions.jsonl里中文有解析的题目
import json

file_path = "D:\\Workspace\\PycharmProjects\\Code-pre\\crawler\\bmm_crawler\\read\\exam_instructions.jsonl"
with open(file_path, 'r', encoding='utf-8') as file:
    with open("result.json", 'a', encoding='utf-8') as result:
        for line in file:
            json_obj = json.loads(line)
            try:
                if json_obj["subject"] == "英语":
                    continue
                value = json_obj["textbox_answer_analysis"]
                if value == []:
                    continue
                json_str = json.dumps(json_obj, ensure_ascii=False)
                result.write(json_str)
                result.write('\n')
            except KeyError:
                continue
