from vector_index import search_skills


sentences = [

    "I am a Python developer with experience building REST APIs using FastAPI.",

    "I have worked with PostgreSQL and MongoDB and developed web applications using React and Next.js.",

    "I use Git and GitHub for version control and have deployed applications using AWS and Docker."

]


for sentence in sentences:

    print("\n")
    print("=" * 80)
    print("SENTENCE:")
    print(sentence)
    print("=" * 80)


    results = search_skills(
        sentence,
        top_k=10,
        min_similarity=0.40
    )


    for result in results:

        print(
            f"{result['skill']} "
            f"-> "
            f"{result['similarity']:.4f} "
            f"| {result['source']}"
        )