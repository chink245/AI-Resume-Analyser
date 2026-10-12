from skill_loader import load_skills


skills = load_skills()

print("Total skills:", len(skills))

print("\nFirst 10 skills:")
print(
    skills[
        ["preferredLabel", "altLabels"]
    ].head(10).to_string(index=False)
)