import tiktoken

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
  """Trả về số lượng token được sử dụng bởi một danh sách tin nhắn."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0613":  # lưu ý: các mô hình tương lai có thể khác biệt
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # mỗi tin nhắn tuân theo <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # nếu có tên, vai trò sẽ được bỏ qua
                  num_tokens += -1  # vai trò luôn được yêu cầu và luôn là 1 token
      num_tokens += 2  # mỗi phản hồi được khởi đầu bằng <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() hiện không được thực hiện cho mô hình {model}.
  Xem https://github.com/openai/openai-python/blob/main/chatml.md để biết thông tin về cách tin nhắn được chuyển đổi thành token.""")

messages = [
    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
    {"role": "user", "content": "Thủ đô của Việt Nam là"}
]

model = "gpt-3.5-turbo-0613"

print(f"{num_tokens_from_messages(messages, model)} prompt tokens counted.")
# Nên hiển thị ~126 total_tokens

# ví dụ về số lượng token từ OpenAI API
from dotenv import load_dotenv
from openai import OpenAI

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Khởi tạo client OpenAI, sẽ tự động sử dụng OPENAI_API_KEY từ biến môi trường
client = OpenAI()

response = client.chat.completions.create(
  model=model,
  messages=messages,
  temperature=0,
)

print(f'{response.usage.prompt_tokens} prompt tokens used.')
