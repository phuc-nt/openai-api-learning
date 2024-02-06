import pandas as pd
import numpy as np

def analyze_csv(file_path):
    try:
        # Đọc tệp CSV
        data = pd.read_csv(file_path)

        # Đếm số bản ghi
        num_records = data.shape[0]

        # Lấy thông tin về tên và kiểu dữ liệu của mỗi cột
        columns_info = data.dtypes

        # Trích xuất 20 bản ghi ngẫu nhiên (hoặc ít hơn nếu tổng số bản ghi ít hơn 20)
        random_records = data.sample(n=min(20, num_records), random_state=np.random.RandomState())

        return num_records, columns_info, random_records
    except Exception as e:
        return str(e), None, None

# Thay thế 'your_file_path.csv' với đường dẫn tệp CSV của bạn
file_path = 'rotten-critic-10_records.csv'
num_records, columns_info, random_records = analyze_csv(file_path)

print("Số lượng bản ghi:", num_records)
print("Thông tin các cột:")
print(columns_info)
print("20 bản ghi ngẫu nhiên:")
print(random_records)
