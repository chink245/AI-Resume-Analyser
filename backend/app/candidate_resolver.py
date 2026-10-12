from candidate_extractor import extract_candidates
from vector_index import search_skills
from unified_skill_loader import load_unified_skills
from skill_alias_index import build_alias_index
from technology_index import build_technology_index

import re


# =========================================================
# LOAD KNOWLEDGE BASE
# =========================================================

skills_df = load_unified_skills()

alias_index = build_alias_index()

technology_index = build_technology_index()


# =========================================================
# NORMALIZATION
# =========================================================

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


# =========================================================
# PHRASE MATCHING
# =========================================================

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


# =========================================================
# CANDIDATE FILTER
# =========================================================

def is_valid_candidate(candidate):

    candidate = candidate.strip()

    if not candidate:
        return False

    if len(candidate) < 2:
        return False

    if not re.search(
        r"[A-Za-z]",
        candidate
    ):
        return False

    stop_words = {

        "i",
        "am",
        "a",
        "an",
        "the",
        "and",
        "or",
        "with",
        "for",
        "to",
        "of",
        "in",
        "on",
        "using",
        "use",
        "have",
        "has",
        "had",
        "worked",
        "work",
        "building",
        "built",
        "developed",
        "develop",
        "experience",
        "deployed",
        "applications",
        "application",
        "developer",
        "web",
        "version",
        "control"
    }

    normalized = normalize_text(
        candidate
    )

    if normalized in stop_words:
        return False

    return True


# =========================================================
# RESOLVE CANDIDATE
# =========================================================

def resolve_candidate(
    candidate,
    detected
):

    normalized_candidate = normalize_text(
        candidate
    )


    # =====================================================
    # 1. EXACT MATCH
    # =====================================================

    exact_matches = skills_df[
        skills_df["normalized_name"]
        == normalized_candidate
    ]

    for _, row in exact_matches.iterrows():

        skill_id = int(
            row["skill_id"]
        )

        if skill_id not in detected:

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

        return


    # =====================================================
    # 2. ALIAS MATCH
    # =====================================================

    if normalized_candidate in alias_index:

        skill_id = alias_index[
            normalized_candidate
        ]

        skill = skills_df[
            skills_df["skill_id"] == skill_id
        ]

        if not skill.empty:

            row = skill.iloc[0]

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

            return


    # =====================================================
    # 3. TECHNOLOGY MATCH
    # =====================================================

    if normalized_candidate in technology_index:

        information = technology_index[
            normalized_candidate
        ]

        skill_id = information[
            "skill_id"
        ]

        if skill_id not in detected:

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

        return


    # =====================================================
    # 4. SEMANTIC MATCH
    # =====================================================

    # Semantic matching is used only when the candidate
    # was not found by exact, alias, or technology matching.

    results = search_skills(
        candidate,
        top_k=3,
        min_similarity=0.78
    )

    if not results:
        return

    best = results[0]

    similarity = float(
        best["similarity"]
    )

    # -----------------------------------------------------
    # Require strong semantic similarity
    # -----------------------------------------------------

    if similarity < 0.78:
        return

    skill_id = best[
        "skill_id"
    ]

    # -----------------------------------------------------
    # Don't duplicate an already detected skill
    # -----------------------------------------------------

    if skill_id in detected:
        return

    # -----------------------------------------------------
    # Avoid generic software categories becoming skills
    # -----------------------------------------------------

    generic_categories = {

        "software",

        "software development",

        "web development",

        "web application",

        "web application software",

        "application software",

        "programming",

        "database management",

        "version control"
    }

    category = normalize_text(
        best["category"]
    )

    if category in generic_categories:
        return
    # =====================================================
    # 4. SEMANTIC MATCH
    # =====================================================

    results = search_skills(
        candidate,
        top_k=3,
        min_similarity=0.78
    )

    if not results:
        return


    best = results[0]


    similarity = float(
        best["similarity"]
    )


    # -----------------------------------------------------
    # Strong similarity required
    # -----------------------------------------------------

    if similarity < 0.78:
        return


    skill_id = best[
        "skill_id"
    ]


    # -----------------------------------------------------
    # Don't duplicate existing skills
    # -----------------------------------------------------

    if skill_id in detected:
        return


    candidate_normalized = normalize_text(
        candidate
    )

    skill_normalized = normalize_text(
        best["skill"]
    )


    # -----------------------------------------------------
    # Reject semantic expansions
    #
    # Example:
    #
    # "version control"
    #      ->
    # "version control software"
    #
    # This isn't a new skill.
    # -----------------------------------------------------

    if (
        candidate_normalized in skill_normalized
        and
        len(skill_normalized) >
        len(candidate_normalized)
    ):

        extra_words = (
            skill_normalized
            .replace(
                candidate_normalized,
                ""
            )
            .strip()
        )


        if len(
            extra_words.split()
        ) <= 2:

            return


    # -----------------------------------------------------
    # Store semantic result
    # -----------------------------------------------------

    detected[skill_id] = {

        "skill_id": skill_id,

        "skill": best[
            "skill"
        ],

        "source": best[
            "source"
        ],

        "category": best[
            "category"
        ],

        "match_type": "semantic",

        "confidence": round(
            similarity,
            4
        )
    }

# =========================================================
# MAIN RESOLVER
# =========================================================

def resolve_resume_candidates(
    resume_text
):

    candidates = extract_candidates(
        resume_text
    )

    detected = {}

    for candidate in candidates:

        if not is_valid_candidate(
            candidate
        ):
            continue

        resolve_candidate(
            candidate,
            detected
        )

    return list(
        detected.values()
    )