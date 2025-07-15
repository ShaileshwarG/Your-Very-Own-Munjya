import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load CSV knowledge
def load_core_knowledge():
    path = os.path.join(os.path.dirname(__file__), "core_1_knowledge.csv")  # ✅ Your confirmed filename
    return pd.read_csv(path)

# Build the FAISS index (cosine similarity)
def build_faiss_index(df, model):
    embeddings = model.encode(df["query"].tolist(), show_progress_bar=False, normalize_embeddings=True)
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatIP(dimension)  # ✅ Cosine similarity via normalized dot product
    index.add(np.array(embeddings).astype("float32"))
    return index, embeddings

# Load once
model = SentenceTransformer("all-MiniLM-L6-v2")
core_knowledge_df = load_core_knowledge()
faiss_index, core_embeddings = build_faiss_index(core_knowledge_df, model)

# Query logic (Top-K=3)
def query_core_1(user_query, top_k=3, threshold=0.7):
    query_embedding = model.encode([user_query], normalize_embeddings=True)[0].astype("float32")
    scores, indices = faiss_index.search(np.array([query_embedding]), k=top_k)

    # Optional: Print or log all top matches
    # for i in range(top_k):
    #     print(f"[{i+1}] Score: {scores[0][i]:.4f} → {core_knowledge_df.iloc[indices[0][i]]['query']}")

    # Choose top response above threshold
    for i in range(top_k):
        score = scores[0][i]
        idx = indices[0][i]
        if score >= threshold:
            return core_knowledge_df.iloc[idx]["response"]

    return ""  # If no confident result found
