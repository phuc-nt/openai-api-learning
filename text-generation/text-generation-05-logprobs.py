from dotenv import load_dotenv
from openai import OpenAI
import pprint


# Tải các biến môi trường từ tệp .env
load_dotenv()

# Khởi tạo client OpenAI, sẽ tự động sử dụng OPENAI_API_KEY từ biến môi trường
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hãy in ra: Hello Phuc"}
    ],
    logprobs=True,
    top_logprobs=5
)

print(completion.choices[0].message.content)

# Chuyển đổi dữ liệu logprobs thành một cấu trúc dễ đọc hơn
logprobs = []
for token_logprob in completion.choices[0].logprobs.content:
    logprobs.append({
        "token": token_logprob.token,
        "logprob": token_logprob.logprob,
        "top_logprobs": [{tp.token: tp.logprob for tp in token_logprob.top_logprobs}]
    })

# Sử dụng pprint để in dữ liệu
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(logprobs)