from unified_skill_loader import load_unified_skills
import re


def normalize_text(text):
    """
    Normalize text for comparison.
    """

    if not text:
        return ""

    text = str(text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip().casefold()


def build_alias_index():

    skills = load_unified_skills()

    alias_index = {}

    for _, row in skills.iterrows():

        skill_id = row["skill_id"]
        skill_name = row["skill_name"]

        # ------------------------------------------------
        # 1. Canonical skill name
        # ------------------------------------------------

        normalized_skill = normalize_text(
            skill_name
        )

        if normalized_skill:
            alias_index[normalized_skill] = skill_id


        # ------------------------------------------------
        # 2. Alternative labels
        # ------------------------------------------------

        aliases = row["aliases"]

        if not aliases:
            continue

        # ESCO can contain multiple aliases
        # separated by newline characters OR spaces.
        #
        # We first normalize the raw value.
        aliases = str(aliases)

        aliases = aliases.replace(
            "\\n",
            "\n"
        )

        # Split newline-separated aliases
        alias_list = re.split(
            r"\n",
            aliases
        )

        for alias in alias_list:

            normalized_alias = normalize_text(
                alias
            )

            if normalized_alias:

                alias_index[
                    normalized_alias
                ] = skill_id


    return alias_index