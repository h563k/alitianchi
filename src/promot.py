import re
import json
from tools.standard_log import log_to_file
from src.llm_api import local_openai
from tools.config import ModelConfig
from src.functional import rouge_l, find_common_elements


config = ModelConfig()


def data_process_predict_task3(data, model_name):
    if re.findall('qwen', model_name):
        data = f"""### 临床资料
    {data['临床资料']}
    ### 病机选项
    {data['病机选项']}
    请根据临床资料，选出合适的病机(单选或多选)，只需要给出答案，不需要任何额外回答,格式如下：
    病机：
    """
        print(data)
        answer = local_openai(data, model_name)
        answer = answer.split("\n")
        temp = []
        for ans in answer:
            if ans:
                temp.append(ans)
        answer = temp
        print(temp)
        Pathogenesis = re.findall('[A-Za-z]+', answer[0])
        temp = []
        for pathogenesi in Pathogenesis:
            if len(pathogenesi) == 1:
                temp.append(pathogenesi)
            elif len(pathogenesi) > 1:
                temp.extend(list(pathogenesi))
        Pathogenesis = list(set(temp))
        return [Pathogenesis, answer]


def data_process_save_task3(datas, answers):
    temp = {}
    for data in datas:
        temp[data["案例编号"]] = {
            "病机答案": data["病机答案"],
        }
    save_file = []
    count, scores1 = 0, 0
    for answer in answers.items():
        patient_id, result = answer
        temp_answer = temp[patient_id]
        score1 = find_common_elements(
            result[0], temp_answer["病机答案"].split(';'))
        save_file.append({patient_id: {
            "病机预测": ';'.join(result[0]),
            "病机答案": temp_answer["病机答案"],
            "病机得分": score1,
        }})
        count += 1
        scores1 += score1
    save_file.append({"总样本数": count, "病机总得分": scores1 / count})
    return save_file


@log_to_file
def data_process(type, model_name, counts):
    json_file_path = config.json_file_path
    with open(json_file_path, 'r') as f:
        datas = json.load(f)
    result = {}
    for i, data in enumerate(datas):
        if i > counts:
            break
        patient_id = data['案例编号']
        if type == 'taks_3':
            try:
                result[patient_id] = data_process_predict_task3(
                    data, model_name)
            except RecursionError as e:
                print(e)
                continue
    return result


def data_save_and_scores(type, model_name, counts):
    answers = data_process(type, model_name, counts)
    if not answers:
        return
    # 读取本地评估用分数计算文件 train.json
    json_file_path = config.json_file_path
    with open(json_file_path, 'r', encoding='utf-8') as f:
        datas = json.load(f)
    if type == 'taks_3':
        save_file = data_process_save_task3(datas, answers)
    # 大模型回答保存到本地
    save_file_path = f"{config.save_file_path}/{type}_{model_name}.json"
    with open(save_file_path, 'w') as f:
        json.dump(save_file, f, ensure_ascii=False)