import pandas as pd
from openai import OpenAI
from tqdm import tqdm
import tiktoken
import os

# Định nghĩa các hằng số
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_ENCODING = "cl100k_base"
MAX_TOKENS = 8000
BATCH_SIZE = 50
INPUT_DATAPATH = "data/AG_news_samples.csv"
OUTPUT_DATAPATH = "data/AG_news_samples_with_embeddings.csv"

# Khởi tạo client OpenAI
client = OpenAI()

def get_embedding(text, model):
    text = str(text).replace("\n", " ")  # Đảm bảo text là chuỗi và loại bỏ xuống dòng
    response = client.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding
    tokens_used = response.usage.total_tokens
    return embedding, tokens_used

# Tải và kiểm tra dữ liệu
df = pd.read_csv(INPUT_DATAPATH)
df = df[["label_int", "title", "description", "label"]]
df["combined"] = "Label: " + df.label.astype(str) + "; Title: " + df.title.str.strip() + "; Description: " + df.description.str.strip()

# Giới hạn token cho mỗi đánh giá
encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)
df["n_tokens"] = [len(encoding.encode(text)) for text in tqdm(df["combined"], desc="Đếm token")]

# Lọc các đánh giá dài vượt quá giới hạn token
df = df[df.n_tokens <= MAX_TOKENS]

# Xóa file kết quả nếu đã tồn tại để bắt đầu mới
if os.path.exists(OUTPUT_DATAPATH):
    os.remove(OUTPUT_DATAPATH)

# Lặp qua DataFrame và xử lý từng batch
for start_idx in tqdm(range(0, len(df), BATCH_SIZE), desc="Xử lý batches"):
    end_idx = start_idx + BATCH_SIZE
    batch_df = df.iloc[start_idx:end_idx].copy()
    
    embeddings = []
    tokens_used_list = []
    
    # Lấy embeddings cho batch hiện tại
    for _, row in batch_df.iterrows():
        embedding, tokens_used = get_embedding(row["combined"], model=EMBEDDING_MODEL)
        embeddings.append(embedding)
        tokens_used_list.append(tokens_used)
    
    batch_df["embedding"] = embeddings
    batch_df["tokens_used"] = tokens_used_list
    
    # Lưu kết quả của batch hiện tại vào file, sử dụng mode 'a' để thêm vào file
    batch_df.to_csv(OUTPUT_DATAPATH, mode='a', header=not os.path.exists(OUTPUT_DATAPATH), index=False)

print("Embeddings và số token đã được lưu vào:", OUTPUT_DATAPATH)
