from final_skill_resolver import resolve_resume_skills
from jd_skill_extractor import extract_jd_skills


# =========================================================
# NORMALIZE SKILL NAME
# =========================================================

def normalize_skill(skill):

    return (
        str(skill)
        .strip()
        .casefold()
    )


# =========================================================
# MATCH RESUME WITH JOB DESCRIPTION
# =========================================================

def match_resume_with_jd(
    resume_text,
    job_description
):

    # -----------------------------------------------------
    # Extract resume skills
    # -----------------------------------------------------

    resume_skills = resolve_resume_skills(
        resume_text
    )


    # -----------------------------------------------------
    # Extract JD skills
    # -----------------------------------------------------

    jd_skills = extract_jd_skills(
        job_description
    )


    # -----------------------------------------------------
    # Create lookup sets
    # -----------------------------------------------------

    resume_skill_names = {

        normalize_skill(
            skill["skill"]
        )

        for skill in resume_skills
    }


    jd_skill_names = {

        normalize_skill(
            skill["skill"]
        )

        for skill in jd_skills
    }


    # -----------------------------------------------------
    # Find matched skills
    # -----------------------------------------------------

    matched_skills = []

    for skill in jd_skills:

        skill_name = normalize_skill(
            skill["skill"]
        )

        if skill_name in resume_skill_names:

            matched_skills.append(
                skill
            )


    # -----------------------------------------------------
    # Find missing skills
    # -----------------------------------------------------

    missing_skills = []

    for skill in jd_skills:

        skill_name = normalize_skill(
            skill["skill"]
        )

        if skill_name not in resume_skill_names:

            missing_skills.append(
                skill
            )


    # -----------------------------------------------------
    # Calculate match percentage
    # -----------------------------------------------------

    total_required = len(
        jd_skills
    )

    total_matched = len(
        matched_skills
    )


    if total_required == 0:

        match_percentage = 0

    else:

        match_percentage = (
            total_matched
            / total_required
        ) * 100


    # -----------------------------------------------------
    # Return analysis
    # -----------------------------------------------------

    return {

        "resume_skills": resume_skills,

        "jd_skills": jd_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "total_required": total_required,

        "total_matched": total_matched,

        "match_percentage": round(
            match_percentage,
            2
        )
    }