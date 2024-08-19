import yaml
import json
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from src.config import ModelConfig
from tools.functionals import CustomRetrievalQA


def promot_read():
    with open('scripts/prompt_settings.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data['medical_zh']['default']


def json_loader():
    data = []
    # 步骤1: 加载 JSON 数据
    json_file_path = 'data/train.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for item in json_data:
            item = f"""案例编号:{item['案例编号']}
'临床资料': {item['临床资料']}
'病机答案': {item['病机答案']}
'病机选项': {item['病机选项']}
'证候答案': {item['证候答案']}
'证候选项': {item['证候选项']}
'临证体会': {item['临证体会']}
            """
            data.append(item)
    return data


def local_openai():
    client = ChatOpenAI(base_url="http://127.0.0.1:8000/v1",
                        openai_api_key='0',
                        temperature=0.1,
                        max_tokens=2048,
                        )
    return client


def rag_miedical(query):
    config = ModelConfig()
    model_name = config.embedding_path
    custom_prompt = config.promot
    # 步骤3: 生成嵌入
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    documents = json_loader()
    llm = local_openai()
    vectorstore = FAISS.from_texts(documents, embeddings)
    qa_chain = load_qa_chain(llm, chain_type="stuff")
    # 步骤3: 实例化自定义的 RetrievalQA
    retriever = vectorstore.as_retriever()
    qa = CustomRetrievalQA(retriever=retriever, qa_chain=qa_chain)
    # 调用自定义的 RetrievalQA 并获取答案和源文档
    answer, source_docs = qa.run(
        query, custom_prompt=custom_prompt, return_source_documents=True)
    # print(source_docs)
    return answer
