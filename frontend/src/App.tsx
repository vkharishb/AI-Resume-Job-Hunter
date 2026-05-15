import { useEffect, useState } from "react";
import { CheckCircle, FileSpreadsheet, Search } from "lucide-react";
import { analyzeResume } from "./api";
import { JobsTable } from "./components/JobsTable";
import { ResumeForm } from "./components/ResumeForm";
import { ThemeToggle } from "./components/ThemeToggle";
import type { AnalyzeResponse } from "./types";

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  async function handleSubmit(formData: FormData) {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      setResult(await analyzeResume(formData));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 text-slate-950 transition dark:bg-slate-950 dark:text-white">
      <section className="border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-md bg-teal-600 text-white">
              <Search size={20} />
            </span>
            <div>
              <p className="text-sm font-bold text-slate-950 dark:text-white">AI Resume Job Hunter</p>
              <p className="text-xs text-slate-500 dark:text-slate-400">India-focused job matching</p>
            </div>
          </div>
          <ThemeToggle darkMode={darkMode} onToggle={() => setDarkMode((value) => !value)} />
        </div>
      </section>

      <section className="mx-auto flex max-w-4xl flex-col items-center px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-8 max-w-2xl text-center">
          <h1 className="text-3xl font-bold leading-tight text-slate-950 dark:text-white sm:text-4xl">Find matched jobs from your resume</h1>
          <p className="mt-4 text-base leading-7 text-slate-600 dark:text-slate-300">
            Upload a resume PDF or paste a GitHub PDF link. The app analyzes your profile and prepares a ranked application tracker.
          </p>
        </div>

        <div className="w-full max-w-2xl">
          <ResumeForm loading={loading} onSubmit={handleSubmit} />
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 pb-10 sm:px-6 lg:px-8">
        {loading && (
          <div className="mx-auto max-w-2xl rounded-lg border border-teal-200 bg-white p-5 text-teal-950 shadow-sm dark:border-teal-500/30 dark:bg-slate-900 dark:text-teal-100">
            <div className="flex items-center justify-center gap-3 text-center">
              <span className="h-6 w-6 animate-spin rounded-full border-2 border-teal-300 border-t-teal-700" />
              <span className="font-semibold">Analyzing resume and matching jobs...</span>
            </div>
          </div>
        )}

        {error && (
          <div className="mx-auto max-w-2xl rounded-lg border border-red-200 bg-white p-4 text-center text-sm font-medium text-red-700 shadow-sm dark:border-red-500/30 dark:bg-slate-900 dark:text-red-200">
            {error}
          </div>
        )}

        {result && (
          <div className="mx-auto max-w-4xl rounded-lg border border-emerald-200 bg-white p-5 text-emerald-950 shadow-sm dark:border-emerald-500/30 dark:bg-slate-900 dark:text-emerald-100">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center gap-3">
                <CheckCircle size={24} />
                <div>
                  <h2 className="font-bold">Tracker generated successfully</h2>
                  <p className="text-sm opacity-80">Excel has been emailed when SMTP is configured.</p>
                </div>
              </div>
              {result.google_sheet_url && (
                <a className="inline-flex min-h-10 items-center justify-center gap-2 rounded-md bg-emerald-700 px-4 text-sm font-semibold text-white hover:bg-emerald-800" href={result.google_sheet_url} target="_blank" rel="noreferrer">
                  <FileSpreadsheet size={18} />
                  Open Google Sheet
                </a>
              )}
            </div>
          </div>
        )}

        <JobsTable jobs={result?.jobs ?? []} />
      </section>
    </main>
  );
}
