import json

def process_poem(input_file_path, system_file_path, output_file_path):
    # Đọc nội dung file system
    with open(system_file_path, 'r', encoding='utf-8') as sys_file:
        system_content = sys_file.read().strip()
    
    # Đọc và xử lý file kieu
    with open(input_file_path, 'r', encoding='utf-8') as poem_file:
        lines = poem_file.readlines()
    
    # Chuẩn bị dữ liệu cho fine-tuning
    examples = []
    poem_segment = []
    for line in lines:
        # Xóa số đầu câu nếu có
        line = line.split('. ', 1)[-1].strip()
        if line:  # Kiểm tra xem dòng không phải là dòng trống
            poem_segment.append(line)
            if len(poem_segment) == 4:  # Đủ 4 câu thơ
                examples.append({
                    "messages": [
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": "Hãy làm cho tôi bài thơ lục bát ..."},
                        {"role": "assistant", "content": "\n".join(poem_segment)}
                    ]
                })
                poem_segment = []  # Đặt lại cho đoạn thơ tiếp theo
    
    # Ghi ra file jsonl
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        for example in examples:
            out_file.write(json.dumps(example, ensure_ascii=False) + '\n')

# Cấu hình đường dẫn
input_file_path = 'data/kieu.txt'
system_file_path = 'data/system.txt'
output_file_path = 'train-data/fine_tuning_data.jsonl'

# Thực thi hàm
process_poem(input_file_path, system_file_path, output_file_path)
