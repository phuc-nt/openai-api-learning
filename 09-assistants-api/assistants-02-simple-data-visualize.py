from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

# Khởi tạo client API
client = OpenAI()

# Tải tệp .csv để sử dụng trong Assistant
file = client.files.create(
    file=open("data/tips.csv", "rb"),
    purpose='assistants'
)

# Tạo một Assistant mới với các cấu hình cụ thể
assistant = client.beta.assistants.create(
    name="Data visualizer",
    description="Bạn là chuyên gia tạo các trực quan hóa dữ liệu đẹp mắt. Bạn phân tích dữ liệu từ các tệp .csv, hiểu các xu hướng và tạo ra các trực quan hóa dữ liệu phù hợp với các xu hướng đó. Bạn cũng chia sẻ một bản tóm tắt ngắn gọn về các xu hướng quan sát được. Bạn luôn sử dụng tiếng Việt để trả lời.",
    model="gpt-4-turbo",
    tools=[{"type": "code_interpreter"}],
    tool_resources={
        "code_interpreter": {
            "file_ids": [file.id]
        }
    }
)

# Tạo một Thread mới để bắt đầu cuộc trò chuyện với Assistant
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "Hãy tạo 1 histogram mô tả phân phối của total bills",
            "attachments": [
                {
                    "file_id": file.id,
                    "tools": [{"type": "code_interpreter"}]
                }
            ]
        }
    ]
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

# Thực thi Run trên Thread với cấu hình mặc định của Assistant
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  event_handler=EventHandler(),
) as stream:
  stream.until_done() 