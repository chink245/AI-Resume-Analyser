"use client";

import {
  CheckCircle2,
  FileText,
  UploadCloud,
  X,
} from "lucide-react";
import { useRef, useState } from "react";

interface ResumeUploadProps {
  file: File | null;
  onFileChange: (file: File | null) => void;
}

export default function ResumeUpload({
  file,
  onFileChange,
}: ResumeUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const [isDragging, setIsDragging] = useState(false);

  const validateAndSetFile = (selectedFile: File) => {
    // PDF validation
    if (selectedFile.type !== "application/pdf") {
      alert("Please upload a PDF resume.");
      return;
    }

    // 10MB validation
    if (selectedFile.size > 10 * 1024 * 1024) {
      alert("Resume must be smaller than 10MB.");
      return;
    }

    onFileChange(selectedFile);
  };

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) return;

    validateAndSetFile(selectedFile);
  };

  const handleDragOver = (
    event: React.DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (
    event: React.DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (
    event: React.DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();

    setIsDragging(false);

    const droppedFile = event.dataTransfer.files?.[0];

    if (!droppedFile) return;

    validateAndSetFile(droppedFile);
  };

  const removeFile = () => {
    onFileChange(null);

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <div className="w-full">

      {!file ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={`
            group relative flex min-h-[260px] cursor-pointer
            flex-col items-center justify-center
            overflow-hidden rounded-2xl
            border border-dashed
            px-6 py-10 text-center
            transition-all duration-300

            ${
              isDragging
                ? "border-violet-400 bg-violet-500/10 scale-[1.01]"
                : "border-slate-700 bg-slate-950/60 hover:border-violet-500/50 hover:bg-violet-500/[0.03]"
            }
          `}
        >

          {/* Background glow */}

          <div
            className="
              pointer-events-none absolute
              left-1/2 top-1/2
              h-40 w-40
              -translate-x-1/2 -translate-y-1/2
              rounded-full
              bg-violet-600/10
              blur-3xl
              transition-opacity
              group-hover:opacity-100
            "
          />

          {/* Upload icon */}

          <div
            className="
              relative mb-5
              flex h-16 w-16
              items-center justify-center
              rounded-2xl
              border border-violet-400/10
              bg-violet-500/10
              shadow-lg shadow-violet-500/10
              transition-all duration-300
              group-hover:-translate-y-1
              group-hover:scale-105
            "
          >
            <UploadCloud
              className="
                h-7 w-7
                text-violet-400
                transition-transform duration-300
                group-hover:-translate-y-0.5
              "
            />
          </div>

          {/* Main text */}

          <h3 className="relative text-base font-semibold text-white">
            {isDragging
              ? "Drop your resume here"
              : "Upload your resume"}
          </h3>

          <p className="relative mt-2 text-sm text-slate-500">
            Drag & drop your PDF here or{" "}
            <span className="font-medium text-violet-400">
              browse files
            </span>
          </p>

          {/* File info */}

          <div className="relative mt-5 flex items-center gap-2">

            <span className="rounded-md border border-white/5 bg-white/[0.04] px-2 py-1 text-[11px] font-medium text-slate-400">
              PDF
            </span>

            <span className="text-xs text-slate-600">
              Maximum size: 10MB
            </span>

          </div>

          <input
            ref={inputRef}
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="hidden"
          />

        </div>
      ) : (

        /* ================= FILE SELECTED ================= */

        <div className="relative overflow-hidden rounded-2xl border border-emerald-500/20 bg-emerald-500/[0.04] p-5">

          {/* Success glow */}

          <div
            className="
              pointer-events-none absolute
              -right-10 -top-10
              h-32 w-32
              rounded-full
              bg-emerald-500/10
              blur-3xl
            "
          />

          <div className="relative flex items-center justify-between gap-4">

            <div className="flex min-w-0 items-center gap-4">

              {/* PDF icon */}

              <div className="relative flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-emerald-500/10">

                <FileText className="h-6 w-6 text-emerald-400" />

                <CheckCircle2
                  className="
                    absolute -right-1 -top-1
                    h-4 w-4
                    fill-[#0c0c13]
                    text-emerald-400
                  "
                />

              </div>

              {/* File information */}

              <div className="min-w-0">

                <div className="flex items-center gap-2">

                  <p className="truncate font-medium text-white">
                    {file.name}
                  </p>

                  <span className="hidden rounded-md bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-400 sm:block">
                    READY
                  </span>

                </div>

                <p className="mt-1 text-xs text-slate-500">
                  {(file.size / 1024 / 1024).toFixed(2)} MB · PDF
                </p>

              </div>

            </div>

            {/* Remove */}

            <button
              type="button"
              aria-label="Remove resume"
              onClick={removeFile}
              className="
                shrink-0 rounded-xl
                border border-white/[0.06]
                bg-white/[0.03]
                p-2
                text-slate-500
                transition-all duration-200
                hover:border-red-500/20
                hover:bg-red-500/10
                hover:text-red-400
              "
            >
              <X className="h-4 w-4" />
            </button>

          </div>

          {/* Replace file */}

          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            className="
              relative mt-5
              text-xs font-medium
              text-violet-400
              transition hover:text-violet-300
            "
          >
            Replace resume
          </button>

          <input
            ref={inputRef}
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="hidden"
          />

        </div>
      )}

    </div>
  );
}
