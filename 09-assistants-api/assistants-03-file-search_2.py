from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

# Khởi tạo client API
client = OpenAI()

# Tên của Vector Store
vector_store_name = "Vietnamese Literature 20 books"

# Lấy ID của Vector Store có tên được chỉ định
vector_stores = client.beta.vector_stores.list()
vector_store_id = None
for store in vector_stores.data:
    if store.name == vector_store_name:
        vector_store_id = store.id
        break

if vector_store_id is None:
    print(f"Không tìm thấy Vector Store có tên '{vector_store_name}'")
else:
    print(f"Đã tìm thấy Vector Store '{vector_store_name}' với ID: {vector_store_id}")

    # Tạo một Assistant mới với File Search được kích hoạt và sử dụng Vector Store có sẵn
    assistant = client.beta.assistants.create(
        name="Literary Analyst Assistant",
        instructions="Bạn là chuyên gia phân tích văn học. Sử dụng cơ sở kiến thức của bạn để trả lời các câu hỏi về tác phẩm văn học Việt Nam.",
        model="gpt-4-turbo",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Liệt kê toàn bộ các cuốn sách trong dữ liệu của bạn"
            }
        ]
    )

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
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
