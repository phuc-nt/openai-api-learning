from qdrant_client import QdrantClient
import numpy as np
from openai import OpenAI

# Định nghĩa các hằng số
MODEL = "text-embedding-3-small"

# Khởi tạo client Qdrant
client = QdrantClient(host="localhost", port=6333)
collection_name = 'food_reviews'  # Tên của collection

# Tạo embedding cho một truy vấn sử dụng OpenAI API
def create_embedding(query, model=MODEL):
    openai_client = OpenAI()  # Khởi tạo client OpenAI
    response = openai_client.embeddings.create(model=model, input=query)
    return np.array(response.data[0].embedding)

# Tìm kiếm các vectors tương tự với truy vấn
def search_similar_vectors(query_vector, top_n=3):
    hits = client.search(
       collection_name=collection_name,
       query_vector=query_vector,
       limit=top_n  # Trả về top_n điểm gần nhất
    )
    # print(hits)  # In ra để kiểm tra cấu trúc
    return hits

# Truy vấn vector và thực hiện tìm kiếm
query = "bánh mì"
query_vector = create_embedding(query)
hits = search_similar_vectors(query_vector, top_n=3)

# In kết quả
print("Top 3 vectors tương tự cho truy vấn:", query)
for hit in hits:
    id = hit.id
    score = hit.score
    summary = hit.payload['Summary']
    text = hit.payload['Text']
    print(f"ID: {id}, Độ tương đồng: {score:.3f}")
    print(f"Summary: {summary}")
    print(f"Text: {text[:200]}...")  # In ra một phần của văn bản nếu nó quá dài
    print("-" * 80)  # Dùng để phân cách giữa các kết quả
