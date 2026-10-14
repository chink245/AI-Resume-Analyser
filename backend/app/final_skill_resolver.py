from app.skill_detector import detect_exact_skills
from app.candidate_extractor import extract_candidates
from app.vector_index import search_skills_batch

import re


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    if not text:
        return ""

    text = str(text).casefold()
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# RESUME CANDIDATE VALIDATION
# ============================================================

def is_valid_candidate(candidate):
    if not candidate:
        return False

    candidate = candidate.strip()

    if len(candidate) < 2:
        return False

    if not re.search(r"[A-Za-z]", candidate):
        return False

    normalized = normalize_text(candidate)

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
        "at",
        "by",
        "from",
        "using",
        "use",
        "used",
        "have",
        "has",
        "had",
        "worked",
        "work",
        "working",
        "building",
        "built",
        "developed",
        "develop",
        "development",
        "experience",
        "experienced",
        "deployed",
        "deployment",
        "applications",
        "application",
        "developer",
        "developers",
        "web",
        "website",
        "websites",
        "software",
        "system",
        "systems",
        "version",
        "control",
        "my",
        "our",
        "this",
        "that",
        "these",
        "those",
        "project",
        "projects",
        "responsible",
        "responsibilities",
        "knowledge",
        "skills",
        "strong",
        "good",
        "excellent",
        "team",
        "teams",
        "including",
        "such",
        "also",
    }

    if normalized in stop_words:
        return False

    return True


# ============================================================
# SEMANTIC RESULTS THAT SHOULD NEVER BECOME RESUME SKILLS
# ============================================================

IGNORED_SEMANTIC_SKILLS = {
    # Generic computer / IT concepts
    "computer programming",
    "computer technology",
    "computer engineering",
    "computer science technology",
    "information technology",
    "information technology systems",
    "computer systems",
    "computer science",
    "computer software",
    "computer applications",

    # Generic software concepts
    "software development",
    "software engineering",
    "web development",
    "application development",
    "software architecture design",
    "architectural design",
    "system architecture design",
    "architectural theory",

    # Generic database concepts
    "database software",
    "digital databases",
    "database systems",
    "database system",
    "database management",
    "database management systems",
    "data extraction software",

    # Generic data-processing concepts
    "data visualisation software",
    "data visualization software",
    "data quality assessment",
    "data cleansing",
    "data cleaning",
    "perform data cleansing",
    "perform data cleaning",
    "process data",
    "processing data",
    "cleaning techniques",
    "perform cleaning duties",

    # Generic workplace / communication concepts
    "personnel management",
    "business communication",
    "written communication",
    "oral communication",
    "google gmail",
    "microsoft outlook",
    "microsoft word",
    "microsoft excel",

    # Generic software/tool concepts
    "salesforce software",
    "java (computer programming)",
    "machine tools",
    "client system",
    "hardware platforms",
    "debuggers",
    "troubleshooting software",

    # Generic actions
    "operate scanner",
    "operate printers",
    "operate printer",
    "use databases",
    "use object oriented programming",
    "object oriented programming",

    # Garbage / low-value semantic results
    "real pro",
}


# ============================================================
# TECHNOLOGY SKILLS
# ============================================================

TECHNOLOGY_SKILLS = {
    "javascript",
    "typescript",
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "react",
    "next.js",
    "vue",
    "angular",
    "node.js",
    "express.js",
    "mongodb",
    "postgresql",
    "mysql",
    "sql",
    "docker",
    "kubernetes",
    "git",
    "github",
    "gitlab",
    "aws",
    "azure",
    "gcp",
    "html",
    "css",
    "postman",
    "django",
    "flask",
    "restful api",
}


# ============================================================
# GENERIC SEMANTIC CONCEPTS
# ============================================================

GENERIC_SEMANTIC_TERMS = {
    "computer programming",
    "computer technology",
    "computer engineering",
    "computer science",
    "information technology",
    "computer systems",
    "software development",
    "software engineering",
    "web development",
    "application development",
    "database software",
    "database systems",
    "database management",
    "data processing",
    "data extraction",
    "data cleaning",
    "data visualization",
}


# ============================================================
# CONTROLLED RELATED CONCEPTS
# ============================================================

