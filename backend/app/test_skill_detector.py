from skill_detector import detect_exact_skills


resume = """
I am a Python developer with experience building REST APIs
using FastAPI.

I have worked with Postgres and MongoDB
and developed web applications using React and Next.js.

I use Git and GitHub for version control and have deployed
applications using AWS and Docker.
"""


skills = detect_exact_skills(resume)


print("\nDetected Skills:\n")


for skill in skills:

    print(
        skill["skill"],
        "->",
        skill["match_type"],
        "->",
        skill["source"]
    )