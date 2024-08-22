from typing import List
from transformers import BertTokenizer, BertModel
from langchain_core.embeddings import Embeddings
from src.config import ModelConfig
import torch


# 自定义一个 RetrievalQA 类，以便能够获取检索到的文档
class CustomRetrievalQA:
    def __init__(self, retriever, qa_chain):
        self.retriever = retriever
        self.qa_chain = qa_chain

    def run(self, query, type, custom_prompt):
        # promot与原始查询合并
        query = custom_prompt(query, type)
        print(query)

        # 获取检索到的文档
        docs_and_scores = self.retriever.similarity_search(
            query, search_kwargs={"k": 3})

        # 返回匹配结果 只推送第一个
        for doc in docs_and_scores:
            print(f"Document: {doc.page_content}")
            print(f"Metadata: {doc.metadata}\n")

        answer = self.qa_chain.run(
            input_documents=docs_and_scores, question=query)
        return answer


class LocalEmbeddings(Embeddings):
    def __init__(self):
        super().__init__()
        model_name = ModelConfig().embedding_path
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval()  # 确保模型处于评估模式

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        inputs = self.tokenizer(documents, padding=True,
                                truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        return embeddings

    def embed_query(self, query: str) -> List[float]:
        # 为单个查询生成嵌入
        inputs = self.tokenizer(query, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        return embeddings