RELATED_CONCEPTS = {
    "debug software": {
        "troubleshoot",
        "error handling",
        "debugging",
        "debug",
    },

    "troubleshoot": {
        "debug software",
        "debugging",
        "debug",
        "error handling",
    },

    "debugging": {
        "debug software",
        "troubleshoot",
        "debug",
        "error handling",
    },

    "debug": {
        "debug software",
        "troubleshoot",
        "debugging",
        "error handling",
    },

    "error handling": {
        "debug software",
        "troubleshoot",
        "debugging",
        "debug",
    },
}


# ============================================================
# BASIC HELPERS
# ============================================================

def get_existing_skill_names(detected):
    return {
        normalize_text(skill["skill"])
        for skill in detected.values()
    }


def skill_already_detected(detected, skill_name):
    normalized_name = normalize_text(skill_name)

    for existing in detected.values():
        existing_name = normalize_text(existing["skill"])

        if existing_name == normalized_name:
            return True

    return False


# ============================================================
# SEMANTIC FILTERING
# ============================================================

def should_ignore_semantic_skill(skill_name, detected):
    normalized_skill = normalize_text(skill_name)

    # Direct blacklist
    if normalized_skill in IGNORED_SEMANTIC_SKILLS:
        return True

    # Generic semantic concepts
    if normalized_skill in GENERIC_SEMANTIC_TERMS:
        return True

    existing_skills = get_existing_skill_names(detected)

    # --------------------------------------------------------
    # Prevent duplicate technology concepts
    # --------------------------------------------------------

    # Python -> Python (computer programming)
    if (
        normalized_skill == "python (computer programming)"
        and "python" in existing_skills
    ):
        return True

    if normalized_skill == "python programming" and "python" in existing_skills:
        return True

    # Java -> Java (computer programming)
    if (
        normalized_skill == "java (computer programming)"
        and "java" in existing_skills
    ):
        return True

    # JavaScript -> JavaScript programming
    if (
        normalized_skill in {
            "javascript programming",
            "javascript (programming language)",
        }
        and "javascript" in existing_skills
    ):
        return True

    # --------------------------------------------------------
    # Version control duplication
    # --------------------------------------------------------

    if normalized_skill in {
        "version control software",
        "revision control software",
    }:
        if "git" in existing_skills or "github" in existing_skills:
            return True

    # --------------------------------------------------------
    # Database generic concepts
    # --------------------------------------------------------

    if normalized_skill in {
        "use databases",
        "database management",
        "database management systems",
        "database systems",
        "database system",
        "database software",
    }:
        database_skills = {
            "mongodb",
            "nosql",
            "postgresql",
            "mysql",
            "sql",
            "oracle",
            "redis",
            "database",
        }

        if existing_skills.intersection(database_skills):
            return True

    # --------------------------------------------------------
    # Generic OOP concept
    # --------------------------------------------------------

    if normalized_skill in {
        "use object oriented programming",
        "object oriented programming",
    }:
        programming_skills = {
            "javascript",
            "typescript",
            "python",
            "java",
            "c",
            "c++",
            "c#",
        }

        if existing_skills.intersection(programming_skills):
            return True

    # --------------------------------------------------------
    # Generic software development terms
    # --------------------------------------------------------

    if normalized_skill in {
        "software development",
        "software engineering",
        "web development",
        "application development",
    }:
        if existing_skills:
            return True

    return False


# ============================================================
# SEMANTIC RESULT QUALITY CHECK
# ============================================================

def is_good_semantic_result(result, detected):
    if not result:
        return False

    skill_name = result.get("skill", "")

    if not skill_name:
        return False

    normalized_skill = normalize_text(skill_name)

    similarity = float(result.get("similarity", 0))

    # Keep semantic matching strict
    if similarity < 0.82:
        return False

    # Never add known noise
    if should_ignore_semantic_skill(skill_name, detected):
        return False

    # Do not add technology names through semantic matching
    # when they should normally come from exact detection.
    if normalized_skill in TECHNOLOGY_SKILLS:
        return False

    return True


# ============================================================
# SELECT BEST SEMANTIC RESULT
# ============================================================

def select_best_semantic_result(results, detected):
    if not results:
        return None

    for result in results:

        if not is_good_semantic_result(result, detected):
            continue

        skill_name = normalize_text(result.get("skill", ""))

        # Never accept generic semantic concepts
        if skill_name in GENERIC_SEMANTIC_TERMS:
            continue

        # Never accept technology skills through semantic matching
        if skill_name in TECHNOLOGY_SKILLS:
            continue

        return result

    return None


# ============================================================
# RESOLVE RESUME SKILLS
# ============================================================

