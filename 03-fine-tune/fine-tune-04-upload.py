from openai import OpenAI
client = OpenAI()

# Tạo file và gán kết quả trả về cho biến
response = client.files.create(
  file=open("train-data/fine_tuning_data.jsonl", "rb"),
  purpose="fine-tune"
)

# In ra file ID
print(response.id)