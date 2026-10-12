from unified_skill_loader import load_unified_skills


skills = load_unified_skills()


print("Total unified skills:", len(skills))

print("\nColumns:")
print(skills.columns.tolist())


print("\nSample:")
print(
    skills[
        [
            "skill_id",
            "skill_name",
            "category",
            "source",
            "normalized_name"
        ]
    ]
    .head(20)
    .to_string(index=False)
)