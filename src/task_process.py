import os
import json
from typing import List
from src.promot import config, data_process_save_task2, data_process_predict_task2
from tools.standard_log import log_to_file


@log_to_file
def data_process(types, model_name, counts, stream):
    json_file_path = config.json_file_path
    with open(json_file_path, 'r') as f:
        datas = json.load(f)
    result = {}
    for i, data in enumerate(datas):
        if i > counts[1] or i < counts[0]:
            continue
        patient_id = data['案例编号']
        if types == 'task1':
            pass
        if types == 'task2':
            try:
                result[patient_id] = data_process_predict_task2(
                    data, model_name, stream)
            except RecursionError as e:
                print(e)
                continue
        if types == 'task3':
            pass
        if types == 'task4':
            pass
        if types == 'task5':
            pass
    return result


def data_save_and_scores(types, model_name, counts, stream=False):
    answers = data_process(types, model_name, counts, stream)
    if not answers:
        return
    # 读取本地评估用分数计算文件 train.json
    save_file = []
    json_file_path = config.json_file_path
    with open(json_file_path, 'r', encoding='utf-8') as f:
        datas = json.load(f)
    if types == 'task2':
        save_file = data_process_save_task2(datas, answers)
    # 大模型回答保存到本地
    save_path = f"{config.save_file_path}/{types}/{model_name}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_file_path = f"{save_path}/{counts[0]}_{counts[1]}.json"
    with open(save_file_path, 'w') as f:
        json.dump(save_file, f, ensure_ascii=False)


def data_save_and_scores_multiple(types: str, model_names: List[str], ranges: int, stream=False):
    counts = list(range(0, ranges+10, 10))
    counts = [[counts[i-1], j] for i, j in enumerate(counts)][1:]
    for count in counts:
        for model_name in model_names:
            data_save_and_scores(types, model_name, count, stream)

# 上面的代码主要用于完成单个api对任务的预测
# 接下来主要用于实现多agent计算, 采取合适的策略使得分数进一步提高


def multiple_agent_process(types: str, model_names: List[str]):
    datas = {}
    for model_name in model_names:
        file_path = f"{config.save_file_path}/{types}/{model_name}"
        _, _, files = os.walk(file_path).__next__()
        temp_data = {}
        for file in files:
            with open(os.path.join(file_path, file), 'r') as f:
                data = json.load(f)
                for patient in data:
                    print(type(patient))
                    key, value = patient.items()
                    temp_data[key] = value
        datas[types] = temp_data
    return datas


def multiple_agent_score():
    pass
