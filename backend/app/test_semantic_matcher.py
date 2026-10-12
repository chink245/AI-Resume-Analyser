from semantic_matcher import semantic_similarity


resume_sentence = """
I developed REST APIs using FastAPI and
built modern web applications using Next.js.
"""


candidate_skills = [
    "FastAPI",
    "Next.js",
    "Python",
    "React",
    "PostgreSQL",
    "Docker",
    "database management",
    "web application development"
]


results = semantic_similarity(
    resume_sentence,
    candidate_skills
)


print("\nSemantic Results:\n")


for result in results:

    print(
        f"{result['skill']} "
        f"-> "
        f"{result['similarity']:.4f}"
    )