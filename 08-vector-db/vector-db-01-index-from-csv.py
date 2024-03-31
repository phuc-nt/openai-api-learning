from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import pandas as pd
from tqdm import tqdm  # Import tqdm
import json
import uuid

# Đọc dữ liệu từ CSV
file_path = 'data/fine_food_reviews_with_embeddings.csv'
df = pd.read_csv(file_path)

# Chuyển đổi cột 'embedding' từ chuỗi sang danh sách các số
df['embedding'] = df['embedding'].apply(lambda x: json.loads(x))

# Khởi tạo client Qdrant
client = QdrantClient(host="localhost", port=6333)

# Tên của collection
collection_name = 'food_reviews'

# Hàm để index dữ liệu sử dụng qdrant_client
def index_data(row):
    point = PointStruct(
        id=str(uuid.uuid4()),  # Tạo ID dạng UUID
        payload={
            'Score': row['Score'],
            'Summary': row['Summary'],
            'Text': row['Text']
        },
        vector=row['embedding']
    )
    operation_info = client.upsert(
        collection_name=collection_name,
        wait=True,
        points=[point]
    )
    return operation_info

# Sử dụng tqdm trong vòng lặp để hiển thị tiến trình
responses = [index_data(row) for _, row in tqdm(df.iterrows(), total=df.shape[0])]

# In ra một số thông tin phản hồi để kiểm tra
for response in responses[:5]:
    print(response)