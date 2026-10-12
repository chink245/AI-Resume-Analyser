from sentence_transformers import SentenceTransformer
from unified_skill_loader import load_unified_skills
from pathlib import Path
import numpy as np
import faiss


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

INDEX_DIR = BASE_DIR / "vector_store"

INDEX_DIR.mkdir(
    parents=True,
    exist_ok=True
)

INDEX_FILE = INDEX_DIR / "skills.index"


# =========================================================
# LOAD MODEL ONCE
# =========================================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading SentenceTransformer model...")

model = SentenceTransformer(
    MODEL_NAME
)

print("Model loaded successfully!")


# =========================================================
# LOAD SKILLS ONCE
# =========================================================

print("Loading unified skills...")

skills_df = load_unified_skills()

print(
    f"Total skills loaded: {len(skills_df)}"
)


# =========================================================
# LOAD FAISS INDEX ONCE
# =========================================================

index = None


if INDEX_FILE.exists():

    print("Loading FAISS index...")

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    print(
        f"FAISS index loaded: {index.ntotal} vectors"
    )

else:

    print(
        "FAISS index not found."
    )

    print(
        "Run build_vector_index() before semantic search."
    )


# =========================================================
# BUILD VECTOR INDEX
# =========================================================

def build_vector_index():

    global index

    print(
        "Generating skill embeddings..."
    )


    # -----------------------------------------------------
    # Prepare skill names
    # -----------------------------------------------------

    skill_names = (
        skills_df["skill_name"]
        .astype(str)
        .tolist()
    )


    # -----------------------------------------------------
    # Generate embeddings
    # -----------------------------------------------------

    embeddings = model.encode(

        skill_names,

        batch_size=64,

        show_progress_bar=True,

        normalize_embeddings=True
    )


    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )


    print(
        f"Embedding shape: {embeddings.shape}"
    )


    # -----------------------------------------------------
    # Create FAISS index
    # -----------------------------------------------------

    dimension = embeddings.shape[1]

    new_index = faiss.IndexFlatIP(
        dimension
    )


    # -----------------------------------------------------
    # Add vectors
    # -----------------------------------------------------

    new_index.add(
        embeddings
    )


    # -----------------------------------------------------
    # Save index
    # -----------------------------------------------------

    faiss.write_index(
        new_index,
        str(INDEX_FILE)
    )


    # -----------------------------------------------------
    # Update global index
    # -----------------------------------------------------

    index = new_index


    print(
        "\nVector index created successfully!"
    )

    print(
        f"Indexed vectors: {index.ntotal}"
    )

    print(
        f"Saved to: {INDEX_FILE}"
    )


    return index


# =========================================================
# PROCESS FAISS RESULTS
# =========================================================

def _process_results(
    scores,
    indices,
    top_k,
    min_similarity
):

    results = []


    # -----------------------------------------------------
    # Process first query
    # -----------------------------------------------------

    for score, index_id in zip(
        scores,
        indices
    ):

        # -------------------------------------------------
        # Invalid index
        # -------------------------------------------------

        if index_id < 0:
            continue


        # -------------------------------------------------
        # Similarity threshold
        # -------------------------------------------------

        if float(score) < min_similarity:
            continue


        # -------------------------------------------------
        # Get skill
        # -------------------------------------------------

        row = skills_df.iloc[
            int(index_id)
        ]


        # -------------------------------------------------
        # Add result
        # -------------------------------------------------

        results.append({

            "skill_id": int(
                row["skill_id"]
            ),

            "skill": row[
                "skill_name"
            ],

            "source": row[
                "source"
            ],

            "category": row[
                "category"
            ],

            "similarity": float(
                score
            )
        })


    return results


# =========================================================
# SINGLE SEARCH
# =========================================================

def search_skills(
    query,
    top_k=10,
    min_similarity=0.60
):

    if not query:
        return []


    # -----------------------------------------------------
    # Make sure index exists
    # -----------------------------------------------------

    if index is None:

        raise FileNotFoundError(
            "FAISS index is not loaded. "
            "Run build_vector_index() first."
        )


    # -----------------------------------------------------
    # Encode query
    # -----------------------------------------------------

    query_embedding = model.encode(

        [query],

        normalize_embeddings=True
    )


    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )


    # -----------------------------------------------------
    # FAISS search
    # -----------------------------------------------------

    scores, indices = index.search(

        query_embedding,

        top_k
    )


    # -----------------------------------------------------
    # Process results
    # -----------------------------------------------------

    return _process_results(

        scores[0],

        indices[0],

        top_k,

        min_similarity
    )


# =========================================================
# BATCH SEARCH
# =========================================================

def search_skills_batch(
    queries,
    top_k=3,
    min_similarity=0.78
):

    if not queries:
        return []


    # -----------------------------------------------------
    # Make sure index exists
    # -----------------------------------------------------

    if index is None:

        raise FileNotFoundError(
            "FAISS index is not loaded. "
            "Run build_vector_index() first."
        )


    # -----------------------------------------------------
    # Clean queries
    # -----------------------------------------------------

    cleaned_queries = [

        str(query).strip()

        for query in queries

        if query and str(query).strip()

    ]


    if not cleaned_queries:
        return []


    # -----------------------------------------------------
    # Generate ALL embeddings together
    # -----------------------------------------------------

    query_embeddings = model.encode(

        cleaned_queries,

        batch_size=32,

        normalize_embeddings=True
    )


    query_embeddings = np.asarray(

        query_embeddings,

        dtype="float32"

    )


    # -----------------------------------------------------
    # Search ALL queries together
    # -----------------------------------------------------

    scores, indices = index.search(

        query_embeddings,

        top_k

    )


    # -----------------------------------------------------
    # Build results
    # -----------------------------------------------------

    all_results = []


    for query_index in range(
        len(cleaned_queries)
    ):

        query_results = _process_results(

            scores[query_index],

            indices[query_index],

            top_k,

            min_similarity

        )


        all_results.append({

            "query": cleaned_queries[
                query_index
            ],

            "results": query_results

        })


    return all_results