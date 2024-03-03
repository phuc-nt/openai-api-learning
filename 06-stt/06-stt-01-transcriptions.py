from openai import OpenAI
client = OpenAI()

audio_file = open("tts-output/hoang-tu-be-bui-giang-00-onyx.mp3", "rb")
transcript = client.audio.transcriptions.create(
  file=audio_file,
  model="whisper-1",
  prompt="dịch giả Bùi Giáng, nhà xuất bản An Tiêm, năm xuất bản 1973"
)

print(transcript.text)