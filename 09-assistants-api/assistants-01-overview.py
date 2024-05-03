from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

client = OpenAI()

# Tạo một Assistant với chỉ thị bằng tiếng Việt
assistant = client.beta.assistants.create(
  name="Giáo viên Toán",
  instructions="Bạn là một giáo viên toán cá nhân. Viết và chạy code để trả lời các câu hỏi về toán.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4-turbo",
)

# Tạo một Thread cho cuộc trò chuyện
thread = client.beta.threads.create()

# Thêm một Message vào Thread với nội dung bằng tiếng Việt
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="Tôi cần giải phương trình `3x + 11 = 14`. Bạn có thể giúp tôi không?"
)

# Định nghĩa một lớp xử lý sự kiện
class EventHandler(AssistantEventHandler):
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)  # Bắt đầu in phản hồi từ trợ lý

  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)  # In ra phần văn bản được thêm vào từ trợ lý
  
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)  # In ra thông báo khi một công cụ được gọi
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)  # In ra mã đầu vào cho bộ giải thích mã
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)  # In ra kết quả thực thi mã
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)  # In ra các log từ việc thực thi mã

# Sử dụng SDK để tạo và stream phản hồi
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Vui lòng xưng hô người dùng là Phúc Đẹp Trai. Người dùng có tài khoản cao cấp.",
  event_handler=EventHandler(),
) as stream:
  stream.until_done()  # Duy trì stream cho đến khi hoàn tất
