from sentence_transformers import SentenceTransformer, util
from skill_loader import load_skills
import spacy


nlp = spacy.load("en_core_web_sm")

model = SentenceTransformer("all-MiniLM-L6-v2")

skills_df = load_skills()

skill_names = skills_df["preferredLabel"].tolist()

skill_embeddings = model.encode(
    skill_names,
    convert_to_tensor=True,
    show_progress_bar=True
)


resume = """
I am a Python developer with experience building REST APIs
using FastAPI. I have worked with PostgreSQL and MongoDB
and developed web applications using React and Next.js.
I use Git and GitHub for version control and have deployed
applications using AWS.
"""


doc = nlp(resume)

sentences = [
    sentence.text.strip()
    for sentence in doc.sents
]


print("\nRESUME SENTENCES:\n")

for sentence in sentences:
    print("-", sentence)


print("\nSEMANTIC MATCHES:\n")


for sentence in sentences:

    sentence_embedding = model.encode(
        sentence,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        sentence_embedding,
        skill_embeddings
    )[0]

    top_results = similarities.topk(5)

    print(f"\nSentence: {sentence}")

    for score, index in zip(
        top_results.values,
        top_results.indices
    ):
        print(
            f"  {skill_names[index]} "
            f"-> {float(score):.4f}"
        )