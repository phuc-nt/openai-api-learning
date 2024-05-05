from openai import OpenAI

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
    # Lấy và in danh sách các file trong Vector Store
    files = client.beta.vector_stores.files.list(vector_store_id=vector_store_id)
    total_usage_bytes = 0
    file_count = 0  # Biến để đếm số lượng file
    if files.data:
        print(f"Danh sách các file trong Vector Store '{vector_store_name}':")
        for file in files.data:
            print(f"ID file: {file.id}, Trạng thái: {file.status}, Dung lượng sử dụng: {file.usage_bytes} bytes")
            total_usage_bytes += file.usage_bytes
            file_count += 1  # Tăng biến đếm file
        max_bytes = 1 * 1024 * 1024 * 1024  # 1GB converted to bytes
        usage_percent = (total_usage_bytes / max_bytes) * 100
        print(f"Tổng số file: {file_count}")
        print(f"Tổng dung lượng sử dụng: {total_usage_bytes} bytes ({usage_percent:.2f}% của 1GB)")
    else:
        print("Không có file nào trong Vector Store này.")

# # Xoá store        
# deleted_vector_store = client.beta.vector_stores.delete(
#   vector_store_id=vector_store_id
# )
# print(deleted_vector_store)