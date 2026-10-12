from technology_index import build_technology_index


index = build_technology_index()


print(
    "Total indexed terms:",
    len(index)
)


test_terms = [
    "aws",
    "github",
    "mongodb",
    "react",
    "docker"
]


print("\nTest terms:\n")


for term in test_terms:

    skill_id = index.get(
        term.casefold()
    )

    print(
        f"{term} -> {skill_id}"
    )