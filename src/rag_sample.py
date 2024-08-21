import yaml
import json
from langchain_openai import ChatOpenAI
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


def local_openai():
    client = ChatOpenAI(base_url="http://127.0.0.1:8000/v1",
                        openai_api_key='0',
                        temperature=0.1,
                        max_tokens=4096,
                        )
    return client


def rag_miedical(query, return_source_documents, type):
    model_name = config.embedding_path
    # 步骤3: 生成嵌入
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    documents = json_loader(type)
    llm = local_openai()
    vectorstore = FAISS.from_texts(documents, embeddings)
    qa_chain = load_qa_chain(llm, chain_type="stuff")
    # 步骤3: 实例化自定义的 RetrievalQA
    retriever = vectorstore.as_retriever()
    qa = CustomRetrievalQA(retriever=retriever, qa_chain=qa_chain)
    # 调用自定义的 RetrievalQA 并获取答案和源文档
    answer = qa.run(query, type, custom_prompt, return_source_documents)
    return answer
