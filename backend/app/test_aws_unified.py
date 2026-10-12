from unified_skill_loader import load_unified_skills


skills = load_unified_skills()


aws = skills[
    skills["skill_name"]
    .str.contains(
        "AWS|Amazon Web Services",
        case=False,
        na=False
    )
]


print(
    "\nAWS-related unified records:\n"
)


print(
    aws[
        [
            "skill_id",
            "skill_name",
            "category",
            "source",
            "normalized_name"
        ]
    ]
    .to_string(index=False)
)