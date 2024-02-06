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

# Yêu cầu với temperature cao
high_temperature_stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.9,  # Tạo ra đầu ra ngẫu nhiên hơn
    max_tokens=100,
    stream=True,
)

print("High temperature (More Random):")
for chunk in high_temperature_stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

# Yêu cầu với temperature thấp
low_temperature_stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.1,  # Tạo ra đầu ra ít ngẫu nhiên hơn
    max_tokens=100,
    stream=True,
)

print("\nLow temperature (Less Random):")
for chunk in low_temperature_stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
