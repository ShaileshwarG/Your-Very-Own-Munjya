# query_core_1.py

import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load CSV knowledge base
def load_core_knowledge():
    path = os.path.join(os.path.dirname(__file__), "core_1_knowledge.csv")
    return pd.read_csv(path)

# Build the FAISS index once
def build_faiss_index(df, model):
    embeddings = model.encode(df["query"].tolist(), show_progress_bar=False)
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(np.array(embeddings).astype("float32"))
    return index, embeddings

# Load model and build index
model = SentenceTransformer("all-MiniLM-L6-v2")  # ✅ Fast + accurate for semantic queries
core_knowledge_df = load_core_knowledge()
faiss_index, core_embeddings = build_faiss_index(core_knowledge_df, model)

# Search Core_1 with threshold + fallback match
def query_core_1(user_query, top_k=3, threshold=0.4):
    query_embedding = model.encode([user_query])[0].astype("float32")
    D, I = faiss_index.search(np.array([query_embedding]), k=top_k)

    # Best match
    best_distance = D[0][0]
    best_index = I[0][0]
    best_answer = core_knowledge_df.iloc[best_index]["response"]

    # Check threshold
    if best_distance < threshold:
        return best_answer
    else:
        return f"(🤔 Approximate match from Core_1)\n{best_answer}"
