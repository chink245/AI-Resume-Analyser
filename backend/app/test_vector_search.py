from vector_index import search_skills


queries = [
    "Python developer",
    "REST API development",
    "React web application",
    "cloud deployment",
    "database management",
]


for query in queries:

    print("\n")
    print("=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)

    results = search_skills(
        query,
        top_k=5,
        min_similarity=0.60
    )

    for result in results:

        print(
            f"{result['skill']} "
            f"-> "
            f"{result['similarity']:.4f} "
            f"| {result['source']}"
        )