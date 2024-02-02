from dotenv import load_dotenv
import openai
import os

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Khởi tạo API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo client OpenAI
client = openai.OpenAI()

# Tạo một yêu cầu chat completion với streaming
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Bạn là trợ lý ảo."},
        {"role": "user", "content": "Tôi cần một danh sách việc cần làm cho ngày mai."},
        {"role": "assistant", "content": "Tôi sẽ giúp bạn lập danh sách. Bạn cần làm gì vào ngày mai?", "name": "Tro_ly_1"}
    ],
    stream=True
)

for chunk in stream:
    # Kiểm tra và in nội dung của phản hồi nếu tồn tại
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
