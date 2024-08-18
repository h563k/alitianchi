import os
import sys
from src.local_embedding import LocalEmbeddings

sys.path.append(os.path.abspath(__file__))

if __name__ == '__main__':
    embeddings = LocalEmbeddings()
    print(embeddings.embed_query('hello world'))
