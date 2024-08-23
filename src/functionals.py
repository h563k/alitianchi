from typing import List
from transformers import BertTokenizer, BertModel
from langchain_core.embeddings import Embeddings
from src.promot import custom_prompt
from src.config import ModelConfig
import torch


# 自定义一个 RetrievalQA 类，以便能够获取检索到的文档
class CustomRetrievalQA:
    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, query, type, return_source_documents):
        # 初步处理
        search_query = custom_prompt(query, type)
        # 获取检索到的文档
        docs = ""
        # 获取检索到的文档
        docs_and_scores = self.retriever.similarity_search_with_score(
            search_query, k=3)
        for i, (doc, score) in enumerate(docs_and_scores):
            page_content = doc.page_content
            # 定制输出格式
            docs += f"## 参考资料{i+1}:\n" + page_content + "\n"

        # promot与原始查询合并
        query = f"""你是一个中医专家，请阅读如下资料:
{docs}


# 请参考上述格式，补齐以下内容，只允许使用中医和中医相关知识,不要出现西医相关内容。
{search_query}
        """
        if return_source_documents:
            print(query)
        return query


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
