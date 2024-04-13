from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

def main():
    client = QdrantClient(host="localhost", port=6333)
    encoder = SentenceTransformer("all-MiniLM-L6-v2")

    # Basic query example
    query_text = "alien invasion"
    print(f"Searching for: '{query_text}'")
    hits = client.search(
        collection_name="my_books",
        query_vector=encoder.encode(query_text).tolist(),
        limit=3,
    )
    for hit in hits:
        print(hit.payload, "score:", hit.score)

    # Narrowed down query example
    query_text = "alien invasion"
    print(f"\nNarrowed down search for: '{query_text}' since 2000")
    hits = client.search(
        collection_name="my_books",
        query_vector=encoder.encode(query_text).tolist(),
        query_filter=models.Filter(
            must=[models.FieldCondition(key="year", range=models.Range(gte=2000))]
        ),
        limit=1,
    )
    for hit in hits:
        print(hit.payload, "score:", hit.score)

if __name__ == "__main__":
    main()
