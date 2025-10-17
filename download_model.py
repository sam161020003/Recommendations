# download_model.py
from sentence_transformers import SentenceTransformer

print("Attempting to download and cache the CLIP model...")
print("This may take a few minutes. Please wait.")

try:
    # This command will download the model to your local cache
    # Using the full model name is crucial.
    model = SentenceTransformer('sentence-transformers/clip-ViT-B-32', device='cpu')
    print("\n✅ Model downloaded and cached successfully!")
except Exception as e:
    print(f"\n❌ An error occurred: {e}")