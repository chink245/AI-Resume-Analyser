from skill_detector import detect_exact_skills


resume_text = """
Languages: Java, JavaScript, Python, SQL
"""


results = detect_exact_skills(resume_text)


print("\n=== DETECTED SKILLS ===")

for skill in results:
    print(skill)