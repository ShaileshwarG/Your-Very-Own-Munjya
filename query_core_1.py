# query_core_1.py

import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load CSV knowledge
def load_core_knowledge():
    path = os.path.join(os.path.dirname(__file__), "core_1_knowledge.csv")
    return pd.read_csv(path)

# Build the FAISS index
def build_faiss_index(df, model):
    embeddings = model.encode(df["query"].tolist(), show_progress_bar=False)
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(np.array(embeddings).astype("float32"))
    return index, embeddings

# Load and index once
model = SentenceTransformer("all-MiniLM-L6-v2")  # ✅ Compact + fast
core_knowledge_df = load_core_knowledge()
faiss_index, core_embeddings = build_faiss_index(core_knowledge_df, model)

# Search interface
def query_core_1(user_query, top_k=1, threshold=0.6):
    query_embedding = model.encode([user_query])[0].astype("float32")
    D, I = faiss_index.search(np.array([query_embedding]), k=top_k)

    if D[0][0] < threshold:
        return ""  # No confident match found

    matched_index = I[0][0]
    return core_knowledge_df.iloc[matched_index]["response"]
