from sentence_transformers import SentenceTransformer, util
from skill_loader import load_skills


# Load the pretrained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load ESCO skills
skills_df = load_skills()

skill_names = skills_df["preferredLabel"].tolist()

# Create embeddings for all ESCO skills
skill_embeddings = model.encode(
    skill_names,
    convert_to_tensor=True,
    show_progress_bar=True
)


def extract_semantic_skills(
    resume_text: str,
    threshold: float = 0.70
):
    """
    Find ESCO skills that are semantically related
    to the resume text.
    """

    # Convert resume text into an embedding
    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    # Compare resume against every ESCO skill
    similarities = util.cos_sim(
        resume_embedding,
        skill_embeddings
    )[0]

    # Get skills above similarity threshold
    matches = []

    for index, score in enumerate(similarities):

        score_value = float(score)

        if score_value >= threshold:
            matches.append({
                "skill": skill_names[index],
                "similarity": round(score_value, 4)
            })

    # Highest similarity first
    matches.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return matches