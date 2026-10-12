
"use client";

import {
  ArrowRight,
  Loader2,
  Sparkles,
} from "lucide-react";

interface AnalyzeButtonProps {
  disabled: boolean;
  loading: boolean;
  onClick: () => void;
}

export default function AnalyzeButton({
  disabled,
  loading,
  onClick,
}: AnalyzeButtonProps) {
  return (
    <button
      type="button"
      disabled={disabled || loading}
      onClick={onClick}
      className="
        group relative flex w-full items-center justify-center
        gap-3 overflow-hidden rounded-2xl
        bg-gradient-to-r from-violet-600 via-indigo-600 to-violet-600
        bg-[length:200%_100%]
        px-6 py-4.5
        text-sm font-semibold text-white
        shadow-xl shadow-violet-600/20
        transition-all duration-300

        hover:-translate-y-0.5
        hover:bg-[position:100%_0]
        hover:shadow-2xl
        hover:shadow-violet-600/30

        active:translate-y-0
        active:scale-[0.99]

        disabled:cursor-not-allowed
        disabled:opacity-40
        disabled:shadow-none
        disabled:hover:translate-y-0
        disabled:hover:shadow-none
      "
    >
      {/* Animated shine */}

      {!disabled && !loading && (
        <span
          className="
            absolute inset-0
            -translate-x-full
            bg-gradient-to-r
            from-transparent
            via-white/10
            to-transparent
            transition-transform duration-700
            group-hover:translate-x-full
          "
        />
      )}

      {/* Button content */}

      {loading ? (
        <>
          <Loader2
            className="h-5 w-5 animate-spin"
          />

          <span>
            Analyzing Resume...
          </span>
        </>
      ) : (
        <>
          <span
            className="
              flex h-7 w-7 items-center justify-center
              rounded-lg bg-white/10
              ring-1 ring-white/10
              transition-transform duration-300
              group-hover:rotate-6
            "
          >
            <Sparkles className="h-4 w-4" />
          </span>

          <span>
            Analyze Resume
          </span>

          <ArrowRight
            className="
              h-5 w-5
              transition-transform duration-300
              group-hover:translate-x-1
            "
          />
        </>
      )}
    </button>
  );
}
