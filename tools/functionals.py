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

    def run(self, query, custom_prompt=None, return_source_documents=False):
        # 如果有自定义提示，将其与原始查询合并
        if custom_prompt:
            query = f"{custom_prompt} {query}"

        # 获取检索到的文档
        docs_and_scores = self.retriever.get_relevant_documents(query)

        if return_source_documents:
            # 返回答案和源文档
            answer, source_docs = self.qa_chain.run(
                input_documents=docs_and_scores, question=query)

            # 定制输出格式
            print("Answer:", answer)
            print("\nSource Documents:")
            for doc in source_docs:
                print(f"Document: {doc.page_content}")
                print(f"Metadata: {doc.metadata}\n")

            return answer, docs_and_scores
        else:
            # 只返回答案
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
