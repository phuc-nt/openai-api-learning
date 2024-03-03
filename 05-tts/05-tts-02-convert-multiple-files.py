from openai import OpenAI
from tqdm import tqdm
import time

def text_to_speech_multiple_files(input_files, voice):
    client = OpenAI()
    total_chars = 0
    skipped_files = []
    start_time = time.time()

    for input_file in tqdm(input_files, desc="Converting"):
        # Đọc nội dung từ file text với mã hóa UTF-8
        with open(input_file, 'r', encoding='utf-8') as file:
            input_text = file.read()

        # Kiểm tra nếu số ký tự vượt quá 4000, bỏ qua file và thêm vào danh sách skipped_files
        if len(input_text) > 4000:
            skipped_files.append(input_file)
            continue  # Bỏ qua file này và chuyển sang file tiếp theo
        
        total_chars += len(input_text)
        input_basename = input_file.split('/')[-1].split('.')[0]  # Lấy tên file không bao gồm phần mở rộng
        output_file = f"{input_basename}-{voice}.mp3"

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
    
    # In ra tên các file đã bị bỏ qua do vượt quá giới hạn ký tự
    if skipped_files:
        print("Skipped files due to character limit:")
        for file in skipped_files:
            print(file)

# Tạo danh sách các file input
input_files = [f"book/hoang-tu-be-bui-giang-{str(i).zfill(2)}.txt" for i in range(1, 28)]

# Chỉ sử dụng một giọng đọc là 'onyx'
text_to_speech_multiple_files(input_files, "onyx")
