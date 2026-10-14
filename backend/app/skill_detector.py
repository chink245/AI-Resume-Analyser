from app.unified_skill_loader import load_unified_skills
from app.skill_alias_index import build_alias_index
from app.technology_index import build_technology_index
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

    # -----------------------------------------------------
    # Fix PDF extraction artifacts around technology names
    #
    # Examples:
    #
    # Node . js       -> Node.js
    # React . js      -> React.js
    # Express . js    -> Express.js
    # Next . js       -> Next.js
    # TypeScript . js -> TypeScript.js
    # -----------------------------------------------------

    text = re.sub(
        r"\b([a-z0-9+#]+)\s*\.\s*(js|jsx|ts|tsx)\b",
        r"\1.\2",
        text,
        flags=re.IGNORECASE
    )

    # -----------------------------------------------------
    # Normalize common separators
    # -----------------------------------------------------

    text = text.replace("-", " ")
    text = text.replace("_", " ")

    # -----------------------------------------------------
    # Normalize extra whitespace
    # -----------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# PDF WORD-CONCATENATION ARTIFACTS
# =========================================================

#
# PDF text extraction can sometimes remove spaces between
# words.
#
# Examples:
#
# Gitversioncontrol  -> Git version control
# JWTAAuthentication -> JWT authentication
# RESTAPI            -> REST API
# CRUDOperations     -> CRUD Operations
#
# Only highly reliable technology-related cases are handled.
# =========================================================

