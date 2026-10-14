from app.final_skill_resolver import resolve_resume_skills
from app.jd_skill_extractor import extract_jd_skills


def normalize_skill_name(skill):
    if not skill:
        return ""
    return (
        str(skill).strip().casefold()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace(".", "")
    )


RELATED_SKILL_MAP = {
    "troubleshoot": [
        "troubleshooting",
        "troubleshooting skills",
        "debugging",
        "error handling",
        "error-handling",
        "debug software"
    ],
    "nosql": ["mongodb"],
}


def find_related_skill(job_skill_name, resume_text):
    normalized_job_skill = normalize_skill_name(job_skill_name)

    related_terms = RELATED_SKILL_MAP.get(normalized_job_skill, [])

    normalized_resume_text = normalize_skill_name(resume_text)

    for term in related_terms:
        normalized_term = normalize_skill_name(term)

        if normalized_term in normalized_resume_text:
            return term

    return None


SOFT_SKILLS = {
    "communication",
    "teamwork",
    "collaboration",
    "leadership",
    "problem solving",
    "time management",
}


SOFT_SKILL_EVIDENCE = {
    "communication": [
        "communication",
        "communicated",
        "presentation",
        "presented",
        "presentations",
        "client interaction",
        "client communication",
        "team collaboration",
        "collaborated",
        "collaboration",
        "teamwork",
    ],

    "teamwork": [
        "teamwork",
        "team collaboration",
        "collaborated",
        "collaboration",
        "worked with a team",
        "team member",
    ],

    "collaboration": [
        "collaboration",
        "collaborated",
        "teamwork",
        "worked with a team",
        "team member",
    ],

    "leadership": [
        "leadership",
        "led",
        "leading",
        "managed a team",
        "team lead",
    ],

    "problem solving": [
        "problem solving",
        "problem-solving",
        "solved problems",
        "debugging",
        "troubleshooting",
    ],

    "time management": [
        "time management",
        "managed deadlines",
        "met deadlines",
        "deadline",
    ],
}


def find_soft_skill_evidence(job_skill_name, resume_text):

    normalized_job_skill = normalize_skill_name(job_skill_name)

    normalized_soft_skills = {
        normalize_skill_name(skill)
        for skill in SOFT_SKILLS
    }

    if normalized_job_skill not in normalized_soft_skills:
        return None

    evidence_terms = []

    for skill_name, terms in SOFT_SKILL_EVIDENCE.items():

        if normalize_skill_name(skill_name) == normalized_job_skill:
            evidence_terms = terms
            break

    if not evidence_terms:
        return None

    normalized_resume_text = normalize_skill_name(resume_text)

    for term in evidence_terms:

        normalized_term = normalize_skill_name(term)

        if normalized_term in normalized_resume_text:
            return term

    return None


def create_skill_name_map(skills):

    skill_map = {}

    for skill in skills:

        name = normalize_skill_name(
            skill.get("skill")
        )

        if not name:
            continue

        skill_map[name] = skill

    return skill_map


def create_unique_skill_list(skills):

    unique_skills = []
    seen = set()

    for skill in skills:

        skill_name = skill.get("skill")

        normalized_name = normalize_skill_name(
            skill_name
        )

        if not normalized_name:
            continue

        if normalized_name in seen:
            continue

        seen.add(normalized_name)

        unique_skills.append(skill)

    return unique_skills


def create_improvement_suggestions(missing_skills):

    suggestions = []

    for skill in missing_skills:

        skill_name = skill.get("skill")

        if not skill_name:
            continue

        category = skill.get(
            "jd_category",
            skill.get("category", "skill")
        )

        if category in [
            "skill",
            "technology",
            "technical_skill",
            "technical_skills",
            "tool",
            "tools",
            "programming_language",
            "programming_languages"
        ]:

            suggestions.append(
                f"Add {skill_name} to your resume if you have experience with it. "
                f"If you have not learned it, consider building a small project "
                f"or gaining practical experience with {skill_name}."
            )

        elif category in ["soft_skill", "soft_skills"]:

            suggestions.append(
                f"Show evidence of {skill_name} in your resume through "
                f"project work, teamwork, achievements, or relevant experience."
            )

        elif category in [
            "education",
            "qualification",
            "degree"
        ]:

            suggestions.append(
                f"Check whether you meet the requirement '{skill_name}'. "
                f"If you do, clearly mention the relevant qualification "
                f"in your resume."
            )

        elif category in [
            "experience",
            "work_experience"
        ]:

            suggestions.append(
                f"If you have experience related to {skill_name}, "
                f"mention it clearly in your resume with specific "
                f"responsibilities or achievements."
            )

        else:

            suggestions.append(
                f"Review the requirement '{skill_name}' and add "
                f"relevant evidence to your resume if you already "
                f"have this experience."
            )

    return suggestions


# ============================================================
# NEW: GROUP MISSING REQUIREMENTS BY CATEGORY
# ============================================================

