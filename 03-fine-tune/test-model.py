from dotenv import load_dotenv
from openai import OpenAI
import os

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Khởi tạo client OpenAI, sẽ tự động sử dụng OPENAI_API_KEY từ biến môi trường
client = OpenAI()

# Đọc content từ file "data/system.txt"
with open("data/system.txt", "r", encoding="utf-8") as file:
    system_content = file.read()

completion = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0613:phucorg::8xgFK0bk", 
  messages=[
    {"role": "system", "content": system_content},
    {"role": "user", "content": "Hãy làm cho tôi bài thơ lục bát 4 câu, chủ đề tôn vinh phụ nữ"}
  ]
)

print(completion.choices[0].message.content)
