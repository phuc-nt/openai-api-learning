import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from tqdm import tqdm

# Giả định DATA_DIR là thư mục hiện tại
DATA_DIR = '.'
# Không sử dụng API key trong môi trường development
QDRANT_API_KEY = None
# Tên của collection
COLLECTION_NAME = 'startups'
# Tên trường văn bản
TEXT_FIELD_NAME = 'description'

# Tên mô hình vector hóa
EMBEDDINGS_MODEL = 'all-MiniLM-L6-v2'

def upload_embeddings():
    # Khởi tạo SentenceTransformer với mô hình all-MiniLM-L6-v2
    model = SentenceTransformer(EMBEDDINGS_MODEL)

    # Khởi tạo Qdrant client
    client = QdrantClient(host="localhost", port=6333)

    payload_path = os.path.join(DATA_DIR, 'data/startups_demo.json')
    payload = []
    documents = []

    # Đọc và xử lý dữ liệu từ file JSON
    with open(payload_path, 'r') as fd:
        for line in fd:
            obj = json.loads(line)
            documents.append(obj[TEXT_FIELD_NAME])  # Lưu trữ mô tả để vector hóa
            # Thêm vào payload với các trường đã chỉnh sửa (nếu cần)
            payload.append(obj)

    # Mã hóa các mô tả thành vector
    vectors = model.encode(documents, show_progress_bar=True).tolist()

    # Tạo collection mới hoặc tái tạo collection cũ nếu nó đã tồn tại
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=model.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )

    # Tải dữ liệu lên Qdrant
    for i in tqdm(range(len(payload))):
        client.upload_points(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=i,
                    vector=vectors[i],
                    payload=payload[i]
                )
            ]
        )

if __name__ == '__main__':
    upload_embeddings()
