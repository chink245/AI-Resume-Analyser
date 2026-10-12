from skill_alias_index import build_alias_index


alias_index = build_alias_index()


print(
    "Total searchable names:",
    len(alias_index)
)


test_terms = [
    "Python",
    "python 3k",
    "PostgreSQL",
    "Postgres",
    "Haskell"
]


print("\nTest results:\n")


for term in test_terms:

    normalized = term.casefold()

    skill_id = alias_index.get(
        normalized
    )

    print(
        f"{term} -> {skill_id}"
    )