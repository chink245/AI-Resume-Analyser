
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from pydantic import BaseModel
import re
import pymupdf

from analysis_service import analyze_resume_vs_job


router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/")
def home():
    return {
        "message": "AI Resume Analyzer Backend is running!"
    }


# --------------------------------------------------
# TEXT CLEANING
# --------------------------------------------------

def clean_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph boundaries."""
    if not text:
        return ""

    text = text.replace("\u00a0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def repair_spaced_token(token: str) -> str:
    """
    Repair a token such as 'J a v a S c r i p t'
    when the PDF extractor places spaces between every character.
    """
    token = token.strip()

    if re.fullmatch(r"(?:[A-Za-z0-9]\s+){2,}[A-Za-z0-9]", token):
        return re.sub(r"\s+", "", token)

    return token


def extract_page_text(page) -> str:
    """
    Extract PDF text using word coordinates.
    Merge single-character tokens when their horizontal gaps
    suggest that they belong to the same word.
    """
    words = page.get_text("words", sort=True)

    if not words:
        return page.get_text("text", sort=True) or ""

    # Group extracted tokens by PDF block and line.
    lines = {}

    for word in words:
        x0, y0, x1, y1, token = word[:5]
        block_no = word[5]
        line_no = word[6]

        key = (block_no, line_no)

        lines.setdefault(key, []).append(
            (
                float(x0),
                float(y0),
                float(x1),
                float(y1),
                str(token)
            )
        )

    # Sort lines by their approximate vertical position.
    ordered_lines = sorted(
        lines.values(),
        key=lambda items: (
            min(item[1] for item in items),
            min(item[0] for item in items)
        )
    )

    output_lines = []

    # Characters commonly found in technology names, emails and URLs.
    allowed_char = re.compile(r"^[A-Za-z0-9@.+/#()_:\-?=&%]$")

    for line_words in ordered_lines:
        line_words.sort(key=lambda item: item[0])
        repaired_tokens = []
        i = 0

        while i < len(line_words):
            x0, y0, x1, y1, token = line_words[i]

            # Some extractors return spaced characters inside one token.
            token = repair_spaced_token(token)

            # Keep normal words unchanged.
            if len(token) != 1 or not allowed_char.fullmatch(token):
                repaired_tokens.append(token)
                i += 1
                continue

            group = [token]
            group_end = x1
            j = i + 1

            while j < len(line_words):
                nx0, ny0, nx1, ny1, next_token = line_words[j]
                next_token = repair_spaced_token(next_token)

                # Only combine adjacent individual character tokens.
                if (
                    len(next_token) != 1
                    or not allowed_char.fullmatch(next_token)
                ):
                    break

                current_width = max(x1 - x0, 1.0)
                next_width = max(nx1 - nx0, 1.0)
                gap = nx0 - group_end

                # Small gaps are likely character spacing.
                threshold = max(
                    1.5,
                    min(current_width, next_width) * 0.6 + 1.0
                )

                if gap > threshold:
                    break

                group.append(next_token)
                group_end = nx1
                j += 1

            if len(group) > 1:
                repaired_tokens.append("".join(group))
                i = j
            else:
                repaired_tokens.append(token)
                i += 1

        output_lines.append(" ".join(repaired_tokens))

    return clean_text("\n".join(output_lines))


# --------------------------------------------------
# FILE SAVING
# --------------------------------------------------

def save_uploaded_file(filename: str, contents: bytes) -> Path:
    """Save the file using its basename to prevent path traversal."""
    safe_filename = Path(filename or "resume.pdf").name
    file_path = UPLOAD_DIR / safe_filename
    file_path.write_bytes(contents)

    return file_path


# --------------------------------------------------
# UPLOAD RESUME
# --------------------------------------------------

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty. Please select your resume again."
        )

    try:
        with pymupdf.open(stream=contents, filetype="pdf") as pdf:
            if pdf.needs_pass:
                raise HTTPException(
                    status_code=400,
                    detail="This PDF is password-protected. Please upload an unlocked PDF."
                )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="We couldn't read this PDF. Please upload a valid PDF file."
        )

    file_path = save_uploaded_file(file.filename, contents)

    return {
        "message": "Resume uploaded successfully.",
        "filename": file_path.name
    }


# --------------------------------------------------
# EXTRACT RESUME TEXT
# --------------------------------------------------

@router.post("/extract-resume-text")
async def extract_resume_text(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty. Please select your resume again."
        )

    try:
        with pymupdf.open(stream=contents, filetype="pdf") as pdf:
            if pdf.needs_pass:
                raise HTTPException(
                    status_code=400,
                    detail="This PDF is password-protected. Please upload an unlocked PDF."
                )

            if pdf.page_count == 0:
                raise HTTPException(
                    status_code=400,
                    detail="This PDF has no pages. Please upload another resume."
                )

            extracted_pages = [
                extract_page_text(page)
                for page in pdf
            ]

        extracted_text = clean_text("\n\n".join(extracted_pages))

        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail=(
                    "No readable text was found in this PDF. "
                    "Please upload a text-based PDF resume."
                )
            )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="We couldn't read this PDF. Please upload a valid PDF file."
        )

    print("\n========== EXTRACTED RESUME TEXT ==========")
    print(extracted_text)
    print("===========================================\n")

    return {
        "filename": Path(file.filename).name,
        "text": extracted_text,
        "resume_text": extracted_text,
        "message": "Resume text extracted successfully."
    }


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

class JobDescription(BaseModel):
    job_description: str


@router.post("/job-description")
async def add_job_description(data: JobDescription):
    job_description = data.job_description.strip()

    if not job_description:
        raise HTTPException(
            status_code=400,
            detail="Please enter a job description."
        )

    return {
        "message": "Job description received successfully.",
        "job_description": job_description
    }


# --------------------------------------------------
# ANALYZE RESUME
# --------------------------------------------------

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/analyze-resume")
async def analyze_resume(data: ResumeAnalysisRequest):
    resume_text = data.resume_text.strip()
    job_description = data.job_description.strip()

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="Resume text is empty. Please upload your resume again."
        )

    if not job_description:
        raise HTTPException(
            status_code=400,
            detail="Please enter a job description before analyzing."
        )

    try:
        result = analyze_resume_vs_job(
            resume_text,
            job_description
        )
        return result

    except Exception:
        # Keep detailed exception information in the backend terminal.
        import logging
        logging.exception("Resume analysis failed")

        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed. Please try again."
        )
