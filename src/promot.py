import re
from tools.standard_log import log_to_file
from src.llm_api import local_openai
from tools.config import ModelConfig
from src.functional import find_common_elements


config = ModelConfig()


def data_process_online_task2(data, model_name):
    prompt = f"""{data['病机选项']} 请解释以上这些中医词汇,每行解释一个词汇"""
    answer = local_openai(system_prompt=None,
                          prompt=prompt, model_name=model_name, stream=None)
    temp = []
    for ans in answer.split('\n'):
        if re.findall('[A-Z]+', ans):
            temp.append(ans)
    answer = '\n'.join(temp)
    prompt = f"""### 临床资料
{data['临床资料']}
### 病机选项
{data['病机选项']}
### 病机解释
{answer}
请根据临床资料最符合的病机选项(单选或多选),给出答案即可,不需要任何额外回答,格式如下：
病机：
"""
    print(prompt)
    answer = local_openai(system_prompt=None,
                          prompt=prompt, model_name=model_name, stream=None)


@log_to_file
def data_process_predict_task2(data, model_name, stream):
    if re.findall('qwen', model_name) or model_name in ['kimi', 'glm']:
        prompt = f"""{data['病机选项']} 请解释以上这些中医词汇,每行解释一个词汇"""
        answer = data_process_online_task2(data, model_name)
    elif re.findall('huatuo', model_name):
        system_prompt = """请根据中医理论，分析临床资料，并从提供的选项中选择最符合的病机，不需要任何额外回答,格式如下：
病机：
"""
        prompt = f"""### 临床资料
{data['临床资料']}
### 病机选项
{data['病机选项']}
"""
        answer = local_openai(system_prompt=system_prompt,
                              prompt=prompt, model_name=model_name, stream=stream)
    else:
        answer = ''
    pathogenesis = re.findall('[A-Z]+', answer)
    temp = []
    for pathogenesi in pathogenesis:
        if len(pathogenesi) == 1:
            temp.append(pathogenesi)
        elif len(pathogenesi) > 1:
            temp.extend(list(pathogenesi))
    pathogenesis = list(set(temp))
    return [pathogenesis, answer]


def data_process_save_task2(datas, answers):
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
