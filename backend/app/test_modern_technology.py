from technology_index import build_technology_index


index = build_technology_index()


print(
    "Total indexed technology terms:",
    len(index)
)


tests = [
    "fastapi",
    "fast api",
    "next.js",
    "next js",
    "node.js",
    "nodejs",
    "express",
    "react",
    "docker",
    "aws"
]


print("\nTEST RESULTS")
print("=" * 70)


for term in tests:

    key = term.casefold()

    result = index.get(key)

    print(
        f"{term:15} -> {result}"
    )