from openai import OpenAI
client = OpenAI()

# Đường dẫn tới file âm thanh của bạn
audio_file_path = "tts-output/hoang-tu-be-bui-giang-00-onyx.mp3"

# Đọc file âm thanh
with open(audio_file_path, "rb") as audio_file:
    # Sử dụng Whisper để chuyển đổi giọng nói thành văn bản
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

# Trích xuất văn bản từ kết quả transcription
transcribed_text = transcription.text

# Định nghĩa system_prompt
system_prompt = "Bạn là chuyện gia về tiếng Việt, hãy sửa lỗi chính tả nếu có của đoạn văn mà người dùng nhập vào"

# Sử dụng GPT-4 để chỉnh sửa bản ghi
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    temperature=0,
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": transcribed_text
        }
    ]
)

# In ra văn bản đã được chỉnh sửa
corrected_text = response.choices[0].message.content
print(corrected_text)
