import os
import json
import time
from typing import List
from src.promot import config, data_process_save_task2, data_process_predict_task2
from src.functional import find_common_elements
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
                time.sleep(6)
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


def data_save_and_scores_multiple(types: str, model_names: List[str], ranges: List[int], stream=False):
    counts = list(range(ranges[0], ranges[1]+10, 10))
    counts = [[counts[i-1], j] for i, j in enumerate(counts)][1:]
    for count in counts:
        for model_name in model_names:
            data_save_and_scores(types, model_name, count, stream)

# 上面的代码主要用于完成单个api对任务的预测
# 接下来主要用于实现多agent计算, 采取合适的策略使得分数进一步提高


def multiple_agent_process(types: str, model_names: List[str]):
    if types == 'task2':
        datas = {}
        for model_name in model_names:
            file_path = f"{config.save_file_path}/{types}/{model_name}"
            _, _, files = os.walk(file_path).__next__()
            temp_data = {}
            for file in files:
                with open(os.path.join(file_path, file), 'r') as f:
                    data = json.load(f)
                    for item in data[:-1]:
                        temp_data.update(item)
            datas[model_name] = temp_data
        return datas


def multiple_agent_score(types: str, model_names: List[str]):
    if types == 'task2':
        multiple_data = {}
        datas = multiple_agent_process(types, model_names)
        for model_name in model_names:
            data = datas[model_name]
            count, scores = 0, 0
            for key, value in data.items():
                count += 1
                choices = value['病机预测'].split(';')
                answer = value['病机答案'].split(';')
                score = find_common_elements(choices, answer)
                scores += score
                if multiple_data.get(key):
                    multiple_data[key]['病机预测'][model_name] = choices
                    multiple_data[key]['病机分数'][model_name] = score
                else:
                    multiple_data[key] = {
                        '病机预测': {model_name: choices},
                        '病机答案': value['病机答案'],
                        '病机分数': {model_name: score}
                    }
            if multiple_data.get('模型总得分'):
                multiple_data['模型总得分'][model_name] = scores/count
            else:
                multiple_data['模型总得分'] = {
                    model_name: scores/count
                }
        count, scores = 0, 0
        for patient_id, data in multiple_data.items():
            if not data.get('病机预测'):
                continue
            # 生成包含 'A' 到 'I' 的字符集合
            letters = set(chr(i) for i in range(ord('A'), ord('I')+1))
            for key in data['病机预测'].keys():
                temp = data['病机预测'][key]
                letters = list(set(letters).intersection(set(temp)))
                if not letters:
                    letters = data['病机预测']['glm']
            score = find_common_elements(letters, data['病机答案'].split(';'))
            count += 1
            scores += score
            multiple_data[patient_id]['病机分数']['混合模型'] = score
        multiple_data['模型总得分']['混合模型'] = scores/count
        # print(multiple_data['模型总得分'])
        count = 0
        for key, value in multiple_data.items():
            if key == '模型总得分':
                continue
            if value['病机分数']['glm'] > value['病机分数']['qwen']:
                count += 1
                print(key, value, count)
