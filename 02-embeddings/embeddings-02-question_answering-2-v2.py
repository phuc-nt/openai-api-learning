import pandas as pd
from openai import OpenAI
import numpy as np
from scipy.spatial.distance import cdist
import json
import time
import tiktoken

# Định nghĩa các hằng số
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"
TOKEN_BUDGET = 4096
DATA_PATH = "data/winter_olympics_2022.csv"

# Khởi tạo OpenAI client
client = OpenAI()

def safe_literal_eval(s):
    try:
        return np.array(json.loads(s.replace('\n', '').replace('array(', '[').replace(')', ']')))
    except json.JSONDecodeError:
        return np.zeros(0)

def create_embedding(query, model=EMBEDDING_MODEL):
    response = client.embeddings.create(model=model, input=query)
    return np.array(response.data[0].embedding)

def search_top_related_texts(query, df, top_n=5):
    query_embedding = create_embedding(query)
    embeddings = np.vstack(df['embedding'].values)
    distances = cdist([query_embedding], embeddings, 'cosine')[0]
    top_indices = distances.argsort()[:top_n]
    return df.iloc[top_indices]['text'].values, 1 - distances[top_indices]

def num_tokens(text):
    encoding = tiktoken.encoding_for_model(GPT_MODEL)
    return len(encoding.encode(text))

def create_message_for_gpt(query, top_strings, token_budget=TOKEN_BUDGET):
    introduction = 'Use the below articles on the 2022 Winter Olympics to answer the question. Trả lời bằng tiếng Việt.'
    message = introduction + "\n\nQuestion: " + query
    for string in top_strings:
        next_section = f'\n\nArticle section:\n"""\n{string}\n"""'
        if num_tokens(message + next_section) <= token_budget:
            message += next_section
        else:
            break
    return message

def ask_gpt(query, top_strings, model=GPT_MODEL, token_budget=TOKEN_BUDGET):
    message = create_message_for_gpt(query, top_strings, token_budget)
    response = client.chat.completions.create(model=model, messages=[{"role": "system", "content": "Answer questions about the 2022 Winter Olympics."}, {"role": "user", "content": message}], temperature=0)
    return response.choices[0].message.content

# Chính code
start_time = time.time()
df = pd.read_csv(DATA_PATH)
df['embedding'] = df['embedding'].apply(safe_literal_eval)
user_query = "Which athletes won the medal in hockey at the 2022 Winter Olympics?"
top_strings, _ = search_top_related_texts(user_query, df)
answer = ask_gpt(user_query, top_strings)
print("Answer from GPT:", answer)
print(f"Thời gian thực thi: {time.time() - start_time} giây.")
