from unified_skill_loader import load_unified_skills


skills = load_unified_skills()


python_rows = skills[
    skills["skill_name"]
    .str.contains(
        "Python",
        case=False,
        na=False
    )
]


print(
    python_rows[
        [
            "skill_name",
            "aliases",
            "source"
        ]
    ].to_string(index=False)
)