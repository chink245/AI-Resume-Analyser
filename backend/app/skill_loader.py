import pandas as pd
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent / "data" / "skills_en.csv"


def load_skills():
    """
    Load skills from the ESCO dataset.
    """

    df = pd.read_csv(DATA_PATH)

    # Keep only actual skill/competence records
    df = df[
        df["conceptType"] == "KnowledgeSkillCompetence"
    ]

    # Remove records without a preferred skill name
    df = df.dropna(subset=["preferredLabel"])

    # Keep only the information we need
    skills = df[
        [
            "conceptUri",
            "preferredLabel",
            "altLabels",
            "definition",
            "description"
        ]
    ].copy()

    # Remove duplicate skill names
    skills = skills.drop_duplicates(
        subset=["preferredLabel"]
    )

    return skills