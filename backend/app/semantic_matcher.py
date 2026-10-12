from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ---------------------------------------------------------
# Load model once
# ---------------------------------------------------------

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------------------------------------------------
# Calculate semantic similarity
# ---------------------------------------------------------

def semantic_similarity(
    resume_text,
    skill_names
):

    if not resume_text:
        return []

    if not skill_names:
        return []

    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True
    )

    skill_embeddings = model.encode(
        skill_names,
        normalize_embeddings=True
    )

    similarities = cosine_similarity(
        resume_embedding,
        skill_embeddings
    )[0]

    results = []

    for skill, score in zip(
        skill_names,
        similarities
    ):

        results.append({
            "skill": skill,
            "similarity": float(score)
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results