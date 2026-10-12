from unified_skill_loader import load_unified_skills


skills = load_unified_skills()

terms = [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "MongoDB",
    "React",
    "Next.js",
    "AWS",
    "Git",
    "GitHub",
    "Docker",
    "JavaScript",
    "Node.js"
]


for term in terms:

    # Exact skill-name comparison
    matches = skills[
        skills["skill_name"]
        .str.strip()
        .str.casefold()
        == term.casefold()
    ]

    print(f"\n===== {term} =====")

    if matches.empty:
        print("❌ Not found")
    else:
        print(
            matches[
                ["skill_name", "aliases", "source"]
            ].to_string(index=False)
        )