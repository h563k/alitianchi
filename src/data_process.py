def answer_process(data, choice, answer):
    disease = {}
    for key in data[choice].split(';'):
        key, val = key.split(':')
        disease[key] = val
    result = [disease[key] for key in data[answer].split(';')]
    return ';'.join(result)


def data_procrss(data, type):
    if type == 'task_1':
        temp = f"""### 临床资料:
{data['临床资料']}

### 回答格式
信息抽取能力-核心临床信息: {data['信息抽取能力-核心临床信息']}
"""
    elif type == 'task_2':
        temp = f"""### 临床资料:
{data['临床资料']}

### 病机选项:
{data['病机选项']}

### 回答格式

病机答案: {answer_process(data, '病机选项', '病机答案')}
"""
    elif type == 'task_3':
        temp = f"""### 临床资料:
{data['临床资料']}

### 证候选项:
{data['证候选项']}

### 回答格式

证候答案: {answer_process(data, '证候选项', '证候答案')}
"""
    elif type == 'task_4':
        temp = f"""### 临床资料:
{data['临床资料']}

### 回答格式

临证体会: {data['临证体会']}
"""
    return temp