def resolve_resume_skills(resume_text):
    detected = {}

    print("\n========== EXTRACTED RESUME TEXT ==========")
    print(resume_text)
    print("===========================================\n")
    # ========================================================
    # STEP 1: EXACT SKILLS
    # ========================================================

    exact_results = detect_exact_skills(resume_text)

    print("\n========== EXACT DETECTION DEBUG ==========")

    for skill in exact_results:
        print(
            skill.get("skill"),
            "|",
            skill.get("skill_id"),
            "|",
            skill.get("match_type")
        )

    print("===========================================\n")

    for skill in exact_results:
        skill_id = int(skill["skill_id"])
        detected[skill_id] = skill

    # ========================================================
    # STEP 2: EXTRACT POSSIBLE RESUME CANDIDATES
    # ========================================================

    candidates = extract_candidates(resume_text)

    valid_candidates = []
    seen_candidates = set()

    for candidate in candidates:

        if not is_valid_candidate(candidate):
            continue

        normalized = normalize_text(candidate)

        if normalized in seen_candidates:
            continue

        seen_candidates.add(normalized)
        valid_candidates.append(candidate)

    if not valid_candidates:
        return list(detected.values())

    # ========================================================
    # STEP 3: SEMANTIC SEARCH
    # ========================================================

    semantic_results = search_skills_batch(
        valid_candidates,
        top_k=3,
        min_similarity=0.82
    )

    # ========================================================
    # STEP 4: ACCEPT ONLY HIGH-QUALITY SEMANTIC SKILLS
    # ========================================================

    for query_result in semantic_results:

        results = query_result.get("results", [])

        if not results:
            continue

        result = select_best_semantic_result(
            results,
            detected
        )

        if result is None:
            continue

        skill_id = int(result["skill_id"])
        skill_name = result["skill"]

        if skill_id in detected:
            continue

        if skill_already_detected(detected, skill_name):
            continue

        if should_ignore_semantic_skill(
            skill_name,
            detected
        ):
            continue

        detected[skill_id] = {
            "skill_id": skill_id,
            "skill": skill_name,
            "source": result["source"],
            "category": result["category"],
            "match_type": "semantic",
            "confidence": round(
                float(result["similarity"]),
                4
            ),
        }

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return list(detected.values())
    
    detected = {}

    # ========================================================
    # STEP 1: EXACT SKILLS
    # ========================================================

    exact_results = detect_exact_skills(resume_text)

    for skill in exact_results:
        skill_id = int(skill["skill_id"])
        detected[skill_id] = skill

    # ========================================================
    # STEP 2: EXTRACT POSSIBLE RESUME CANDIDATES
    # ========================================================

    candidates = extract_candidates(resume_text)

    valid_candidates = []
    seen_candidates = set()

    for candidate in candidates:

        if not is_valid_candidate(candidate):
            continue

        normalized = normalize_text(candidate)

        if normalized in seen_candidates:
            continue

        seen_candidates.add(normalized)
        valid_candidates.append(candidate)

    if not valid_candidates:
        return list(detected.values())

    # ========================================================
    # STEP 3: SEMANTIC SEARCH
    # ========================================================

    semantic_results = search_skills_batch(
        valid_candidates,
        top_k=3,
        min_similarity=0.82
    )

    # ========================================================
    # STEP 4: ACCEPT ONLY HIGH-QUALITY SEMANTIC SKILLS
    # ========================================================

    for query_result in semantic_results:

        results = query_result.get("results", [])

        if not results:
            continue

        result = select_best_semantic_result(
            results,
            detected
        )

        if result is None:
            continue

        skill_id = int(result["skill_id"])
        skill_name = result["skill"]

        # ----------------------------------------------------
        # Already detected by ID
        # ----------------------------------------------------

        if skill_id in detected:
            continue

        # ----------------------------------------------------
        # Already detected by name
        # ----------------------------------------------------

        if skill_already_detected(detected, skill_name):
            continue

        # ----------------------------------------------------
        # Final safety check
        # ----------------------------------------------------

        if should_ignore_semantic_skill(
            skill_name,
            detected
        ):
            continue

        # ----------------------------------------------------
        # Add semantic skill
        # ----------------------------------------------------

        detected[skill_id] = {
            "skill_id": skill_id,
            "skill": skill_name,
            "source": result["source"],
            "category": result["category"],
            "match_type": "semantic",
            "confidence": round(
                float(result["similarity"]),
                4
            ),
        }

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return list(detected.values())