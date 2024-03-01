from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Có gì trong hình?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Steve_Jobs_and_Macintosh_computer%2C_January_1984%2C_by_Bernard_Gotfryd_-_edited.jpg/800px-Steve_Jobs_and_Macintosh_computer%2C_January_1984%2C_by_Bernard_Gotfryd_-_edited.jpg",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])