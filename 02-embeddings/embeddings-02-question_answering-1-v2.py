import pandas as pd
from openai import OpenAI
import numpy as np
from scipy.spatial.distance import cdist
import json
import time

# Định nghĩa các hằng số
EMBEDDING_MODEL = "text-embedding-ada-002"
DATA_PATH = "data/winter_olympics_2022.csv"

# Khởi tạo OpenAI client
client = OpenAI()

def safe_literal_eval(s):
    try:
        return np.array(json.loads(s.replace('\n', '').replace('array(', '[').replace(')', ']')))
    except json.JSONDecodeError:
        return np.zeros(0)

def create_embeddings(queries):
    responses = [client.embeddings.create(model=EMBEDDING_MODEL, input=query) for query in queries]
    return [np.array(response.data[0].embedding) for response in responses]

def search_top_related_texts(query, df, top_n=5):
    query_embedding = create_embeddings([query])[0]
    embeddings = np.vstack(df['embedding'].values)
    distances = cdist([query_embedding], embeddings, 'cosine')[0]
    top_indices = distances.argsort()[:top_n]
    return df.iloc[top_indices]['text'].values, 1 - distances[top_indices]

# Chính code
start_time = time.time()

df = pd.read_csv(DATA_PATH)
df['embedding'] = df['embedding'].apply(safe_literal_eval)

user_query = "Which athletes won the medal in hockey at the 2022 Winter Olympics?"
top_strings, top_relatednesses = search_top_related_texts(user_query, df)

for string, relatedness in zip(top_strings, top_relatednesses):
    print(f"Điểm liên quan: {relatedness:.3f}")
    print(string)
    print("\n---\n")

print(f"Thời gian thực thi: {time.time() - start_time} giây.")
