import pandas as pd
import tiktoken
from tqdm import tqdm  # Import tqdm

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string using the specified encoding."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def estimate_cost(num_tokens: int, price_per_1k_tokens: float = 0.00002) -> float:
    """Estimates the cost for the given number of tokens."""
    return (num_tokens / 1000) * price_per_1k_tokens

# Đọc file CSV và kết hợp nội dung của cột "Summary" và "Text"
df = pd.read_csv('F:/phucnt/Workspace/data-sets/fine-food reviews/fine_food_reviews_1k.csv')  # Thay '/path/to/' bằng đường dẫn thực tế đến file của bạn
df['Combined'] = df['Summary'].fillna('') + ' ' + df['Text'].fillna('')  # Kết hợp nội dung và xử lý NaN

# Đếm số token và ước lượng chi phí cho mỗi dòng
total_tokens = 0
for combined_text in tqdm(df['Combined'], desc="Counting tokens"):  # Sử dụng tqdm để hiển thị thanh tiến trình
    num_tokens = num_tokens_from_string(combined_text, "cl100k_base")  # Sử dụng bộ mã hóa "cl100k_base"
    total_tokens += num_tokens

total_cost = estimate_cost(total_tokens)

print(f"Total number of tokens: {total_tokens}")
print(f"Estimated cost for embeddings API: ${total_cost:.5f}")
