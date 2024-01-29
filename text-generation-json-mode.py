from dotenv import load_dotenv
from openai import OpenAI

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Khởi tạo client OpenAI, sẽ tự động sử dụng OPENAI_API_KEY từ biến môi trường
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
    {"role": "user", "content": "Cho tôi công thức nấu món Phở Bò Việt Nam"}
  ]
)
print(response.choices[0].message.content)