from openai import OpenAI
import os
from tqdm import tqdm
import csv

# Khởi tạo client API
client = OpenAI()

# Đường dẫn đến thư mục chứa các file PDF
folder_path = 'F:/phucnt/Workspace/rag-vietnam-literature-search/book3'
file_names = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

# Tên của Vector Store
vector_store_name = "Vietnamese Literature 20 books"

# Lấy hoặc tạo Vector Store với tên cụ thể
vector_stores = client.beta.vector_stores.list()
vector_store_id = None
for store in vector_stores.data:
    if store.name == vector_store_name:
        vector_store_id = store.id
        break

# Nếu không tìm thấy Vector Store, tạo mới
if vector_store_id is None:
    print(f"Không tìm thấy Vector Store có tên '{vector_store_name}', đang tạo mới...")
    vector_store = client.beta.vector_stores.create(name=vector_store_name)
    vector_store_id = vector_store.id
    print(f"Đã tạo Vector Store mới với ID: {vector_store_id}")

# Chuẩn bị và tải các file lên, lưu trữ ID và tên file
file_info_list = []
for file_name in tqdm(file_names, desc="Uploading files"):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'rb') as file_stream:
        file_response = client.files.create(file=file_stream, purpose='assistants')
        file_info_list.append((file_response.id, file_name))
        print(f"Uploaded {file_name} as {file_response.id}")

# Thêm file vào Vector Store và theo dõi trạng thái
for file_id, file_name in tqdm(file_info_list, desc="Processing files"):
    file_batch = client.beta.vector_stores.file_batches.create_and_poll(
        vector_store_id=vector_store_id,
        file_ids=[file_id]
    )
    print(f"Processing {file_name}: {file_batch.status}")
    if file_batch.status == 'completed':
        print(f"File {file_name} ({file_id}) added successfully.")
    else:
        print(f"Failed to process file {file_name} ({file_id}).")

# Lưu file_info_list vào file CSV mà không ghi đè dữ liệu cũ
csv_path = 'F:/phucnt/Workspace/openai-api-learning/vector-store-history/file_info_list.csv'
with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if os.stat(csv_path).st_size == 0:  # Kiểm tra xem file có rỗng không
        writer.writerow(['File ID', 'File Name'])  # Viết tiêu đề nếu file rỗng
    writer.writerows(file_info_list)
    print(f"File info list has been updated and saved to {csv_path}")

# Đóng các file nếu cần
