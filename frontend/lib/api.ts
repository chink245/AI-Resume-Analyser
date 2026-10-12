const API_BASE_URL = "http://127.0.0.1:8000";


// =========================================================
// EXTRACT RESUME TEXT
// =========================================================
export async function extractResumeText(file: File): Promise<string> {
  console.log("FILE BEFORE UPLOAD:", {
    name: file.name,
    type: file.type,
    size: file.size,
  });

  if (!file || file.size === 0) {
    throw new Error("Selected PDF file is empty.");
  }

  const formData = new FormData();
  formData.append("file", file, file.name);

  console.log("FORM DATA FILE:", formData.get("file"));

  const response = await fetch(`${API_BASE_URL}/extract-resume-text`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  console.log("EXTRACT RESPONSE:", data);

  if (!response.ok) {
    throw new Error(
      `Resume extraction failed: ${JSON.stringify(data)}`
    );
  }

  if (!data.text || typeof data.text !== "string") {
    throw new Error(
      `Resume text was not extracted. Backend response: ${JSON.stringify(data)}`
    );
  }

  return data.text;
}


// =========================================================
// ANALYZE RESUME
// =========================================================

export async function analyzeResume(
  resumeText: string,
  jobDescription: string
) {

  const response = await fetch(
    `${API_BASE_URL}/analyze-resume`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
      }),
    }
  );

  if (!response.ok) {

    const errorText =
      await response.text();

    throw new Error(
      `Resume analysis failed: ${errorText}`
    );
  }

  return await response.json();
}