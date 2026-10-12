from final_skill_resolver import resolve_resume_skills


resume_text = """
Languages: Java, JavaScript, Python, SQL
"""


results = resolve_resume_skills(resume_text)


print("\n=== RESOLVED RESUME SKILLS ===")

for skill in results:
    print(skill)