from typing import List
from transformers import BertTokenizer, BertModel
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from src.config import ModelConfig
import torch


class LocalEmbeddings(Embeddings):
    def __init__(self):
        super().__init__()
        model_name = ModelConfig().embedding_path
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval()  # 确保模型处于评估模式

    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        # 将文档转换为嵌入向量
        texts = [doc.page_content for doc in documents]
        inputs = self.tokenizer(texts, padding=True,
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


if __name__ == '__main__':
    embeddings = LocalEmbeddings()
    print(embeddings.embed_query("你好,你是谁"))
