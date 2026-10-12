from candidate_extractor import extract_candidates


resume = """
I am a Python developer with experience building REST APIs
using FastAPI.

I have worked with PostgreSQL and MongoDB
and developed web applications using React and Next.js.

I use Git and GitHub for version control and have deployed
applications using AWS and Docker.
"""


candidates = extract_candidates(
    resume
)


print("\n")
print("CANDIDATE PHRASES")
print("=" * 60)


for candidate in candidates:

    print(candidate)