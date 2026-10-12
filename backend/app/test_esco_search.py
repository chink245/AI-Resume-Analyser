from skill_loader import load_skills


skills = load_skills()


search_terms = [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "MongoDB",
    "React",
    "Next.js",
    "AWS",
    "Git",
    "GitHub"
]


for term in search_terms:

    results = skills[
        skills["preferredLabel"]
        .str.contains(
            term,
            case=False,
            na=False
        )
    ]

    print(f"\n===== {term} =====")

    if results.empty:
        print("No preferred-label match found")
    else:
        print(
            results[
                [
                    "preferredLabel",
                    "altLabels"
                ]
            ].head(5).to_string(index=False)
        )