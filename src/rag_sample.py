import yaml
from langchain.document_loaders import JSONLoader
from langchain.vectorstores import FAISS
from openai import OpenAI
from src.local_embedding import LocalEmbeddings


def promot_read():
    with open('scripts/prompt_settings.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data['medical_zh']['default']


def get_response(prompt, question):
    client = OpenAI(base_url="http://127.0.0.1:8000/v1",
                    api_key="0")
    response = client.chat.completions.create(
        model="baichuan-chat-7b",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
    )
    return response.choices[0].message.content


def rag_miedical():
    # 步骤1: 加载 JSON 数据
    json_file_path = 'data/train.json'
    loader = JSONLoader(file_path=json_file_path,
                        jq_schema='.', text_content=False)  # 确保 jq_schema 参数被传递
    documents = loader.load()

    # 步骤3: 生成嵌入
    embeddings = LocalEmbeddings()


if __name__ == '__main__':
    rag_miedical()
