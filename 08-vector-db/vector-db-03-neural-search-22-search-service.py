from fastapi import FastAPI
from neural_searcher import NeuralSearcher

app = FastAPI()

# Create an instance of NeuralSearcher
neural_searcher = NeuralSearcher(collection_name="startups")

@app.get("/api/search")
def search_startup(q: str):
    # Perform the search using the NeuralSearcher instance
    return {"result": neural_searcher.search(text=q)}

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app with uvicorn on host 0.0.0.0 and port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
