from dotenv import load_dotenv
import openai
import os

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Khởi tạo API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo client OpenAI
client = openai.OpenAI()

# Định nghĩa tin nhắn đầu vào
messages = [
    {"role": "system", "content": "Hãy liệt kê các loại trái cây."},
    {"role": "user", "content": "Hãy kể cho tôi một số loại trái cây."}
]

# Yêu cầu với frequency_penalty dương
positive_fp_stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    frequency_penalty=1.0,  # Giá trị dương để giảm thiểu sự lặp lại
    stream=True,
)

print("Positive frequency_penalty (Avoiding Repetition):")
for chunk in positive_fp_stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

# Yêu cầu với frequency_penalty âm
negative_fp_stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    frequency_penalty=-1.0,  # Giá trị âm để khuyến khích sự lặp lại
    stream=True,
)

print("\n\nNegative frequency_penalty (Encouraging Repetition):")
for chunk in negative_fp_stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
