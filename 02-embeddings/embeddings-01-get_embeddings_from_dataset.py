import pandas as pd
from openai import OpenAI
from tqdm import tqdm
import tiktoken
import os

# Khởi tạo client OpenAI
client = OpenAI()

def get_embedding(text, model):
    text = str(text).replace("\n", " ")  # Đảm bảo text là chuỗi và loại bỏ xuống dòng
    response = client.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding
    tokens_used = response.usage.total_tokens
    return embedding, tokens_used

# Đường dẫn tới tập dữ liệu
input_datapath = "data/fine_food_reviews.csv"

# Tải và kiểm tra dữ liệu
df = pd.read_csv(input_datapath)
df = df[["ProductId", "UserId", "Score", "Summary", "Text", "Time"]]
df = df.dropna()
df["combined"] = "Title: " + df.Summary.str.strip() + "; Content: " + df.Text.str.strip()

# Chọn 1000 bản ghi mới nhất sau khi lọc bớt bản ghi dài
top_n = 1000
df = df.sort_values("Time").tail(top_n * 2)  # Chọn 2000 bản ghi mới nhất để dự phòng
df.drop("Time", axis=1, inplace=True)  # Xóa cột "Time" không cần thiết sau khi sắp xếp

# Giới hạn token cho mỗi đánh giá
embedding_model = "text-embedding-3-small"
embedding_encoding = "cl100k_base"
max_tokens = 8000

# Lấy mã hóa và đếm token với tiến trình được hiển thị bởi tqdm
encoding = tiktoken.get_encoding(embedding_encoding)
df["n_tokens"] = [len(encoding.encode(text)) for text in tqdm(df["combined"], desc="Đếm token")]

# Lọc các đánh giá dài vượt quá giới hạn token
df = df[df.n_tokens <= max_tokens].tail(top_n)

# Đặt số lượng bản ghi xử lý trước khi lưu
batch_size = 50

# Đường dẫn lưu file kết quả
output_datapath = "data/fine_food_reviews_with_embeddings.csv"

# Xóa file kết quả nếu đã tồn tại để bắt đầu mới
if os.path.exists(output_datapath):
    os.remove(output_datapath)

# Lặp qua DataFrame và xử lý từng batch
for start_idx in tqdm(range(0, len(df), batch_size), desc="Xử lý batches"):
    end_idx = start_idx + batch_size
    batch_df = df.iloc[start_idx:end_idx].copy()
    
    embeddings = []
    tokens_used_list = []
    
    # Lấy embeddings cho batch hiện tại
    for _, row in batch_df.iterrows():
        embedding, tokens_used = get_embedding(row["combined"], model=embedding_model)
        embeddings.append(embedding)
        tokens_used_list.append(tokens_used)
    
    batch_df["embedding"] = embeddings
    batch_df["tokens_used"] = tokens_used_list
    
    # Lưu kết quả của batch hiện tại vào file, sử dụng mode 'a' để thêm vào file
    batch_df.to_csv(output_datapath, mode='a', header=not os.path.exists(output_datapath), index=False)

print("Embeddings và số token đã được lưu vào:", output_datapath)
