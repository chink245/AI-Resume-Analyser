from unified_skill_loader import load_unified_skills
from skill_alias_index import build_alias_index
from technology_index import build_technology_index
from vector_index import search_skills

import re


# ---------------------------------------------------------
# Load knowledge base once
# ---------------------------------------------------------

skills_df = load_unified_skills()

alias_index = build_alias_index()

technology_index = build_technology_index()


# ---------------------------------------------------------
# Text normalization
# ---------------------------------------------------------

def normalize_text(text):

    if not text:
        return ""

    text = str(text).casefold()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ---------------------------------------------------------
# Phrase matching
# ---------------------------------------------------------

def phrase_exists(text, phrase):

    pattern = (
        r"(?<!\w)"
        + re.escape(phrase)
        + r"(?!\w)"
    )

    return bool(
        re.search(
            pattern,
            text
        )
    )


# ---------------------------------------------------------
# Main Resume Skill Detector
# ---------------------------------------------------------

def analyze_resume_skills(resume_text):

    text = normalize_text(
        resume_text
    )

    detected = {}


    # =====================================================
    # 1. EXACT CANONICAL SKILL MATCHING
    # =====================================================

    for _, row in skills_df.iterrows():

        skill_name = row["skill_name"]

        normalized_skill = normalize_text(
            skill_name
        )

        if not normalized_skill:
            continue

        if phrase_exists(
            text,
            normalized_skill
        ):

            skill_id = int(
                row["skill_id"]
            )

            detected[skill_id] = {

                "skill_id": skill_id,

                "skill": row[
                    "skill_name"
                ],

                "source": row[
                    "source"
                ],

                "category": row[
                    "category"
                ],

                "match_type": "exact",

                "confidence": 1.0
            }


    # =====================================================
    # 2. ALIAS MATCHING
    # =====================================================

    for alias, skill_id in alias_index.items():

        if phrase_exists(
            text,
            alias
        ):

            skill = skills_df[
                skills_df["skill_id"] == skill_id
            ]

            if skill.empty:
                continue

            row = skill.iloc[0]


            # Do not overwrite exact match

            if skill_id not in detected:

                detected[skill_id] = {

                    "skill_id": int(
                        skill_id
                    ),

                    "skill": row[
                        "skill_name"
                    ],

                    "source": row[
                        "source"
                    ],

                    "category": row[
                        "category"
                    ],

                    "match_type": "alias",

                    "confidence": 0.95
                }


    # =====================================================
    # 3. TECHNOLOGY MATCHING
    # =====================================================

    for term, information in technology_index.items():

        if phrase_exists(
            text,
            term
        ):

            skill_id = information[
                "skill_id"
            ]


            # Do not overwrite exact/alias

            if skill_id in detected:
                continue


            detected[skill_id] = {

                "skill_id": int(
                    skill_id
                ),

                "skill": information[
                    "skill_name"
                ],

                "source": information[
                    "source"
                ],

                "category": information[
                    "category"
                ],

                "match_type": "technology",

                "confidence": 0.90
            }


    # =====================================================
    # 4. SEMANTIC MATCHING
    # =====================================================

    # Split resume into sentences.
    #
    # We do NOT send the entire resume as one query.
    # Each sentence can describe a different skill.

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )


    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue


        # -------------------------------------------------
        # Search FAISS
        # -------------------------------------------------

        semantic_results = search_skills(
            sentence,
            top_k=5,
            min_similarity=0.60
        )


        # -------------------------------------------------
        # Add semantic candidates
        # -------------------------------------------------

        for result in semantic_results:

            skill_id = result[
                "skill_id"
            ]


            # -------------------------------------------------
            # IMPORTANT:
            #
            # Exact, alias and technology matches
            # always have priority.
            # -------------------------------------------------

            if skill_id in detected:
                continue


            detected[skill_id] = {

                "skill_id": skill_id,

                "skill": result[
                    "skill"
                ],

                "source": result[
                    "source"
                ],

                "category": result[
                    "category"
                ],

                "match_type": "semantic",

                "confidence": round(
                    result[
                        "similarity"
                    ],
                    4
                )
            }


    # =====================================================
    # RETURN RESULTS
    # =====================================================

    return list(
        detected.values()
    )