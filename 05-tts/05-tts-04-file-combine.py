from pydub import AudioSegment
import os

def merge_mp3_files(folder_path, output_file):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.mp3')])
    combined = AudioSegment.empty()

    for file_name in files:
        path = os.path.join(folder_path, file_name)
        audio = AudioSegment.from_mp3(path)
        combined += audio

    combined.export(output_file, format="mp3")

# Đường dẫn tới folder chứa các file mp3
folder_path = "hoang-tu-be-mp3"
# Đường dẫn file mp3 kết quả sau khi ghép
output_file = "hoang-tu-be-combined.mp3"

merge_mp3_files(folder_path, output_file)
