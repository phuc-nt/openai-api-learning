from dotenv import load_dotenv
from openai import OpenAI

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Khởi tạo client OpenAI, sẽ tự động sử dụng OPENAI_API_KEY từ biến môi trường
client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Bạn là 1 chuyên gia về ẩm thực Việt Nam, đầu bếp 40 năm kinh nghiệm."},
        {"role": "user", "content": "Hãy cho tôi công thức nấu món Phở"}
    ],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