def categorize_missing_requirements(missing_skill_objects):

    categorized = {
        "technical_skills": [],
        "soft_skills": [],
        "education": [],
        "experience": [],
        "tools": [],
        "other": []
    }

    for skill in missing_skill_objects:

        skill_name = skill.get("skill")

        if not skill_name:
            continue

        category = skill.get(
            "jd_category",
            skill.get("category", "skill")
        )

        category = (
            str(category)
            .casefold()
            .strip()
            .replace("-", "_")
            .replace(" ", "_")
        )

        if category in [
            "skill",
            "technical_skill",
            "technical_skills",
            "technology",
            "programming_language",
            "programming_languages"
        ]:

            categorized["technical_skills"].append(
                skill_name
            )

        elif category in ["soft_skill", "soft_skills"]:

            categorized["soft_skills"].append(
                skill_name
            )

        elif category in [
            "education",
            "qualification",
            "degree"
        ]:

            categorized["education"].append(
                skill_name
            )

        elif category in [
            "experience",
            "work_experience"
        ]:

            categorized["experience"].append(
                skill_name
            )

        elif category in [
            "tool",
            "tools"
        ]:

            categorized["tools"].append(
                skill_name
            )

        else:

            categorized["other"].append(
                skill_name
            )

    return categorized


def analyze_resume_vs_job(
    resume_text,
    job_description
):

    resume_skills = resolve_resume_skills(
        resume_text
    )

    if not resume_skills:
        resume_skills = []

    job_skills = extract_jd_skills(
        job_description
    )

    if not job_skills:
        job_skills = []

    resume_skills = create_unique_skill_list(
        resume_skills
    )

    job_skills = create_unique_skill_list(
        job_skills
    )

    resume_name_map = create_skill_name_map(
        resume_skills
    )

    matched_skill_names = set()

    missing_skill_objects = []

    related_matches = []

    for job_skill in job_skills:

        job_skill_name = job_skill.get(
            "skill"
        )

        normalized_job_name = normalize_skill_name(
            job_skill_name
        )

        if not normalized_job_name:
            continue

        if normalized_job_name in resume_name_map:

            matched_skill_names.add(
                normalized_job_name
            )

            continue

        soft_skill_evidence = find_soft_skill_evidence(
            job_skill_name,
            resume_text
        )

        if soft_skill_evidence:

            related_matches.append({
                "job_skill": job_skill_name,
                "resume_evidence": soft_skill_evidence,
                "match_type": "soft_skill",
                "score": 0.5
            })

            continue

        related_skill = find_related_skill(
            job_skill_name,
            resume_text
        )

        if related_skill:

            related_matches.append({
                "job_skill": job_skill_name,
                "resume_evidence": related_skill,
                "match_type": "related",
                "score": 0.5
            })

            continue

        missing_skill_objects.append(
            job_skill
        )

    matched_skills = []

    matched_seen = set()

    for job_skill in job_skills:

        skill_name = job_skill.get(
            "skill"
        )

        normalized_name = normalize_skill_name(
            skill_name
        )

        if not normalized_name:
            continue

        if normalized_name in matched_skill_names:

            if normalized_name not in matched_seen:

                matched_seen.add(
                    normalized_name
                )

                matched_skills.append(
                    skill_name
                )

    missing_skills = []

    missing_seen = set()

    for skill in missing_skill_objects:

        skill_name = skill.get(
            "skill"
        )

        normalized_name = normalize_skill_name(
            skill_name
        )

        if not normalized_name:
            continue

        if normalized_name in missing_seen:
            continue

        missing_seen.add(
            normalized_name
        )

        missing_skills.append(
            skill_name
        )

    total_required = len(job_skills)

    total_matched = len(
        matched_skill_names
    )

    total_related = len(
        related_matches
    )

    exact_score = total_matched * 1.0

    related_score = total_related * 0.5

    weighted_score = (
        exact_score +
        related_score
    )

    if total_required == 0:

        match_percentage = 0.0

    else:

        match_percentage = round(
            (weighted_score / total_required) * 100,
            2
        )

    improvement_suggestions = (
        create_improvement_suggestions(
            missing_skill_objects
        )
    )

    # ========================================================
    # NEW: CREATE CATEGORY-WISE MISSING REQUIREMENTS
    # ========================================================

    missing_by_category = categorize_missing_requirements(
        missing_skill_objects
    )

    return {

        "match_percentage":
            match_percentage,

        "total_required":
            total_required,

        "total_matched":
            total_matched,

        "total_missing":
            len(missing_skills),

        "total_related":
            total_related,

        "exact_score":
            exact_score,

        "related_score":
            related_score,

        "weighted_score":
            weighted_score,

        "matched_skills":
            matched_skills,

        "related_matches":
            related_matches,

        "missing_skills":
            missing_skills,

        # NEW
        "missing_by_category":
            missing_by_category,

        "improvement_suggestions":
            improvement_suggestions,

        "resume_skills":
            resume_skills,

        "job_skills":
            job_skills
    }