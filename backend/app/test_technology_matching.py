from unified_skill_loader import load_unified_skills
import re


skills = load_unified_skills()


def find_matching_technologies(text):

    text = text.casefold()

    matches = []

    for _, row in skills.iterrows():

        skill = row["skill_name"]

        if not skill:
            continue

        skill = skill.casefold()

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, text):

            matches.append({
                "skill": row["skill_name"],
                "source": row["source"],
                "category": row["category"]
            })

    return matches


resume = """
I have experience with AWS.
I have used AWS CloudFormation and AWS SageMaker.
I also worked with PostgreSQL, MongoDB, React and GitHub.
"""


results = find_matching_technologies(resume)


print("\nDetected technologies:\n")

for result in results:

    print(
        f"{result['skill']} | "
        f"{result['category']} | "
        f"{result['source']}"
    )