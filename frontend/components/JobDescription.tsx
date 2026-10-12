"use client";

import {
  BriefcaseBusiness,
  FileText,
  Sparkles,
  X,
} from "lucide-react";

interface JobDescriptionProps {
  value: string;
  onChange: (value: string) => void;
}

export default function JobDescription({
  value,
  onChange,
}: JobDescriptionProps) {
  const MAX_LENGTH = 10000;

  const handleChange = (
    event: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    const newValue = event.target.value;

    if (newValue.length <= MAX_LENGTH) {
      onChange(newValue);
    }
  };

  const clearDescription = () => {
    onChange("");
  };

  return (
    <div className="w-full">

      {/* ================= EMPTY / INPUT STATE ================= */}

      <div className="relative">

        {/* Subtle background glow */}

        <div
          className="
            pointer-events-none absolute
            -right-10 -top-10
            h-32 w-32
            rounded-full
            bg-indigo-500/10
            blur-3xl
          "
        />

        <div
          className="
            relative overflow-hidden
            rounded-2xl
            border border-slate-800
            bg-slate-950/60
            transition-all duration-300
            focus-within:border-violet-500/40
            focus-within:ring-4
            focus-within:ring-violet-500/[0.06]
          "
        >

          {/* Textarea */}

          <textarea
            value={value}
            onChange={handleChange}
            placeholder={`Paste the job description here...

For example:
• Required technical skills
• Years of experience
• Responsibilities
• Qualifications`}
            className="
              min-h-[260px]
              w-full resize-none
              bg-transparent
              px-5 pb-14 pt-5
              text-sm leading-7
              text-white
              outline-none
              placeholder:text-slate-600
            "
          />

          {/* Bottom toolbar */}

          <div
            className="
              absolute bottom-0 left-0 right-0
              flex items-center justify-between
              border-t border-white/[0.05]
              bg-slate-950/80
              px-4 py-3
              backdrop-blur
            "
          >

            {/* Character information */}

            <div className="flex items-center gap-2">

              <FileText
                className="h-3.5 w-3.5 text-slate-600"
              />

              <span
                className={`text-xs ${
                  value.length > MAX_LENGTH * 0.9
                    ? "text-amber-400"
                    : "text-slate-600"
                }`}
              >
                {value.length.toLocaleString()} /{" "}
                {MAX_LENGTH.toLocaleString()}
              </span>

            </div>


            {/* Clear button */}

            {value.length > 0 && (
              <button
                type="button"
                onClick={clearDescription}
                className="
                  flex items-center gap-1.5
                  rounded-lg
                  px-2.5 py-1.5
                  text-xs font-medium
                  text-slate-500
                  transition
                  hover:bg-white/[0.05]
                  hover:text-slate-300
                "
              >
                <X className="h-3.5 w-3.5" />
                Clear
              </button>
            )}

          </div>

        </div>

      </div>


      {/* ================= HELPER ================= */}

      <div className="mt-4 flex items-start gap-2.5">

        <div
          className="
            mt-0.5 flex h-6 w-6 shrink-0
            items-center justify-center
            rounded-lg
            bg-violet-500/10
          "
        >
          <Sparkles
            className="h-3.5 w-3.5 text-violet-400"
          />
        </div>

        <p className="text-xs leading-5 text-slate-600">
          Include the complete job description for more accurate
          skill matching and better analysis.
        </p>

      </div>

    </div>
  );
}
