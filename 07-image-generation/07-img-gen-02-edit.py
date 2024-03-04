from openai import OpenAI
client = OpenAI()

response = client.images.edit(
  model="dall-e-2",
  image=open("image/image_edit_original.png", "rb"),
  mask=open("image/image_edit_mask.png", "rb"),
  prompt="A sunlit indoor lounge area with a pool containing a flamingo",
  n=1,
  size="1024x1024"
)
image_url = response.data[0].url
print(image_url)