from final_skill_resolver import resolve_resume_skills


resume = """

I am a Python developer with experience building REST APIs
using FastAPI.

I have worked with Postgres and MongoDB
and developed web applications using React and Next.js.

I use Git and GitHub for version control and have deployed
applications using AWS and Docker.

"""


skills = resolve_resume_skills(
    resume
)


print("\n")
print("=" * 70)
print("FINAL RESUME SKILLS")
print("=" * 70)


for skill in skills:

    print(
        f'{skill["skill"]} | '
        f'{skill["match_type"]} | '
        f'{skill["confidence"]} | '
        f'{skill["source"]}'
    )