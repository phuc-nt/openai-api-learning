import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

# Định nghĩa các hằng số
DATA_PATH = "data/AG_news_samples_with_embeddings.csv"
EMBEDDING_MODEL = "text-embedding-3-small"
K_NEAREST_NEIGHBORS = 2

# Đọc dữ liệu từ CSV đã có embeddings
df = pd.read_csv(DATA_PATH, converters={'embedding': pd.eval})

# Hàm để tính khoảng cách cosine và tìm k bản ghi gần nhất
def print_recommendations_from_embeddings(df, index_of_source_string, k_nearest_neighbors):
    # Lấy embedding của bản ghi nguồn
    query_embedding = np.array(df.iloc[index_of_source_string]['embedding'])

    # Tính khoảng cách giữa bản ghi nguồn và các bản ghi khác
    all_embeddings = np.stack(df['embedding'].values)
    distances = cdist([query_embedding], all_embeddings, 'cosine').flatten()

    # Lấy chỉ số của k bản ghi gần nhất (không tính bản ghi nguồn)
    nearest_indices = distances.argsort()[1:k_nearest_neighbors+1]

    # In bản ghi nguồn và k bản ghi gần nhất
    print(f"Source string: {df.iloc[index_of_source_string]['combined']}\n")
    for idx, nearest_idx in enumerate(nearest_indices, start=1):
        print(f"--- Recommendation #{idx} ---")
        print(f"String: {df.iloc[nearest_idx]['combined']}")
        print(f"Distance: {distances[nearest_idx]:0.3f}\n")

# Chạy hàm đề xuất cho 2 bản ghi mẫu
print("Articles similar to the random one:")
print_recommendations_from_embeddings(df, 10, K_NEAREST_NEIGHBORS)