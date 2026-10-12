import pandas as pd
import re
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"

ESCO_PATH = DATA_DIR / "skills_en.csv"
ONET_PATH = DATA_DIR / "software_skills.csv"


def normalize_text(text):
    """
    Normalize text for reliable comparison.
    """

    if pd.isna(text):
        return ""

    text = str(text)

    # Convert escaped newline characters into spaces
    text = text.replace("\\n", " ")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_key(text):
    """
    Create a normalized key used for duplicate detection.
    """

    text = normalize_text(text)

    return text.casefold()


def load_esco_skills():

    df = pd.read_csv(ESCO_PATH)

    df = df[
        df["conceptType"] == "KnowledgeSkillCompetence"
    ]

    df = df.dropna(
        subset=["preferredLabel"]
    )

    skills = pd.DataFrame({
        "skill_name": df["preferredLabel"].apply(
            normalize_text
        ),

        "aliases": df["altLabels"].apply(
            normalize_text
        ),

        "category": "skill",

        "source": "ESCO"
    })

    return skills


def load_onet_skills():

    df = pd.read_csv(ONET_PATH)

    df = df.dropna(
        subset=["Workplace Example"]
    )

    df["Workplace Example"] = (
        df["Workplace Example"]
        .apply(normalize_text)
    )

    df["Element Name"] = (
        df["Element Name"]
        .apply(normalize_text)
    )

    # Keep the technology itself as the canonical name.
    # Keep the O*NET category as metadata.
    skills = pd.DataFrame({
        "skill_name": df["Workplace Example"],

        "aliases": "",

        "category": df["Element Name"],

        "source": "ONET"
    })

    return skills

def load_unified_skills():

    esco = load_esco_skills()

    onet = load_onet_skills()

    unified = pd.concat(
        [esco, onet],
        ignore_index=True
    )

    # Remove empty skill names
    unified = unified[
        unified["skill_name"] != ""
    ]

    # Create normalized key
    unified["normalized_name"] = (
        unified["skill_name"]
        .apply(normalize_key)
    )

    # Remove duplicate canonical names
    unified = unified.drop_duplicates(
        subset=["normalized_name"]
    )

    # Create stable numeric ID
    unified.insert(
        0,
        "skill_id",
        range(1, len(unified) + 1)
    )

    return unified

if __name__ == "__main__":
    skills = load_unified_skills()

    print("\n=== SQL CHECK ===")
    print(
        skills[
            skills["skill_name"]
            .str.casefold()
            .eq("sql")
        ][
            ["skill_id", "skill_name", "category", "source"]
        ]
    )

    print("\n=== COMPUTER SCIENCE CHECK ===")
    print(
        skills[
            skills["skill_name"]
            .str.casefold()
            .eq("computer science")
        ][
            ["skill_id", "skill_name", "category", "source"]
        ]
    )    