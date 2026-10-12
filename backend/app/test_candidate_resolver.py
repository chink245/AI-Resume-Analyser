from candidate_resolver import resolve_resume_candidates


resume = """
I am a Python developer with experience building REST APIs
using FastAPI.

I have worked with PostgreSQL and MongoDB
and developed web applications using React and Next.js.

I use Git and GitHub for version control and have deployed
applications using AWS and Docker.
"""


results = resolve_resume_candidates(
    resume
)


print("\n")
print("RESOLVED RESUME SKILLS")
print("=" * 70)


for skill in results:

    print(
        f"{skill['skill']} | "
        f"{skill['match_type']} | "
        f"{skill['confidence']} | "
        f"{skill['source']}"
    )