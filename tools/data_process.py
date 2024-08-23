import os
import json


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


def task_2_step():
    task = open('/opt/project/alitianchi/data/task.json',
                'r', encoding='utf-8')
    save = open('/opt/project/alitianchi/data/提交内容.txt',
                'w', encoding='utf-8')
    task_json = json.load(task)
    for data in task_json:
        patient_id = data['input']['案例编号']
        task_1 = data['task_1'].replace('核心临床信息: ', '')
        print(patient_id)
        print(task_1, end='\n\n')
    task.close()
    save.close()


if __name__ == '__main__':
    task_1_step()
