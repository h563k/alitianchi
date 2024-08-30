import json
from typing import List
from src.promot import config, data_process_save_task2, data_process_predict_task2
from tools.standard_log import log_to_file


@log_to_file
def data_process(type, model_name, counts, stream):
    json_file_path = config.json_file_path
    with open(json_file_path, 'r') as f:
        datas = json.load(f)
    result = {}
    for i, data in enumerate(datas):
        if i > counts:
            break
        patient_id = data['案例编号']
        if type == 'task1':
            pass
        if type == 'task2':
            try:
                result[patient_id] = data_process_predict_task2(
                    data, model_name, stream)
            except RecursionError as e:
                print(e)
                continue
        if type == 'task3':
            pass
        if type == 'task4':
            pass
        if type == 'task5':
            pass
    return result


def data_save_and_scores(type, model_name, counts, stream=False):
    answers = data_process(type, model_name, counts, stream)
    if not answers:
        return
    # 读取本地评估用分数计算文件 train.json
    save_file = []
    json_file_path = config.json_file_path
    with open(json_file_path, 'r', encoding='utf-8') as f:
        datas = json.load(f)
    if type == 'task2':
        save_file = data_process_save_task2(datas, answers)
    # 大模型回答保存到本地
    save_file_path = f"{config.save_file_path}/{type}_{model_name}.json"
    with open(save_file_path, 'w') as f:
        json.dump(save_file, f, ensure_ascii=False)


def data_save_and_scores_multiple(type: str, model_names: List[str], counts: int, stream=False):
    for model_name in model_names:
        data_save_and_scores(type, model_name, counts, stream)