def normalize_pdf_artifacts(text):

    if not text:
        return ""

    text = str(text).casefold()

    replacements = {

        "gitversioncontrol":
            "git version control",

        "jwtauthentication":
            "jwt authentication",

        "restapi":
            "rest api",

        "restapis":
            "rest apis",

        "apidesign":
            "api design",

        "crudoperations":
            "crud operations",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    return text


# =========================================================
# VALID SKILL CHECK
# =========================================================

#
# Prevent low-quality entries from being detected.
#
# Example:
#
# J       ❌
# C       ❌
# A       ❌
#
# But:
#
# JavaScript  ✅
# React       ✅
# AWS         ✅
# SQL         ✅
#
# =========================================================

INVALID_SKILL_NAMES = {

    "j",
    "c",
    "r",
    "go",
    "a",
    "an",
    "the"
}


def is_valid_skill_name(skill_name):

    if not skill_name:
        return False

    normalized = normalize_text(
        skill_name
    )

    # -----------------------------------------------------
    # Reject extremely short skill names
    # -----------------------------------------------------

    if len(normalized) < 2:
        return False

    # -----------------------------------------------------
    # Reject known invalid names
    # -----------------------------------------------------

    if normalized in INVALID_SKILL_NAMES:
        return False

    # -----------------------------------------------------
    # Must contain at least one alphabet
    # -----------------------------------------------------

    if not re.search(
        r"[a-z]",
        normalized
    ):
        return False

    return True


# =========================================================
# SOFT SKILL CLASSIFICATION
# =========================================================

#
# Some knowledge-base entries may classify soft skills
# simply as "skill".
#
# We explicitly classify known soft skills here so that
# analysis_service.py can handle them differently from
# technical skills.
#
# =========================================================

SOFT_SKILLS = {

    "communication",
    "teamwork",
    "collaboration",
    "leadership",
    "problem solving",
    "time management",
    "adaptability",
    "critical thinking",
    "interpersonal skills",
}


def get_skill_category(
    skill_name,
    original_category
):

    normalized_skill = normalize_text(
        skill_name
    )

    normalized_soft_skills = {

        normalize_text(skill)

        for skill in SOFT_SKILLS
    }

    if normalized_skill in normalized_soft_skills:

        return "soft_skill"

    return original_category


# =========================================================
# PHRASE MATCHING
# =========================================================

def phrase_exists(
    text,
    phrase
):

    if not phrase:
        return False

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
# CHECK WHETHER SKILL ALREADY EXISTS
# =========================================================

def skill_already_detected(
    detected,
    skill_name
):

    normalized_name = normalize_text(
        skill_name
    )

    for existing in detected.values():

        existing_name = normalize_text(
            existing["skill"]
        )

        if existing_name == normalized_name:

            return True

    return False


# =========================================================
# DETECT SKILLS
# =========================================================

def detect_exact_skills(
    resume_text
):

    # =====================================================
    # 0. NORMALIZE PDF TEXT BEFORE SKILL MATCHING
    # =====================================================

    text = normalize_pdf_artifacts(
        resume_text
    )

    text = normalize_text(
        text
    )

    detected = {}


    # =====================================================
    # 1. EXACT CANONICAL SKILL MATCH
    # =====================================================

    for _, row in skills_df.iterrows():

        skill_name = str(
            row["skill_name"]
        )

        # -------------------------------------------------
        # Ignore invalid / noisy skill names
        # -------------------------------------------------

        if not is_valid_skill_name(
            skill_name
        ):
            continue

        normalized_skill = normalize_text(
            skill_name
        )

        if not normalized_skill:
            continue

        if not phrase_exists(
            text,
            normalized_skill
        ):
            continue

        skill_id = int(
            row["skill_id"]
        )

        # -------------------------------------------------
        # EXACT MATCH HAS HIGHEST PRIORITY
        # -------------------------------------------------

        if skill_already_detected(
            detected,
            skill_name
        ):
            continue

        detected[skill_id] = {

            "skill_id":
                skill_id,

            "skill":
                skill_name,

            "source":
                row["source"],

            "category":
                get_skill_category(
                    skill_name,
                    row["category"]
                ),

            "match_type":
                "exact",

            "confidence":
                1.0
        }


    # =====================================================
    # 2. ALIAS MATCH
    # =====================================================

    for alias, skill_id in alias_index.items():

        alias = normalize_text(
            alias
        )

        if not alias:
            continue

        if not phrase_exists(
            text,
            alias
        ):
            continue

        # -------------------------------------------------
        # Find canonical skill
        # -------------------------------------------------

        skill_rows = skills_df[
            skills_df["skill_id"] == skill_id
        ]

        if skill_rows.empty:
            continue

        row = skill_rows.iloc[0]

        skill_name = str(
            row["skill_name"]
        )

        # -------------------------------------------------
        # Ignore invalid skill names
        # -------------------------------------------------

        if not is_valid_skill_name(
            skill_name
        ):
            continue

        # -------------------------------------------------
        # Don't overwrite exact match
        # -------------------------------------------------

        if skill_already_detected(
            detected,
            skill_name
        ):
            continue

        detected[int(skill_id)] = {

            "skill_id":
                int(skill_id),

            "skill":
                skill_name,

            "source":
                row["source"],

            "category":
                get_skill_category(
                    skill_name,
                    row["category"]
                ),

            "match_type":
                "alias",

            "confidence":
                0.95
        }


    # =====================================================
    # 3. MODERN / O*NET TECHNOLOGY MATCH
    # =====================================================

    for term, information in technology_index.items():

        term = normalize_text(
            term
        )

        if not term:
            continue

        if not phrase_exists(
            text,
            term
        ):
            continue

        skill_name = str(
            information["skill_name"]
        )

        # -------------------------------------------------
        # Ignore invalid technology names
        # -------------------------------------------------

        if not is_valid_skill_name(
            skill_name
        ):
            continue

        # -------------------------------------------------
        # Don't add technology if the same skill was
        # already detected by exact or alias matching.
        #
        # Example:
        #
        # React -> exact
        # React -> technology
        #
        # Keep only:
        #
        # React -> exact
        # -------------------------------------------------

        if skill_already_detected(
            detected,
            skill_name
        ):
            continue

        skill_id = information[
            "skill_id"
        ]

        detected[int(skill_id)] = {

            "skill_id":
                int(skill_id),

            "skill":
                skill_name,

            "source":
                information["source"],

            "category":
                get_skill_category(
                    skill_name,
                    information["category"]
                ),

            "match_type":
                "technology",

            "confidence":
                0.90
        }


    # =====================================================
    # RETURN RESULTS
    # =====================================================

    return list(
        detected.values()
    )