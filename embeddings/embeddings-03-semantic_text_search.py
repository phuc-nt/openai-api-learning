import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from ast import literal_eval
from openai import OpenAI

# Định nghĩa các hằng số
DATAFILE_PATH = "data/fine_food_reviews_with_embeddings.csv"
MODEL = "text-embedding-3-small"

# Chuyển đổi chuỗi thành numpy array một cách an toàn
def safe_literal_eval(s):
    try:
        return np.array(literal_eval(s))
    except ValueError:
        return np.zeros(0)

# Tạo embedding cho một truy vấn sử dụng OpenAI API
def create_embedding(query, model=MODEL):
    client = OpenAI()  # Khởi tạo client OpenAI
    response = client.embeddings.create(model=model, input=query)
    return np.array(response.data[0].embedding)

# Tìm kiếm các đánh giá có độ tương đồng cao nhất với truy vấn
def search_reviews(query, df, top_n=3):
    query_embedding = create_embedding(query)
    embeddings = np.vstack(df['embedding'].values)
    distances = cdist([query_embedding], embeddings, 'cosine')[0]
    top_indices = distances.argsort()[:top_n]

    # Tạo một cột mới 'combined' trước khi áp dụng lọc
    df['combined'] = 'Title: ' + df['Summary'] + '; Content: ' + df['Text']
    
    # Lấy kết quả dựa trên top_indices
    results = (
        df.loc[top_indices, 'combined']
        .str.replace("Title: ", "")
        .str.replace("; Content:", ": ")
    )

    # Hiển thị kết quả
    # for result in results:
    #     print(result[:200])
    #     print()

    # Trả về kết quả và độ tương đồng
    return results.values, 1 - distances[top_indices]

# Đọc dữ liệu và chuẩn bị embeddings
df = pd.read_csv(DATAFILE_PATH)
df["embedding"] = df.embedding.apply(safe_literal_eval)

# Thực hiện tìm kiếm với một truy vấn cụ thể
query = "bánh mì"
results, similarities = search_reviews(query, df, top_n=3)

# In kết quả
print("Top 3 đánh giá liên quan đến:", query)
for result, similarity in zip(results, similarities):
    print(f"Độ tương đồng: {similarity:.3f}, Đánh giá: {result[:200]}\n")
