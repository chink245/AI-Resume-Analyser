from analysis_service import analyze_resume_vs_job


resume = """
I am a Python developer with experience building REST APIs
using FastAPI.

I have worked with PostgreSQL and MongoDB
and developed web applications using React and Next.js.

I use Git and GitHub for version control and have deployed
applications using AWS and Docker.
"""


job_description = """
We are looking for a developer with experience in:

Python
FastAPI
PostgreSQL
MongoDB
React
Next.js
JavaScript
Git
GitHub
Docker
AWS
"""


result = analyze_resume_vs_job(
    resume,
    job_description
)


print("\n")
print("=" * 70)
print("FINAL ANALYSIS")
print("=" * 70)

print(
    "\nMatch Percentage:",
    result["match_percentage"],
    "%"
)

print(
    "Total Required:",
    result["total_required"]
)

print(
    "Total Matched:",
    result["total_matched"]
)


print("\nMATCHED SKILLS")
print("-" * 70)

for skill in result["matched_skills"]:

    print(skill)


print("\nMISSING SKILLS")
print("-" * 70)

for skill in result["missing_skills"]:

    print(skill)


print("\nRESUME SKILLS")
print("-" * 70)

for skill in result["resume_skills"]:

    print(
        skill["skill"],
        "|",
        skill["match_type"],
        "|",
        skill["confidence"]
    )


print("\nJOB DESCRIPTION SKILLS")
print("-" * 70)

for skill in result["job_skills"]:

    print(
        skill["skill"],
        "|",
        skill["match_type"],
        "|",
        skill["confidence"]
    )