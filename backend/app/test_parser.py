from resume_parser import process_resume_text


text = """
John Doe is a Python developer.

He worked at Google for 3 years and developed
web applications using FastAPI and PostgreSQL.

He completed his B.Tech in Computer Science in 2024.
"""


result = process_resume_text(text)

print("\nENTITIES:")
for entity in result["entities"]:
    print(entity)

print("\nSENTENCES:")
for sentence in result["sentences"]:
    print(sentence)