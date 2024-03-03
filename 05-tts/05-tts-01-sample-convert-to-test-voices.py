from openai import OpenAI
from tqdm import tqdm

def text_to_speech(input_file, voices):
    # Đọc nội dung từ file text với mã hóa UTF-8
    with open(input_file, 'r', encoding='utf-8') as file:
        input_text = file.read()

    client = OpenAI()
    
    # Tạo tên file output dựa trên tên file input và giọng đọc
    input_basename = input_file.split('/')[-1].split('.')[0]  # Lấy tên file không bao gồm phần mở rộng
    output_files = [f"{input_basename}-{voice}.mp3" for voice in voices]

    # Tạo speech output cho mỗi giọng và lưu vào file tương ứng
    for voice, output_file in tqdm(zip(voices, output_files), total=len(voices), desc="Processing"):
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=input_text,
        )
        # Giả sử `stream_to_file` là phương thức hợp lệ để lưu audio stream vào file
        # Vì không thể thực thi trong môi trường này, giả định phương thức này tồn tại
        response.stream_to_file(output_file)

# Danh sách giọng đọc
voices = ["alloy", "nova", "shimmer"]

# Gọi hàm và truyền vào file input và danh sách giọng
text_to_speech("book/hoang-tu-be-bui-giang-00.txt", voices)
