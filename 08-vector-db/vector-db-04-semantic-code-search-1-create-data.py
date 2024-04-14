import json
import os
import uuid
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
import inflection
import re
from typing import Dict, Any
from tqdm import tqdm

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy token từ biến môi trường
HF_TOKEN = os.getenv("HF_TOKEN_READ")

# Đường dẫn tới file JSON chứa cấu trúc mã nguồn
file_path = "data/structured_code_short.jsonl"

# Khởi tạo client Qdrant
client = QdrantClient(host="localhost", port=6333)

# Đọc dữ liệu từ file JSON
structures = []
with open(file_path, "r", encoding='utf-8') as fp:
    for row in tqdm(fp, desc="Đọc file JSON"):
        entry = json.loads(row)
        structures.append(entry)

# Hàm chuyển đổi mã thành văn bản tự nhiên
def textify(chunk: Dict[str, Any]) -> str:
    name = inflection.humanize(inflection.underscore(chunk["name"]))
    signature = inflection.humanize(inflection.underscore(chunk["signature"]))
    docstring = f"that does {chunk['docstring']}" if chunk.get("docstring") else ""
    context = f"module {chunk['context']['module']} file {chunk['context']['file_name']}"
    if chunk["context"].get("struct_name"):
        struct_name = inflection.humanize(inflection.underscore(chunk["context"]["struct_name"]))
        context = f"được định nghĩa trong struct {struct_name} {context}"
    text_representation = f"{chunk['code_type']} {name} {docstring} được định nghĩa là {signature} {context}"
    tokens = re.split(r"\W+", text_representation)
    return " ".join(filter(None, tokens))

# Chuyển đổi tất cả các chunks thành biểu diễn văn bản
text_representations = list(map(textify, tqdm(structures, desc="Chuyển đổi mã thành văn bản")))

# Mã hóa các biểu diễn văn bản
nlp_model = SentenceTransformer("all-MiniLM-L6-v2")
nlp_embeddings = nlp_model.encode(text_representations, show_progress_bar=True)

# Mã hóa mã nguồn
code_snippets = [entry["context"]["snippet"] for entry in structures]
code_model = SentenceTransformer("jinaai/jina-embeddings-v2-base-code", token=HF_TOKEN, trust_remote_code=True)
code_model.max_seq_length = 8192
code_embeddings = code_model.encode(code_snippets, batch_size=4, show_progress_bar=True)

# Tạo bộ sưu tập Qdrant mới để lưu trữ các embeddings
client.create_collection(
    "code-sources",
    vectors_config={
        "text": models.VectorParams(size=nlp_embeddings.shape[1], distance=models.Distance.COSINE),
        "code": models.VectorParams(size=code_embeddings.shape[1], distance=models.Distance.COSINE),
    }
)

# Tải các embeddings lên Qdrant
points = [
    models.PointStruct(
        id=str(uuid.uuid4()),
        vector={"text": text_embedding.tolist(), "code": code_embedding.tolist()},
        payload=entry
    )
    for text_embedding, code_embedding, entry in tqdm(zip(nlp_embeddings, code_embeddings, structures), desc="Tải dữ liệu lên Qdrant")
]
client.upload_points("code-sources", points=points, batch_size=64)

# Các điểm dữ liệu hiện có sẵn cho việc tìm kiếm
print("Dữ liệu đã được tải lên Qdrant và sẵn sàng cho việc tìm kiếm.")
