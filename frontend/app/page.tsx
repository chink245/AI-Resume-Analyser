"use client";

import { useState } from "react";
import {
  ArrowRight,
  CheckCircle2,
  FileText,
  Sparkles,
  Target,
  Zap,
} from "lucide-react";

import Navbar from "@/components/Navbar";
import ResumeUpload from "@/components/ResumeUpload";
import JobDescription from "@/components/JobDescription";
import AnalyzeButton from "@/components/AnalyzeButton";
import AnalysisResult from "@/components/AnalysisResult";

import {
  extractResumeText,
  analyzeResume,
} from "@/lib/api";


// =========================================================
// TYPES
// =========================================================

interface AnalysisResultData {
  match_percentage: number;
  total_required: number;
  total_matched: number;
  matched_skills: string[];
  missing_skills: string[];
  resume_skills: unknown[];
  improvement_suggestions: string[];
}


// =========================================================
// HOME
// =========================================================

export default function Home() {

  // -------------------------------------------------------
  // STATE
  // -------------------------------------------------------

  const [file, setFile] = useState<File | null>(null);

  const [jobDescription, setJobDescription] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [analysisResult, setAnalysisResult] =
    useState<AnalysisResultData | null>(null);


  // -------------------------------------------------------
  // ANALYZE RESUME
  // -------------------------------------------------------

  const handleAnalyze = async () => {

    if (!file || !jobDescription.trim()) {
      return;
    }

    try {

      setLoading(true);

      // -----------------------------------------------
      // 1. Extract resume text
      // -----------------------------------------------

      const resumeText =
        await extractResumeText(file);


      // -----------------------------------------------
      // 2. Analyze resume against job description
      // -----------------------------------------------

      const result =
        await analyzeResume(
          resumeText,
          jobDescription
        );


      // -----------------------------------------------
      // 3. Save result
      // -----------------------------------------------

      console.log(
        "ANALYSIS RESULT:",
        result
      );

      setAnalysisResult(result);


      // -----------------------------------------------
      // 4. Scroll to results
      // -----------------------------------------------

      setTimeout(() => {

        document
          .getElementById("analysis-result")
          ?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });

      }, 100);

    }  catch (error) {
  const message =
    error instanceof Error
      ? error.message
      : "It is not possible to analyze this file.";

  if (message === "Selected PDF file is empty.") {
    alert(
      "⚠️ It is not possible to analyze an empty PDF. Please upload a valid PDF."
    );
  } else {
    alert(
      "⚠️ It is not possible to analyze this resume. Please try another PDF."
    );
  }
} finally {

      setLoading(false);

    }
  };


  // -------------------------------------------------------
  // RESET
  // -------------------------------------------------------

  const handleReset = () => {

    setAnalysisResult(null);

    setFile(null);

    setJobDescription("");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };


  // -------------------------------------------------------
  // BUTTON STATE
  // -------------------------------------------------------

  const isDisabled =
    !file ||
    !jobDescription.trim() ||
    loading;


  // =======================================================
  // UI
  // =======================================================

  return (

    <main className="min-h-screen overflow-hidden bg-[#07070c] text-white">


      {/* ================================================= */}
      {/* NAVBAR */}
      {/* ================================================= */}

      <Navbar />


      {/* ================================================= */}
      {/* HERO */}
      {/* ================================================= */}

      <section className="relative px-6 pb-20 pt-20 md:pb-28 md:pt-28">

        {/* Background glow */}

        <div
          className="
            pointer-events-none
            absolute
            left-1/2
            top-0
            -z-0
            h-[500px]
            w-[700px]
            -translate-x-1/2
            rounded-full
            bg-violet-600/10
            blur-[140px]
          "
        />


        <div className="relative z-10 mx-auto max-w-5xl text-center">


          {/* Badge */}

          <div
            className="
              mb-7
              inline-flex
              items-center
              gap-2
              rounded-full
              border
              border-white/10
              bg-white/[0.04]
              px-4
              py-2
              text-sm
              text-slate-300
              shadow-lg
              shadow-violet-500/5
              backdrop-blur
            "
          >

            <Sparkles
              size={15}
              className="text-violet-400"
            />

            AI-Powered Resume Analyzer

            <ArrowRight
              size={14}
              className="text-slate-500"
            />

          </div>


          {/* Heading */}

          <h1
            className="
              text-5xl
              font-bold
              leading-[1.05]
              tracking-tight
              sm:text-6xl
              md:text-7xl
              lg:text-8xl
            "
          >

            Your Resume.

            <br />

            <span
              className="
                bg-gradient-to-r
                from-violet-400
                via-indigo-400
                to-cyan-400
                bg-clip-text
                text-transparent
              "
            >
              Your Next Opportunity.
            </span>

          </h1>


          {/* Description */}

          <p
            className="
              mx-auto
              mt-7
              max-w-2xl
              text-base
              leading-7
              text-slate-400
              sm:text-lg
            "
          >

            Discover how well your resume matches a job description.
            Get instant AI-powered skill analysis and find exactly
            what you need to improve.

          </p>


          {/* Mini stats */}

          <div
            className="
              mt-8
              flex
              flex-wrap
              items-center
              justify-center
              gap-6
              text-sm
              text-slate-400
            "
          >

            <div className="flex items-center gap-2">

              <CheckCircle2
                size={16}
                className="text-emerald-400"
              />

              Skill Matching

            </div>


            <div className="flex items-center gap-2">

              <CheckCircle2
                size={16}
                className="text-emerald-400"
              />

              AI Analysis

            </div>


            <div className="flex items-center gap-2">

              <CheckCircle2
                size={16}
                className="text-emerald-400"
              />

              Instant Results

            </div>

          </div>

        </div>

      </section>


      {/* ================================================= */}
      {/* ANALYZER */}
      {/* ================================================= */}

      <section
        id="analyzer"
        className="relative px-6 pb-24"
      >

        <div className="mx-auto max-w-6xl">


          {/* Section heading */}

          <div
            className="
              mb-8
              flex
              flex-col
              gap-3
              md:flex-row
              md:items-end
              md:justify-between
            "
          >

            <div>

              <p
                className="
                  text-sm
                  font-medium
                  uppercase
                  tracking-widest
                  text-violet-400
                "
              >
                Resume Analysis
              </p>


              <h2
                className="
                  mt-2
                  text-2xl
                  font-semibold
                  text-white
                  md:text-3xl
                "
              >
                Analyze your resume
              </h2>

            </div>


            <p
              className="
                max-w-md
                text-sm
                leading-6
                text-slate-500
                md:text-right
              "
            >
              Upload your resume and provide the job description
              you're targeting.
            </p>

          </div>


          {/* ================================================= */}
          {/* INPUT CARDS */}
          {/* ================================================= */}

          <div className="grid gap-6 lg:grid-cols-2">


            {/* ------------------------------------------------- */}
            {/* RESUME */}
            {/* ------------------------------------------------- */}

            <div
              className="
                group
                rounded-3xl
                border
                border-white/[0.08]
                bg-white/[0.025]
                p-2
                shadow-2xl
                shadow-black/20
                transition
                duration-300
                hover:border-violet-500/20
              "
            >

              <div
                className="
                  rounded-[22px]
                  border
                  border-white/[0.06]
                  bg-[#0c0c13]
                  p-6
                "
              >

                <div className="mb-5 flex items-center gap-3">

                  <div
                    className="
                      flex
                      h-11
                      w-11
                      items-center
                      justify-center
                      rounded-xl
                      bg-violet-500/10
                      text-violet-400
                    "
                  >
                    <FileText size={21} />
                  </div>


                  <div>

                    <h3 className="font-semibold text-white">
                      Upload Resume
                    </h3>

                    <p className="text-sm text-slate-500">
                      PDF format recommended
                    </p>

                  </div>

                </div>


                <ResumeUpload
                  file={file}
                  onFileChange={setFile}
                />

              </div>

            </div>


            {/* ------------------------------------------------- */}
            {/* JOB DESCRIPTION */}
            {/* ------------------------------------------------- */}

            <div
              className="
                group
                rounded-3xl
                border
                border-white/[0.08]
                bg-white/[0.025]
                p-2
                shadow-2xl
                shadow-black/20
                transition
                duration-300
                hover:border-indigo-500/20
              "
            >

              <div
                className="
                  rounded-[22px]
                  border
                  border-white/[0.06]
                  bg-[#0c0c13]
                  p-6
                "
              >

                <div className="mb-5 flex items-center gap-3">

                  <div
                    className="
                      flex
                      h-11
                      w-11
                      items-center
                      justify-center
                      rounded-xl
                      bg-indigo-500/10
                      text-indigo-400
                    "
                  >
                    <Target size={21} />
                  </div>


                  <div>

                    <h3 className="font-semibold text-white">
                      Job Description
                    </h3>

                    <p className="text-sm text-slate-500">
                      Paste the role you're applying for
                    </p>

                  </div>

                </div>


                <JobDescription
                  value={jobDescription}
                  onChange={setJobDescription}
                />

              </div>

            </div>

          </div>


          {/* ================================================= */}
          {/* ANALYZE BUTTON */}
          {/* ================================================= */}

          <div className="mt-7">

            <AnalyzeButton
              disabled={isDisabled}
              loading={loading}
              onClick={handleAnalyze}
            />


            <div
              className="
                mt-4
                flex
                items-center
                justify-center
                gap-2
                text-xs
                text-slate-600
              "
            >

              <Zap size={13} />

              Your resume is processed securely using our
              AI skill-matching engine.

            </div>

          </div>


          {/* ================================================= */}
          {/* ANALYSIS RESULT */}
          {/* ================================================= */}

          {analysisResult && (

            <div id="analysis-result">

              <AnalysisResult
  matchPercentage={analysisResult.match_percentage}
  totalMatched={analysisResult.total_matched}
  totalRequired={analysisResult.total_required}
  matchedSkills={analysisResult.matched_skills}
  missingSkills={analysisResult.missing_skills}
  improvementSuggestions={analysisResult.improvement_suggestions}
  onReset={handleReset}
/>

            </div>

          )}

        </div>

      </section>


      {/* ================================================= */}
      {/* FEATURES */}
      {/* ================================================= */}

      <section
        className="
          border-t
          border-white/[0.06]
          px-6
          py-20
        "
      >

        <div className="mx-auto max-w-6xl">


          <div className="mx-auto mb-12 max-w-xl text-center">

            <p
              className="
                text-sm
                font-medium
                uppercase
                tracking-widest
                text-violet-400
              "
            >
              Why use ResumeAI?
            </p>


            <h2
              className="
                mt-3
                text-3xl
                font-bold
                md:text-4xl
              "
            >
              Understand your resume better
            </h2>


            <p className="mt-4 text-slate-500">

              Go beyond a basic resume checker. Understand exactly
              how your skills align with the job.

            </p>

          </div>


          {/* Feature cards */}

          <div className="grid gap-5 md:grid-cols-3">


            {/* Feature 1 */}

            <div
              className="
                rounded-2xl
                border
                border-white/[0.07]
                bg-white/[0.025]
                p-6
                transition
                hover:-translate-y-1
                hover:border-violet-500/20
              "
            >

              <div
                className="
                  mb-5
                  flex
                  h-11
                  w-11
                  items-center
                  justify-center
                  rounded-xl
                  bg-violet-500/10
                  text-violet-400
                "
              >
                <Target size={20} />
              </div>


              <h3 className="text-lg font-semibold">
                Smart Skill Matching
              </h3>


              <p className="mt-2 text-sm leading-6 text-slate-500">

                Compare your resume skills with the requirements
                of the job you're targeting.

              </p>

            </div>


            {/* Feature 2 */}

            <div
              className="
                rounded-2xl
                border
                border-white/[0.07]
                bg-white/[0.025]
                p-6
                transition
                hover:-translate-y-1
                hover:border-indigo-500/20
              "
            >

              <div
                className="
                  mb-5
                  flex
                  h-11
                  w-11
                  items-center
                  justify-center
                  rounded-xl
                  bg-indigo-500/10
                  text-indigo-400
                "
              >
                <Sparkles size={20} />
              </div>


              <h3 className="text-lg font-semibold">
                AI-Powered Analysis
              </h3>


              <p className="mt-2 text-sm leading-6 text-slate-500">

                Semantic analysis helps identify relevant skills
                beyond simple keyword matching.

              </p>

            </div>


            {/* Feature 3 */}

            <div
              className="
                rounded-2xl
                border
                border-white/[0.07]
                bg-white/[0.025]
                p-6
                transition
                hover:-translate-y-1
                hover:border-cyan-500/20
              "
            >

              <div
                className="
                  mb-5
                  flex
                  h-11
                  w-11
                  items-center
                  justify-center
                  rounded-xl
                  bg-cyan-500/10
                  text-cyan-400
                "
              >
                <Zap size={20} />
              </div>


              <h3 className="text-lg font-semibold">
                Actionable Insights
              </h3>


              <p className="mt-2 text-sm leading-6 text-slate-500">

                See missing skills and discover what you should
                improve before applying.

              </p>

            </div>

          </div>

        </div>

      </section>


      {/* ================================================= */}
      {/* FOOTER */}
      {/* ================================================= */}

      <footer
        className="
          border-t
          border-white/[0.06]
          px-6
          py-8
        "
      >

        <div
          className="
            mx-auto
            flex
            max-w-6xl
            flex-col
            items-center
            justify-between
            gap-4
            text-sm
            text-slate-600
            md:flex-row
          "
        >

          <p>
            © 2026 ResumeAI. Built with AI.
          </p>


          <div className="flex gap-5">

            <span className="cursor-pointer hover:text-slate-400">
              Privacy
            </span>

            <span className="cursor-pointer hover:text-slate-400">
              About
            </span>

          </div>

        </div>

      </footer>

    </main>
  );
}
