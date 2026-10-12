from vector_index import search_skills


result = search_skills(
    "version control",
    top_k=5,
    min_similarity=0.70
)


print("=" * 70)
print("SEMANTIC DEBUG")
print("=" * 70)

for item in result:

    print("\nSKILL:")
    print(repr(item["skill"]))

    print("CATEGORY:")
    print(repr(item["category"]))

    print("SOURCE:")
    print(repr(item["source"]))

    print("SIMILARITY:")
    print(item["similarity"])