import pandas as pd
from openai import OpenAI
import numpy as np
from scipy.spatial.distance import cdist
import json
import time
import tiktoken  # Thêm thư viện này để đếm số token

# Bắt đầu đo thời gian
start_time = time.time()

# Khởi tạo OpenAI client
client = OpenAI()

def safe_literal_eval(s):
    try:
        return np.array(json.loads(s.replace('\n', '').replace('array(', '[').replace(')', ']')))
    except json.JSONDecodeError:
        return np.zeros(0)

# Vector hóa việc tạo embeddings
def create_embedding(query):
    response = client.embeddings.create(model="text-embedding-ada-002", input=query)
    return np.array(response.data[0].embedding)

# Hàm tìm kiếm các đoạn văn bản liên quan nhất dựa trên embeddings
def search_top_related_texts(query, df, top_n=5):
    query_embedding = create_embedding(query)
    embeddings = np.vstack(df['embedding'].values)
    distances = cdist([query_embedding], embeddings, 'cosine')[0]
    top_indices = distances.argsort()[:top_n]
    return df.iloc[top_indices]['text'].values, 1 - distances[top_indices]

# Hàm đếm số token của một chuỗi văn bản
def num_tokens(text: str) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))

# Tạo thông điệp cho GPT với các đoạn văn bản liên quan
def create_message_for_gpt(query, top_strings, token_budget=4096):
    introduction = 'Use the below articles on the 2022 Winter Olympics to answer the subsequent question. If the answer cannot be found in the articles, write "I could not find an answer."'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in top_strings:
        next_section = f'\n\nWikipedia article section:\n"""\n{string}\n"""'
        if num_tokens(message + next_section + question) > token_budget:
            break
        else:
            message += next_section
    return message + question

# Hàm gửi câu hỏi tới GPT và nhận câu trả lời
def ask_gpt(query, top_strings, model="gpt-3.5-turbo", token_budget=4096):
    message = create_message_for_gpt(query, top_strings, token_budget)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You answer questions about the 2022 Winter Olympics."},
            {"role": "user", "content": message},
        ],
        temperature=0
    )
    return response.choices[0].message.content

# Đọc file CSV và chuẩn bị embeddings
df = pd.read_csv("data/winter_olympics_2022.csv")
df['embedding'] = df['embedding'].apply(safe_literal_eval)

# Tìm top 5 đoạn văn bản liên quan nhất
user_query = "Which athletes won the medal in hockey at the 2022 Winter Olympics?"
top_strings, top_relatednesses = search_top_related_texts(user_query, df)

# Sử dụng hàm ask_gpt để nhận câu trả lời từ GPT
answer = ask_gpt(user_query, top_strings)
print("Answer from GPT:", answer)

# Kết thúc đo thời gian và in ra
new_version_time = time.time() - start_time
print(f"Thời gian thực thi: {new_version_time} giây.")
