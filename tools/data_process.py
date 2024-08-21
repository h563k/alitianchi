import os
import json


def answer_process(data, choice, answer):
    disease = {}
    for key in data[choice].split(';'):
        key, val = key.split(':')
        disease[key] = val
    result = [disease[key] for key in data[answer].split(';')]
    return ';'.join(result)


procrss = []
with open('data/train.json', 'r') as f:
    datas = json.load(f)
    for data in datas:

        temp = f"""### 临床资料:
{data['临床资料']}

### 病机选项:
{data['病机选项']}

### 证候选项:
{data['证候选项']}

### 回答格式

信息抽取能力-核心临床信息: {data['信息抽取能力-核心临床信息']}
病机答案: {answer_process(data, '病机选项', '病机答案')}
证候答案: {answer_process(data, '证候选项', '证候答案')}
临证体会: {data['临证体会']}
"""
        procrss.append(temp)

with open('data/train_process.json', 'w') as f:
    json.dump(procrss, f, ensure_ascii=False)
