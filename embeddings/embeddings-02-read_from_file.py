import pandas as pd
import numpy as np

# Đọc dữ liệu từ file CSV
df = pd.read_csv('data/output/rotten_tomatoes_critic_reviews-50-embedded.csv')

# Kiểm tra và chuyển đổi cột 'ada_embedding'
if 'ada_embedding' in df.columns:
    df['ada_embedding'] = df['ada_embedding'].apply(eval).apply(np.array)
else:
    print("Cột 'ada_embedding' không tồn tại trong DataFrame.")

# In thông tin cơ bản của DataFrame để kiểm tra
print("Thông tin cơ bản của DataFrame:")
print(f"Số dòng: {df.shape[0]}, Số cột: {df.shape[1]}")  # In số dòng và số cột
print("\nCác cột trong DataFrame:", df.columns.tolist())  # In tên các cột
print("\nMột số hàng đầu tiên của DataFrame:")
print(df.head())  # In ra 5 hàng đầu tiên của DataFrame để kiểm tra
