"use client";

import {
  AlertCircle,
  CheckCircle2,
  Lightbulb,
  RotateCcw,
  Sparkles,
  Target,
} from "lucide-react";

interface AnalysisResultProps {
  matchPercentage: number;
  totalMatched: number;
  totalRequired: number;
  matchedSkills: string[];
  missingSkills: string[];
  improvementSuggestions?: string[];
  onReset: () => void;
}

export default function AnalysisResult({
  matchPercentage,
  totalMatched,
  totalRequired,
  matchedSkills,
  missingSkills,
  improvementSuggestions=[],
  onReset,
}: AnalysisResultProps) {
  return (
    <section className="mt-16">

      {/* ================= HEADER ================= */}

      <div className="mb-8 text-center">

        <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-emerald-400/10 bg-emerald-500/[0.07] px-4 py-2 text-sm text-emerald-400">
          <CheckCircle2 className="h-4 w-4" />
          Analysis Complete
        </div>

        <h2 className="text-3xl font-bold text-white md:text-4xl">
          Your Resume Match
        </h2>

        <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-slate-500">
          Here's how closely your resume matches the requirements
          of this job.
        </p>

      </div>


      {/* ================= SCORE CARD ================= */}

      <div className="relative overflow-hidden rounded-3xl border border-white/[0.08] bg-white/[0.025] p-8 shadow-2xl">

        {/* Background glow */}

        <div className="pointer-events-none absolute left-1/2 top-0 h-64 w-64 -translate-x-1/2 rounded-full bg-violet-600/10 blur-[100px]" />

        <div className="relative flex flex-col items-center">

          {/* Score */}

          <div className="relative flex h-44 w-44 items-center justify-center rounded-full border-8 border-violet-500/10">

            <div className="absolute inset-2 flex items-center justify-center rounded-full border border-violet-400/10 bg-[#0c0c13]">

              <div className="text-center">

                <div className="bg-gradient-to-r from-violet-400 via-indigo-400 to-cyan-400 bg-clip-text text-4xl font-bold text-transparent">
                  {matchPercentage.toFixed(2)}%
                </div>

                <p className="mt-1 text-xs uppercase tracking-widest text-slate-600">
                  Match Score
                </p>

              </div>

            </div>

          </div>


          {/* Summary */}

          <div className="mt-8 grid w-full max-w-lg grid-cols-2 gap-4">

            {/* Matched */}

            <div className="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.04] p-5 text-center">

              <div className="mx-auto mb-2 flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500/10">

                <CheckCircle2 className="h-5 w-5 text-emerald-400" />

              </div>

              <p className="text-2xl font-bold text-white">
                {totalMatched}
              </p>

              <p className="mt-1 text-xs text-slate-500">
                Matched Skills
              </p>

            </div>


            {/* Missing */}

            <div className="rounded-2xl border border-amber-500/10 bg-amber-500/[0.04] p-5 text-center">

              <div className="mx-auto mb-2 flex h-9 w-9 items-center justify-center rounded-xl bg-amber-500/10">

                <AlertCircle className="h-5 w-5 text-amber-400" />

              </div>

              <p className="text-2xl font-bold text-white">
                {missingSkills.length}
              </p>

              <p className="mt-1 text-xs text-slate-500">
                Missing Skills
              </p>

            </div>

          </div>


          {/* Required */}

          <p className="mt-5 text-xs text-slate-600">
            {totalMatched} of {totalRequired} required skills matched
          </p>

        </div>

      </div>


      {/* ================= SKILLS ================= */}

      <div className="mt-6 grid gap-6 lg:grid-cols-2">

        {/* ================= MATCHED SKILLS ================= */}

        <div className="rounded-3xl border border-white/[0.08] bg-white/[0.025] p-6">

          <div className="mb-5 flex items-center justify-between">

            <div className="flex items-center gap-3">

              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10">
                <CheckCircle2 className="h-5 w-5 text-emerald-400" />
              </div>

              <div>

                <h3 className="font-semibold text-white">
                  Matched Skills
                </h3>

                <p className="text-xs text-slate-600">
                  Skills found in your resume
                </p>

              </div>

            </div>

            <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-400">
              {matchedSkills.length}
            </span>

          </div>


          <div className="flex flex-wrap gap-2">

            {matchedSkills.map((skill) => (
              <span
                key={skill}
                className="rounded-lg border border-emerald-500/10 bg-emerald-500/[0.05] px-3 py-2 text-xs font-medium text-emerald-300"
              >
                ✓ {skill}
              </span>
            ))}

          </div>

        </div>


        {/* ================= MISSING SKILLS ================= */}

        <div className="rounded-3xl border border-white/[0.08] bg-white/[0.025] p-6">

          <div className="mb-5 flex items-center justify-between">

            <div className="flex items-center gap-3">

              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10">
                <AlertCircle className="h-5 w-5 text-amber-400" />
              </div>

              <div>

                <h3 className="font-semibold text-white">
                  Missing Skills
                </h3>

                <p className="text-xs text-slate-600">
                  Skills to consider improving
                </p>

              </div>

            </div>

            <span className="rounded-full bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-400">
              {missingSkills.length}
            </span>

          </div>


          {missingSkills.length > 0 ? (
            <div className="flex flex-wrap gap-2">

              {missingSkills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-lg border border-amber-500/10 bg-amber-500/[0.05] px-3 py-2 text-xs font-medium text-amber-300"
                >
                  + {skill}
                </span>
              ))}

            </div>
          ) : (
            <div className="flex items-center gap-2 text-sm text-emerald-400">

              <CheckCircle2 className="h-4 w-4" />

              Excellent! No missing skills detected.

            </div>
          )}

        </div>

      </div>


      {/* ================= AI IMPROVEMENT SUGGESTIONS ================= */}

      {improvementSuggestions.length > 0 && (
        <div className="relative mt-6 overflow-hidden rounded-3xl border border-cyan-500/10 bg-cyan-500/[0.04] p-6">

          {/* Background glow */}

          <div className="pointer-events-none absolute right-0 top-0 h-40 w-40 rounded-full bg-cyan-500/5 blur-[80px]" />


          {/* Header */}

          <div className="relative mb-5 flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10">

              <Target className="h-5 w-5 text-cyan-400" />

            </div>

            <div>

              <h3 className="font-semibold text-white">
                AI Improvement Suggestions
              </h3>

              <p className="text-xs text-slate-600">
                Personalized suggestions based on the job requirements
              </p>

            </div>

            <span className="ml-auto rounded-full bg-cyan-500/10 px-3 py-1 text-xs font-semibold text-cyan-400">
              {improvementSuggestions.length}
            </span>

          </div>


          {/* Suggestions */}

          <div className="relative space-y-3">

            {improvementSuggestions.map((suggestion, index) => (

              <div
                key={`${index}-${suggestion}`}
                className="flex gap-3 rounded-xl border border-white/[0.06] bg-white/[0.02] p-4 transition hover:border-cyan-500/10 hover:bg-white/[0.035]"
              >

                {/* Number */}

                <div className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-xs font-semibold text-cyan-400">
                  {index + 1}
                </div>


                {/* Suggestion */}

                <p className="text-sm leading-6 text-slate-400">
                  {suggestion}
                </p>

              </div>

            ))}

          </div>

        </div>
      )}


      {/* ================= INSIGHT ================= */}

      <div className="relative mt-6 overflow-hidden rounded-3xl border border-violet-500/10 bg-violet-500/[0.04] p-6">

        <div className="flex gap-4">

          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-violet-500/10">

            <Lightbulb className="h-5 w-5 text-violet-400" />

          </div>

          <div>

            <div className="flex items-center gap-2">

              <h3 className="font-semibold text-white">
                AI Insight
              </h3>

              <Sparkles className="h-4 w-4 text-violet-400" />

            </div>

            <p className="mt-2 text-sm leading-6 text-slate-400">

              Your resume matches{" "}

              <span className="font-semibold text-white">
                {totalMatched} out of {totalRequired}
              </span>{" "}

              required skills for this position. Focus on developing
              your missing skills to improve your overall job match.

            </p>

          </div>

        </div>

      </div>


      {/* ================= RESET ================= */}

      <div className="mt-8 flex justify-center">

        <button
          type="button"
          onClick={onReset}
          className="group flex items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.03] px-5 py-3 text-sm font-medium text-slate-400 transition hover:border-violet-500/20 hover:bg-violet-500/[0.05] hover:text-white"
        >

          <RotateCcw className="h-4 w-4 transition-transform group-hover:-rotate-45" />

          Analyze Another Resume

        </button>

      </div>

    </section>
  );
}