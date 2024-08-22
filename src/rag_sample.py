import yaml
import json
from http import HTTPStatus
import dashscope
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from src.config import ModelConfig
from src.functionals import CustomRetrievalQA
from src.data_process import data_procrss
from src.promot import custom_prompt


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
            # print(item)
            data.append(item)
    return data


def local_openai(prompt):
    dashscope.api_key = config.dashscope_key
    response = dashscope.Generation.call(
        model='qwen2-72b-instruct',
        prompt=prompt,
        seed=42,
        top_p=0.8,
        result_format='message',
        max_tokens=1000,
        temperature=0.2,
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
    qa = CustomRetrievalQA(retriever=vectorstore, qa_chain=local_openai)
    # 调用自定义的 RetrievalQA 并获取答案和源文档
    query = qa.run(query, type, custom_prompt, return_source_documents)
    answer = local_openai(query)
    return answer.output.choices[0].message.content


def answer_process():
    result = []
    predict_file_path = config.predict_file_path
    save = open(config.save_file_path, 'w', encoding='utf-8')
    with open(predict_file_path, 'r', encoding='utf-8') as file:
        querys = json.load(file)
        for query in querys:
            answer_task1 = rag_miedical(query, False, 'task_1')
            result.append({
                'input': query,
                'task_1': answer_task1
            })
            print(f"{query['案例编号']}")
        json.dump(result, save, ensure_ascii=False)
        save.close()
