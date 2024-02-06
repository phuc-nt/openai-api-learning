from dotenv import load_dotenv
import openai
import os

# Tải các biến môi trường
load_dotenv()

# Khởi tạo client OpenAI với API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

# Định nghĩa tin nhắn đầu vào
messages = [
    {"role": "user", "content": "Lionel Messi là"},
]

# Yêu cầu với top_p cao
high_top_p_stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    top_p=0.9,  # Cho phép đa dạng hóa nhiều lựa chọn token
    max_tokens=100,
    stream=True,
)

print("High top_p (More Diverse):")
for chunk in high_top_p_stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

# Yêu cầu với top_p thấp
low_top_p_stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    top_p=0.1,  # Hạn chế lựa chọn token, tạo ra đầu ra ít đa dạng hơn
    max_tokens=100,
    stream=True,
)

print("\nLow top_p (Less Diverse):")
for chunk in low_top_p_stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")