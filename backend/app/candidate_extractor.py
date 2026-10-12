import spacy


# =========================================================
# LOAD SPACY MODEL
# =========================================================

nlp = spacy.load(
    "en_core_web_sm"
)


# =========================================================
# EXTRACT CANDIDATE PHRASES
# =========================================================

def extract_candidates(text):

    if not text:
        return []

    doc = nlp(text)

    candidates = set()

    # =====================================================
    # 1. NOUN CHUNKS
    # =====================================================

    for chunk in doc.noun_chunks:

        phrase = chunk.text.strip()

        if not phrase:
            continue

        # Ignore very short phrases
        if len(phrase) < 3:
            continue

        # Must contain alphabet
        if not any(
            char.isalpha()
            for char in phrase
        ):
            continue

        candidates.add(phrase)

    # =====================================================
    # 2. NAMED ENTITIES
    # =====================================================

    for ent in doc.ents:

        phrase = ent.text.strip()

        if not phrase:
            continue

        if len(phrase) < 3:
            continue

        if not any(
            char.isalpha()
            for char in phrase
        ):
            continue

        candidates.add(phrase)

    # =====================================================
    # 3. IMPORTANT TECHNOLOGY TOKENS
    # =====================================================
    #
    # We DO NOT add every individual token anymore.
    #
    # This prevents things like:
    #
    # J
    # I
    # My
    # The
    #
    # from going into semantic search.
    #
    # Instead, only add tokens which are long enough.
    # =====================================================

    for token in doc:

        if not token.is_alpha:
            continue

        word = token.text.strip()

        if len(word) < 3:
            continue

        candidates.add(word)

    # =====================================================
    # RETURN CLEAN CANDIDATES
    # =====================================================

    return list(candidates)