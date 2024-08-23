import yaml
import json
from typing import List
from http import HTTPStatus
import dashscope
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from src.config import ModelConfig
from src.functionals import CustomRetrievalQA
from src.data_process import data_procrss


config = ModelConfig()


def promot_read():
    with open('scripts/prompt_settings.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data['medical_zh']['default']


def json_loader(type):
    data = []
    # 步骤1: 加载 JSON 数据
    json_file_path = config.json_file_path
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for item in json_data:
            item = data_procrss(item, type)
            data.append(item)
    return data


def local_openai(prompt):
    dashscope.api_key = config.dashscope_key
    response = dashscope.Generation.call(
        model=config.model_name,
        prompt=prompt,
        seed=42,
        top_p=0.8,
        result_format='message',
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        repetition_penalty=1.0
    )
    if response.status_code == HTTPStatus.OK:
        return response
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


def rag_miedical(query, return_source_documents, type):
    model_name = config.embedding_path
    # 步骤3: 生成嵌入
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    documents = json_loader(type)
    vectorstore = FAISS.from_texts(documents, embeddings)
    # 步骤3: 实例化自定义的 RetrievalQA
    qa = CustomRetrievalQA(vectorstore)
    # 调用自定义的 RetrievalQA 并获取答案和源文档
    query = qa.run(query, type, return_source_documents)
    if return_source_documents:
        return query
    else:
        answer = local_openai(query)
        return answer.output.choices[0].message.content


def answer_process(task_list: List[str]):
    result = []
    predict_file_path = config.predict_file_path
    save = open(config.save_file_path, 'w', encoding='utf-8')
    with open(predict_file_path, 'r', encoding='utf-8') as file:
        querys = json.load(file)
        temp = {}
        for query in querys:
            temp['input'] = query
            for task in task_list:
                temp[task] = rag_miedical(query, False, task)
            result.append(temp.copy())
            print(f"{query['案例编号']}")
        json.dump(result, save, ensure_ascii=False)
        save.close()
