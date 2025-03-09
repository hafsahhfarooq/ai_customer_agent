import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load sentence transformer model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Sample return policy knowledge base
RETURN_POLICIES = [
    "Returns are allowed within 30 days if the item is defective or damaged.",
    "Clothing items can only be returned if they are unworn and with original tags.",
    "Electronics must be returned in their original packaging with all accessories.",
    "Customized or personalized items are non-returnable.",
    "Sale items are final and cannot be returned.",
]

# Generate embeddings for return policies
policy_embeddings = np.array([embedding_model.encode(policy) for policy in RETURN_POLICIES])

# Create FAISS index
dimension = policy_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(policy_embeddings)


def retrieve_policy(user_request: str):
    """Retrieve the most relevant return policy based on vector similarity."""
    user_embedding = np.array([embedding_model.encode(user_request)])
    distances, indices = index.search(user_embedding, k=1)

    closest_policy = RETURN_POLICIES[indices[0][0]]
    return closest_policy, float(distances[0][0])
