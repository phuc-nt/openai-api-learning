import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models

# Load environment variables from .env file
load_dotenv()

# Retrieve the HF_TOKEN from .env file
HF_TOKEN = os.getenv("HF_TOKEN_READ")

# Đường dẫn đến file JSON chứa cấu trúc mã nguồn
file_path = "data/structured_code.jsonl"

# Khởi tạo client Qdrant
client = QdrantClient(host="localhost", port=6333)

# Khởi tạo các mô hình Sentence Transformers
nlp_model = SentenceTransformer("all-MiniLM-L6-v2")
code_model = SentenceTransformer(
    "jinaai/jina-embeddings-v2-base-code",
    token=HF_TOKEN,
    trust_remote_code=True
)

# Mã hóa truy vấn bằng text embeddings
query = "How do I count points in a collection?"
text_query_vector = nlp_model.encode(query).tolist()

# Tìm kiếm sử dụng text embeddings
text_hits = client.search(
    collection_name="code-sources",
    query_vector=("text", text_query_vector),
    limit=5,
)

# # Kiểm tra cấu trúc payload của hit đầu tiên
# if text_hits:
#     print("Payload structure of the first hit:", text_hits[0].payload)
# else:
#     print("No hits returned.")

# Mã hóa truy vấn bằng code embeddings
code_query_vector = code_model.encode(query).tolist()

# Tìm kiếm sử dụng code embeddings
code_hits = client.search(
    collection_name="code-sources",
    query_vector=("code", code_query_vector),
    limit=5,
)

# In kết quả từ text embeddings
print("Results from text embeddings:")
for hit in text_hits:
    context = hit.payload['context']
    print(f"Module: {context['module']}, File: {context['file_name']}, Score: {hit.score}, Signature: {hit.payload['signature']}")

# In kết quả từ code embeddings
print("\nResults from code embeddings:")
for hit in code_hits:
    context = hit.payload['context']
    print(f"Module: {context['module']}, File: {context['file_name']}, Score: {hit.score}, Signature: {hit.payload['signature']}")

# Kết hợp kết quả từ cả hai mô hình
combined_results = client.search_batch(
    collection_name="code-sources",
    requests=[
        models.SearchRequest(
            vector=models.NamedVector(
                name="text",
                vector=text_query_vector
            ),
            with_payload=True,
            limit=5,
        ),
        models.SearchRequest(
            vector=models.NamedVector(
                name="code",
                vector=code_query_vector
            ),
            with_payload=True,
            limit=5,
        ),
    ]
)

# In kết quả kết hợp
print("\nCombined results from both models:")
for result_set in combined_results:
    for hit in result_set:
        context = hit.payload['context']
        print(f"Module: {context['module']}, File: {context['file_name']}, Score: {hit.score}, Signature: {hit.payload['signature']}")
