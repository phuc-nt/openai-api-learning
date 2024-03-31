from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# Khởi tạo client Qdrant
client = QdrantClient(host="localhost", port=6333)

# Tên của collection mới
collection_name = 'food_reviews'

# Cấu hình vector cho collection
vectors_config = VectorParams(
    size=1536,  # Kích thước của vector embeddings từ "text-embedding-3-small"
    distance=Distance.COSINE  # Sử dụng khoảng cách Cosine
)

# Tạo collection mới
client.create_collection(
    collection_name=collection_name,
    vectors_config=vectors_config
)

print(f"Collection '{collection_name}' đã được tạo thành công.")
