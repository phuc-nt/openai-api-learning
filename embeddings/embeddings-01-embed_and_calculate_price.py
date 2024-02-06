import pandas as pd
from openai import OpenAI
from tqdm import tqdm  # Import tqdm

# Khởi tạo client OpenAI
client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
    text = str(text).replace("\n", " ")  # Đảm bảo text là chuỗi và loại bỏ xuống dòng
    response = client.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding
    tokens_used = response.usage.total_tokens
    return embedding, tokens_used

# Đọc dữ liệu từ file CSV
df = pd.read_csv('F:/phucnt/Workspace/openai-api-learning/data/rotten_tomatoes_critic_reviews-50.csv')

# Kết hợp cột 'review_type' và 'review_content' thành cột 'combined'
df['combined'] = df['review_type'].astype(str) + " " + df['review_content'].astype(str)

total_tokens_used = 0

def apply_and_track_tokens(row):
    global total_tokens_used
    embedding, tokens_used = get_embedding(row, model='text-embedding-3-small')
    total_tokens_used += tokens_used
    return embedding

# Sử dụng tqdm để bọc lấy df['combined'].apply(...) để theo dõi tiến trình
tqdm.pandas(desc="Processing records")
df['ada_embedding'] = df['combined'].progress_apply(apply_and_track_tokens)

# In thông tin chi phí sau khi hoàn thành
gia_moi_1000_token = 0.00002
chi_phi = (total_tokens_used / 1000) * gia_moi_1000_token
print(f"Tổng số token đã sử dụng: {total_tokens_used}")
print(f"Chi phí ước lượng: ${chi_phi:.10f}")

# Lưu kết quả vào file CSV mới
df.to_csv('data/output/rotten_tomatoes_critic_reviews-50-embedded.csv', index=False)
