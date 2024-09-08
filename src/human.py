import json
import pandas as pd
from src.functional import rouge_l, find_common_elements


def datas_process(data, temp: dict):
    # 案例编号
    num = data["案例编号"]
    temp[num] = {
        'task1': data["信息抽取能力-核心临床信息"],
        'task2': data["病机答案"],
        'task3': data["证候答案"],
        'task4': data["临证体会"],
        'task5': data["辨证"]
    }


def human_score():
    answer, human_scores = {}, {}
    with open("data/train.json", "r") as f:
        answers = json.load(f)
    with open("data/human.json", "r") as f:
        datas = json.load(f)
    for ans in answers:
        datas_process(ans, answer)
    for data in datas[-5:]:
        datas_process(data, human_scores)
    scores, count = 0, 0
    result = pd.DataFrame(
        columns=['抽取', '病机', '证候', '临证', '辨证', '得分'])
    for key, value in human_scores.items():
        ans = answer[key]
        ans['task1'] = ans['task1'].replace('，', ',')
        ans['task4'] = ans['task1'].replace('，', ',')
        ans['task5'] = ans['task1'].replace('，', ',')
        task1_score = rouge_l(ans['task1'], value['task1'])['rouge-l']['r']
        task4_score = rouge_l(ans['task4'], value['task4'])['rouge-l']['r']
        task5_score = rouge_l(ans['task5'], value['task5'])['rouge-l']['r']
        task2_score = find_common_elements(
            ans['task2'].split(";"), value['task2'].split(";"))
        task3_score = find_common_elements(
            ans['task3'].split(";"), value['task3'].split(";"))
        score = task1_score*0.1+task2_score*0.35 + \
            task3_score * 0.35+task4_score*0.1+task5_score*0.1
        result.loc[f"抽取测试{count+1}"] = [task1_score, task2_score, task3_score,
                                        task4_score, task5_score, score]
        scores += score
        count += 1
    # 将 DataFrame 格式化为百分数形式
    result = result.applymap(lambda x: f'{x*100:.2f}%')
    print(result)
    print(f"测试集平均准确率为：{scores/count:.2%}")
    result.to_excel("data/human_score.xlsx")
