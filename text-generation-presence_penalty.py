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
    {"role": "system", "content": "Bạn là một nđầu bếp."},
    {"role": "user", "content": "Cho tôi biết nguyên liệu làm mỳ carbonara"},
]

# Yêu cầu với presence_penalty dương
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    presence_penalty=1.0,  # Khuyến khích các chủ đề mới
    max_tokens=300,
    stream=True,
)

# In kết quả
print("Encouraging New Topics:")
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")


# Yêu cầu với presence_penalty âm
negative_pp_stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    presence_penalty=-1.0,  # Khuyến khích lặp lại các chủ đề hoặc từ
    max_tokens=300,
    stream=True,
)

# In kết quả
print("\nEncouraging Repetition:")
for chunk in negative_pp_stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
