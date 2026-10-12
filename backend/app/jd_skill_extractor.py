from skill_detector import detect_exact_skills


# =========================================================
# EXTRACT JOB DESCRIPTION SKILLS
# =========================================================

def extract_jd_skills(job_description):

    if not job_description:
        return []

    # -----------------------------------------------------
    # For Job Descriptions:
    #
    # Use only:
    #   1. Exact skill matching
    #   2. Alias matching
    #   3. Technology matching
    #
    # Do NOT use semantic matching here.
    # -----------------------------------------------------

    skills = detect_exact_skills(
        job_description
    )

    return skills