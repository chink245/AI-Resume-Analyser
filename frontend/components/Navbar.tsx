"use client";

import {
  ArrowRight,
  FileSearch,
  Sparkles,
} from "lucide-react";

export default function Navbar() {
  const scrollToAnalyzer = () => {
    document
      .getElementById("analyzer")
      ?.scrollIntoView({
        behavior: "smooth",
      });
  };

  return (
    <nav
      className="
        sticky top-0 z-50
        border-b border-white/[0.06]
        bg-[#07070c]/80
        backdrop-blur-xl
      "
    >
      <div
        className="
          mx-auto flex h-18 max-w-7xl
          items-center justify-between
          px-5 sm:px-6
        "
      >

        {/* ================= LOGO ================= */}

        <button
          type="button"
          onClick={() =>
            window.scrollTo({
              top: 0,
              behavior: "smooth",
            })
          }
          className="group flex items-center gap-3"
        >

          <div
            className="
              relative flex h-10 w-10
              items-center justify-center
              overflow-hidden rounded-xl
              bg-gradient-to-br
              from-violet-500
              via-indigo-500
              to-cyan-500
              shadow-lg
              shadow-violet-500/20
              transition-all duration-300
              group-hover:scale-105
              group-hover:shadow-violet-500/30
            "
          >

            <FileSearch
              className="
                relative z-10 h-5 w-5
                text-white
              "
            />

            {/* Glow */}

            <div
              className="
                absolute inset-0
                bg-white/10
                opacity-0
                transition-opacity
                group-hover:opacity-100
              "
            />

          </div>


          <div className="text-left">

            <div className="text-lg font-bold tracking-tight">

              <span className="text-white">
                Resume
              </span>

              <span
                className="
                  bg-gradient-to-r
                  from-violet-400
                  to-cyan-400
                  bg-clip-text
                  text-transparent
                "
              >
                AI
              </span>

            </div>

            <p className="hidden text-[11px] text-slate-500 sm:block">
              Smart Resume Analyzer
            </p>

          </div>

        </button>


        {/* ================= DESKTOP NAV ================= */}

        <div className="hidden items-center gap-8 md:flex">

          <button
            type="button"
            onClick={() =>
              window.scrollTo({
                top: 0,
                behavior: "smooth",
              })
            }
            className="
              text-sm text-slate-400
              transition hover:text-white
            "
          >
            Home
          </button>

          <button
            type="button"
            onClick={scrollToAnalyzer}
            className="
              text-sm text-slate-400
              transition hover:text-white
            "
          >
            Analyzer
          </button>

          <a
            href="#features"
            className="
              text-sm text-slate-400
              transition hover:text-white
            "
          >
            Features
          </a>

        </div>


        {/* ================= RIGHT SIDE ================= */}

        <div className="flex items-center gap-3">

          {/* AI status */}

          <div
            className="
              hidden items-center gap-2
              rounded-full
              border border-violet-400/15
              bg-violet-500/[0.07]
              px-3 py-1.5
              sm:flex
            "
          >

            <span
              className="
                h-1.5 w-1.5
                rounded-full
                bg-emerald-400
                shadow-sm
                shadow-emerald-400/50
              "
            />

            <Sparkles
              className="h-3.5 w-3.5 text-violet-400"
            />

            <span className="text-xs font-medium text-violet-300">
              AI Powered
            </span>

          </div>


          {/* CTA */}

          <button
            type="button"
            onClick={scrollToAnalyzer}
            className="
              group flex items-center gap-2
              rounded-xl
              bg-white
              px-3.5 py-2
              text-sm font-semibold
              text-slate-950
              transition-all duration-200
              hover:-translate-y-0.5
              hover:bg-slate-100
              hover:shadow-lg
              hover:shadow-white/10
              active:translate-y-0
            "
          >

            <span className="hidden sm:inline">
              Get Started
            </span>

            <span className="sm:hidden">
              Start
            </span>

            <ArrowRight
              className="
                h-4 w-4
                transition-transform
                group-hover:translate-x-0.5
              "
            />

          </button>

        </div>

      </div>
    </nav>
  );
}

