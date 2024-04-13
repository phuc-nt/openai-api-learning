from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Khởi tạo client Qdrant
        self.qdrant_client = QdrantClient(host="localhost", port=6333)
        # Khởi tạo mô hình Sentence Transformer
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, text: str):
        # Chuyển đổi truy vấn thành vector
        query_vector = self.encoder.encode(text).tolist()
        # Thực hiện truy vấn tìm kiếm với vector
        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=3  # Lấy ra 3 kết quả gần nhất
        )
        # Trích xuất payload từ các kết quả tìm kiếm
        results = [{
            'id': hit.id,
            'score': hit.score,
            'payload': hit.payload
        } for hit in search_results]
        return results