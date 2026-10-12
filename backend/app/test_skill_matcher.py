from skill_matcher import match_resume_with_jd


resume = """

I am a Python developer with experience building REST APIs
using FastAPI.

I have worked with Postgres and MongoDB
and developed web applications using React and Next.js.

I use Git and GitHub for version control and have deployed
applications using AWS and Docker.

"""


job_description = """

We are looking for a Python developer
with experience building REST APIs using FastAPI.

The candidate should have experience with
PostgreSQL, MongoDB, React and Next.js.

Experience with Git, GitHub, Docker and AWS
is also required.

"""


result = match_resume_with_jd(
    resume,
    job_description
)


print("\n")
print("=" * 70)
print("RESUME vs JOB DESCRIPTION")
print("=" * 70)


print(
    "\nMatch Percentage:",
    result["match_percentage"],
    "%"
)


print(
    "\nTotal Required:",
    result["total_required"]
)


print(
    "Total Matched:",
    result["total_matched"]
)


print("\nMATCHED SKILLS")
print("-" * 70)

for skill in result["matched_skills"]:

    print(
        skill["skill"]
    )


print("\nMISSING SKILLS")
print("-" * 70)

for skill in result["missing_skills"]:

    print(
        skill["skill"]
    )