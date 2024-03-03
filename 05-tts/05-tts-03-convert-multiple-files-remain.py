import os
from openai import OpenAI
from tqdm import tqdm
import time

def text_to_speech_for_folder(folder_path, voice):
    client = OpenAI()
    total_chars = 0
    files = os.listdir(folder_path)  # Liệt kê tất cả các file trong folder
    start_time = time.time()

    for file_name in tqdm(files, desc="Converting"):
        input_file = os.path.join(folder_path, file_name)  # Đường dẫn đầy đủ tới file input
        
        # Đọc nội dung từ file text với mã hóa UTF-8
        with open(input_file, 'r', encoding='utf-8') as file:
            input_text = file.read()
            total_chars += len(input_text)
        
        input_basename = file_name.split('.')[0]  # Lấy tên file không bao gồm phần mở rộng
        output_file = f"{input_basename}-{voice}.mp3"  # Tạo tên file output
        
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=input_text,
        )
        # Giả định phương thức `stream_to_file` tồn tại để lưu audio stream vào file
        response.stream_to_file(output_file)

    end_time = time.time()
    print(f"Total characters converted: {total_chars}")
    print(f"Total conversion time: {end_time - start_time:.2f} seconds")

# Đường dẫn tới folder chứa các file cần convert
folder_path = "book-remain"
# Chỉ sử dụng một giọng đọc là 'onyx'
text_to_speech_for_folder(folder_path, "onyx")
