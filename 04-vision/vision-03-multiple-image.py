from openai import OpenAI
from pprint import pprint

client = OpenAI()
response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "những tấm hình này có gì? chúng có đièu gì tương đồng?",
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/en/8/82/Superman_issue_6_1940.jpg",
          },
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/en/9/95/Batman_%26_Robin_%28Batman_vol._1_-9_Feb._1942%29.jpg",
          },
        },
      ],
    }
  ],
  max_tokens=1000,
)
pprint(response.choices[0].message.content)