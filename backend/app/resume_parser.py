import spacy


# Load pretrained English NLP model
nlp = spacy.load("en_core_web_sm")


def process_resume_text(text: str):
    """
    Process resume text using spaCy NLP.
    """

    doc = nlp(text)

    # Extract named entities detected by the NLP model
    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
        })

    # Extract sentences
    sentences = [
        sentence.text.strip()
        for sentence in doc.sents
    ]

    return {
        "entities": entities,
        "sentences": sentences
    }