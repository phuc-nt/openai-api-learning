from dotenv import load_dotenv
from openai import OpenAI

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Khởi tạo client OpenAI, sẽ tự động sử dụng OPENAI_API_KEY từ biến môi trường
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Bạn là 1 chuyên gia về ẩm thực Việt Nam, đầu bếp 40 năm kinh nghiệm."},
    {"role": "user", "content": "Hãy cho tôi công thức nấu món Phở"}
  ]
)

print(completion.choices[0].message.content)