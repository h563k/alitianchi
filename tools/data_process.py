import os
import json
import re


def task_1_step():
    task1 = open('/opt/project/alitianchi/data/task1.json',
                 'r', encoding='utf-8')
    task5 = open('/opt/project/alitianchi/data/task5.json',
                 'r', encoding='utf-8')
    task1234 = open('/opt/project/alitianchi/data/task1234.json',
                    'r', encoding='utf-8')
    task_1_json = json.load(task1)
    task5_json = json.load(task5)
    task1234_json = json.load(task1234)

    result = []
    for data in task1234_json:

        for temp in task5_json:
            if data['input'] == temp['input']:
                data['task_5'] = temp['task_5']
                break
            for temp2 in task_1_json:
                if data['input'] == temp2['input']:
                    data['task_1'] = temp2['task_1']
                    result.append(data.copy())
                    break
    with open('/opt/project/alitianchi/data/task.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)
    task5.close()
    task1234.close()


def task_1_process(task_1):
    task_1 = task_1.replace('核心临床信息:', '')
    task_1 = task_1.replace('###信息抽取\n', '')
    task_1 = task_1.replace(',', ';')
    task_1 = task_1.replace('，', ';')
    if '\n\n' in task_1:
        task_1 = task_1.split('\n\n')[0]
    task_1 = task_1.split('。')[0]
    task_1 = task_1.split(';')
    temp = []
    for item in task_1:
        if re.findall(r'[一-九]|\d+|\s+|\(|\)', item) or len(item) > 7:
            continue
        temp.append(item)
    task_1 = ';'.join(temp)
    return task_1


def answer_process(patient, choice):
    data = open('/opt/project/alitianchi/data/A榜.json', 'r', encoding='utf-8')
    data_json = json.load(data)
    temp = ""
    temp_dict = {}
    for data in data_json:
        if data['案例编号'] == patient:
            temp = data[choice]
            break
    temp = temp.split(';')
    for item in temp:
        value, key = item.split(':')
        temp_dict[key] = value
    return temp_dict


def task_2_process(task_2, patient, choices):
    task_2 = task_2.replace('病机答案:', '')
    task_2 = task_2.split('\n')[0]
    if re.findall(r'[A-Z]', task_2):
        task_2 = [temp.split(':')[0].strip() for temp in task_2.split(';')]
        task_2 = ';'.join(task_2)
    else:
        temp = []
        answer = answer_process(patient, choices)
        for choice in task_2.split(';'):
            choice = choice.strip()
            try:
                temp.append(answer[choice])
            except KeyError as e:
                print(f"patient:{patient}, choices:{choices},choice:{e},")
        task_2 = ';'.join(temp)
    return task_2


def task_4_process(task_4):
    task_4 = task_4.replace('临证体会：', '').replace('### 临证体会', '')
    while task_4.startswith('\n') or task_4.endswith('\n'):
        task_4 = task_4.strip('\n')
    if '\n' in task_4:
        task_4 = task_4.split('\n')[0]
    task_4 = task_4.strip('\n')
    return task_4


def task_5_process(task_5):
    task_5 = task_5.replace('### 辨证', '')

    def clean(task_5, word):
        if word in task_5:
            task_5 = task_5.split(word)[0]
        return task_5
    clean(task_5, '解析')
    clean(task_5, '分析')
    while task_5.startswith('\n') or task_5.endswith('\n'):
        task_5 = task_5.strip('\n')
    task_5 = task_5.split('\n')
    task_5 = "".join(task_5)
    task_5 = task_5.strip('\n').replace('辨证要点', '辨证')
    print(task_5)
    return task_5


def task_2_step():
    task = open('/opt/project/alitianchi/data/task_temp.json',
                'r', encoding='utf-8')
    save = open('/opt/project/alitianchi/data/提交内容.txt',
                'w', encoding='utf-8')
    task_json = json.load(task)
    answer = ""
    for data in task_json:
        patient_id = data['input']['案例编号']
        task_1 = task_1_process(data['task_1'])
        task_2 = task_2_process(data['task_2'], patient_id, '病机选项')
        task_3 = task_2_process(data['task_3'], patient_id, '证候选项')
        task_4 = task_4_process(data['task_4'])
        task_5 = task_5_process(data['task_5'])
        print(patient_id)
        text = f"{patient_id}@{task_1}@{task_2}@{task_3}@临证体会：{task_4}@{task_5}"
        answer += text + '\n'
    save.write(answer)
    task.close()
    save.close()


if __name__ == '__main__':
    task_2_step()
