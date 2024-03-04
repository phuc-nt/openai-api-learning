from openai import OpenAI
client = OpenAI()

response = client.images.create_variation(
  image=open("image/image_edit_original.png", "rb"),
  n=2,
  size="1024x1024"
)

image_url = response.data[0].url
print(image_url)