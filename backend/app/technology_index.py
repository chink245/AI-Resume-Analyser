from unified_skill_loader import load_unified_skills
import pandas as pd
from pathlib import Path
import re
import hashlib


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

TECHNOLOGY_FILE = (
    BASE_DIR / "data" / "modern_technologies.csv"
)


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip().casefold()


# =========================================================
# BUILD TECHNOLOGY INDEX
# =========================================================

def build_technology_index():

    index = {}


    # =====================================================
    # 1. LOAD O*NET / ESCO DATA
    # =====================================================

    skills = load_unified_skills()


    for _, row in skills.iterrows():

        skill_id = row["skill_id"]

        name = str(
            row["skill_name"]
        )

        normalized_name = normalize_text(
            name
        )

        if not normalized_name:
            continue


        # -------------------------------------------------
        # Add existing ESCO / O*NET technology name
        # -------------------------------------------------

        if normalized_name not in index:

            index[normalized_name] = {

                "skill_id": skill_id,

                "skill_name": name,

                "source": row["source"],

                "category": row["category"],

                "match_type": "technology"
            }


    # =====================================================
    # 2. LOAD MODERN TECHNOLOGY DATASET
    # =====================================================

    if not TECHNOLOGY_FILE.exists():

        raise FileNotFoundError(
            f"Technology dataset not found: "
            f"{TECHNOLOGY_FILE}"
        )


    modern_df = pd.read_csv(
        TECHNOLOGY_FILE
    )


    # -----------------------------------------------------
    # Validate CSV columns
    # -----------------------------------------------------

    required_columns = {
        "technology",
        "aliases",
        "category"
    }


    missing_columns = (
        required_columns
        - set(modern_df.columns)
    )


    if missing_columns:

        raise ValueError(
            "Missing columns in modern technology "
            f"dataset: {missing_columns}"
        )


    # =====================================================
    # 3. ADD MODERN TECHNOLOGIES
    # =====================================================

    for _, row in modern_df.iterrows():

        technology = str(
            row["technology"]
        ).strip()


        if not technology:
            continue


        normalized_name = normalize_text(
            technology
        )


        if not normalized_name:
            continue


        # -------------------------------------------------
        # Create deterministic technology ID
        #
        # SHA-256 gives us a stable ID.
        # Negative IDs prevent collision with the
        # positive ESCO / O*NET skill IDs.
        # -------------------------------------------------

        hash_value = hashlib.sha256(
            normalized_name.encode("utf-8")
        ).hexdigest()


        technology_id = -(
            int(hash_value[:15], 16)
        )


        # -------------------------------------------------
        # Add canonical technology
        # -------------------------------------------------

        index[normalized_name] = {

            "skill_id": technology_id,

            "skill_name": technology,

            "source": "MODERN_TECH",

            "category": str(
                row["category"]
            ),

            "match_type": "technology"
        }


        # =================================================
        # 4. ADD TECHNOLOGY ALIASES
        # =================================================

        aliases = str(
            row["aliases"]
        )


        if aliases.lower() == "nan":

            aliases = ""


        for alias in aliases.split(";"):

            alias = normalize_text(
                alias
            )


            if not alias:
                continue


            index[alias] = {

                "skill_id": technology_id,

                "skill_name": technology,

                "source": "MODERN_TECH",

                "category": str(
                    row["category"]
                ),

                "match_type": "technology"
            }


    # =====================================================
    # RETURN INDEX
    # =====================================================

    return index