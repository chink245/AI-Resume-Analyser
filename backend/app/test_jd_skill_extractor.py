from jd_skill_extractor import extract_jd_skills


job_description = """

We are looking for a Python developer
with experience building REST APIs using FastAPI.

The candidate should have experience with
PostgreSQL, MongoDB, React and Next.js.

Experience with Git, GitHub, Docker and AWS
is also required.

"""


skills = extract_jd_skills(
    job_description
)


print("\n")
print("=" * 70)
print("JOB DESCRIPTION SKILLS")
print("=" * 70)


for skill in skills:

    print(
        f'{skill["skill"]} | '
        f'{skill["match_type"]} | '
        f'{skill["confidence"]} | '
        f'{skill["source"]}'
    )