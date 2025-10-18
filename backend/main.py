import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import torch
from dotenv import load_dotenv

# --- LangChain Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# =====================================================================================
# 1. INITIALIZATION
# =====================================================================================

# Load environment variables from .env file
load_dotenv()

# Check for GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"--- Backend using device: {device} ---")

# Load the sentence transformer model once during startup
print("--- Loading embedding model... ---")
embed_model = SentenceTransformer('clip-ViT-B-32', device=device)
print("--- Embedding model loaded successfully. ---")

# Initialize Pinecone
print("--- Initializing Pinecone... ---")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = 'product-recommender'

if index_name not in pc.list_indexes().names():
    raise RuntimeError(f"Pinecone index '{index_name}' does not exist. Please run the model training notebook first.")
index = pc.Index(index_name)
print(f"--- Connected to Pinecone index '{index_name}'. ---")


# Initialize LangChain with Google Gemini (latest stable model)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Create a prompt template for the description generation
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a creative marketing assistant. Generate a concise, one-paragraph product description."),
    ("user", "Generate a description for this product: Title - {product_title}, Brand - {product_brand}.")
])
output_parser = StrOutputParser()
description_chain = prompt | llm | output_parser


# Initialize FastAPI app
app = FastAPI()

# =====================================================================================
# 2. CORS MIDDLEWARE
# =====================================================================================

origins = ["http://localhost:3000","https://*.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================================
# 3. Pydantic Models
# =====================================================================================

class Query(BaseModel):
    query: str
    top_k: int = 12

class ProductDetails(BaseModel):
    product_title: str
    product_brand: str

# =====================================================================================
# 4. API ENDPOINTS
# =====================================================================================

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Product Recommendation API is running."}

@app.get("/analytics")
def get_analytics():
    try:
        with open("analytics_output.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Analytics file not found.")

@app.post("/recommend")
def recommend_products(query: Query):
    try:
        text_embedding = embed_model.encode(query.query).tolist()
        image_embedding_placeholder = [0.0] * 512
        query_vector = text_embedding + image_embedding_placeholder

        results = index.query(
            vector=query_vector,
            top_k=query.top_k,
            include_metadata=True
        )
        
        product_matches = [
            {'id': match['id'], 'score': match['score'], 'metadata': match['metadata']}
            for match in results['matches']
        ]
        return {"products": product_matches}
    except Exception as e:
        print(f"Error during recommendation: {e}")
        raise HTTPException(status_code=500, detail="Error fetching recommendations.")

@app.post("/generate-description")
def generate_description(details: ProductDetails):
    try:
        # Use the modern .invoke() method
        description = description_chain.invoke({
            "product_title": details.product_title,
            "product_brand": details.product_brand
        })
        return {"description": description.strip()}
    except Exception as e:
        # This will now print a more detailed error if Google API fails
        print(f"Error during description generation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate description.")
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server on port 7860...")
    uvicorn.run("main:app", host="0.0.0.0", port=7860)
