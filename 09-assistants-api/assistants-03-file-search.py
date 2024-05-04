from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

# Khởi tạo client API
client = OpenAI()

# Tạo một Assistant mới với File Search được kích hoạt
assistant = client.beta.assistants.create(
    name="Literary Analyst Assistant",
    instructions="Bạn là chuyên gia phân tích văn học. Sử dụng cơ sở kiến thức của bạn để trả lời các câu hỏi về tác phẩm văn học Việt Nam.",
    model="gpt-4-turbo",
    tools=[{"type": "file_search"}],
)

# Tạo Vector Store để chứa các tệp
vector_store = client.beta.vector_stores.create(name="Vietnamese Literature")

# Chuẩn bị tệp để tải lên OpenAI
file_path = "data/Soi Toc - Thach Lam.pdf"
file_stream = open(file_path, "rb")

# Tải tệp lên, thêm vào Vector Store, và theo dõi trạng thái của lô tệp
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=[file_stream]
)

print(f"Trạng thái lô tệp: {file_batch.status}")
print(f"Số lượng tệp: {file_batch.file_counts}")

# Cập nhật Assistant để sử dụng Vector Store mới
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

# Tạo một Thread và đính kèm tệp
message_file = client.files.create(
    file=open("data/Lanh Lung - Nhat Linh.pdf", "rb"), purpose="assistants"
)

thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "Tác phẩm 'Sợi Tóc' nói về điều gì?",
            "attachments": [
                {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
            ],
        }
    ]
)

print(f"Nguồn tệp trong Thread: {thread.tool_resources.file_search}")

# Định nghĩa một lớp xử lý sự kiện
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\ntrợ lý > ", end="")

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\ntrợ lý > {tool_call.type}\n")

    @override
    def on_message_done(self, message) -> None:
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))

# Thực thi Run trên Thread với EventHandler
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Xin hãy xưng hô người dùng là Trọng Phúc. Người dùng có tài khoản cao cấp.",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()
