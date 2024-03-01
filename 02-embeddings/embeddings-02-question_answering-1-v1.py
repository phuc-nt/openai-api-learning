import pandas as pd
from openai import OpenAI
import numpy as np
from scipy.spatial.distance import cosine
import json
import time

# Bắt đầu đo thời gian
start_time = time.time()

# Khởi tạo OpenAI client
client = OpenAI()

def safe_literal_eval(s):
    try:
        # Sử dụng json.loads để chuyển chuỗi thành list
        return json.loads(s.replace('\n', '').replace('array(', '[').replace(')', ']'))
    except json.JSONDecodeError:
        # Trả về list rỗng nếu có lỗi trong quá trình chuyển đổi
        return []

# Hàm tìm kiếm các đoạn văn bản liên quan nhất dựa trên embeddings
def strings_ranked_by_relatedness(query, df, relatedness_fn=lambda x, y: 1 - cosine(x, y), top_n=2):
    # Tạo embedding cho truy vấn
    response = client.embeddings.create(model="text-embedding-ada-002", input=query)
    query_embedding = response.data[0].embedding
    
    # Tính điểm liên quan giữa embedding truy vấn và embedding của mỗi dòng trong DataFrame
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for _, row in df.iterrows()
    ]
    
    # Sắp xếp các dòng theo điểm liên quan giảm dần và lấy top_n dòng
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    top_strings, top_relatednesses = zip(*strings_and_relatednesses[:top_n])
    
    return top_strings, top_relatednesses

# Đọc file CSV vào DataFrame
df = pd.read_csv("data/winter_olympics_2022.csv")

# Chuyển đổi chuỗi embeddings trong DataFrame thành list
df['embedding'] = df['embedding'].apply(safe_literal_eval)

# Chuyển đổi list thành numpy array để tiện cho việc tính toán sau này
df['embedding'] = df['embedding'].apply(lambda x: np.array(x))

# Query từ người dùng
user_query = "Which athletes won the medal in hockey at the 2022 Winter Olympics?"

# Tìm top 5 đoạn văn bản liên quan nhất
top_strings, top_relatednesses = strings_ranked_by_relatedness(user_query, df, top_n=5)

# Hiển thị kết quả
for string, relatedness in zip(top_strings, top_relatednesses):
    print(f"Điểm liên quan: {relatedness:.3f}")
    print(string)
    print("\n---\n")

# Kết thúc đo thời gian và in ra
old_version_time = time.time() - start_time
print(f"Thời gian thực thi phiên bản cũ: {old_version_time} giây.")