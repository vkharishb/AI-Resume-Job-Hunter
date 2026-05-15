import { useEffect, useState } from "react";
import { CheckCircle, FileSpreadsheet, Sparkles } from "lucide-react";
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
    <main className="min-h-screen bg-slate-50 text-slate-950 transition dark:bg-slate-950 dark:text-white">
      <section className="relative overflow-hidden bg-[linear-gradient(135deg,#0f172a_0%,#0f766e_52%,#f59e0b_100%)]">
        <div className="mx-auto flex max-w-6xl flex-col gap-10 px-4 py-6 sm:px-6 lg:px-8">
          <header className="flex items-center justify-between">
            <div className="flex items-center gap-3 text-white">
              <span className="inline-flex h-10 w-10 items-center justify-center rounded-md bg-white/15 backdrop-blur">
                <Sparkles size={20} />
              </span>
              <span className="text-base font-bold">AI Resume Job Hunter</span>
            </div>
            <ThemeToggle darkMode={darkMode} onToggle={() => setDarkMode((value) => !value)} />
          </header>

          <div className="grid items-center gap-8 pb-10 pt-2 lg:grid-cols-[1.05fr_0.95fr]">
            <div className="max-w-2xl">
              <p className="mb-3 inline-flex rounded-md bg-white/15 px-3 py-1 text-sm font-medium text-white backdrop-blur">India-focused job matching</p>
              <h1 className="text-4xl font-bold leading-tight text-white sm:text-5xl">Turn one resume into a ranked application tracker.</h1>
              <p className="mt-5 max-w-xl text-base leading-7 text-white/85">
                Upload a PDF or paste a GitHub resume link. The backend parses the resume, analyzes your profile, searches live Indian roles, exports Excel, creates Google Sheets, and emails the tracker.
              </p>
            </div>
            <ResumeForm loading={loading} onSubmit={handleSubmit} />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        {loading && (
          <div className="rounded-lg border border-teal-200 bg-teal-50 p-5 text-teal-950 dark:border-teal-500/30 dark:bg-teal-500/10 dark:text-teal-100">
            <div className="flex items-center gap-3">
              <span className="h-6 w-6 animate-spin rounded-full border-2 border-teal-300 border-t-teal-700" />
              <span className="font-semibold">Analyzing resume and matching jobs...</span>
            </div>
          </div>
        )}

        {error && <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700 dark:border-red-500/30 dark:bg-red-500/10 dark:text-red-200">{error}</div>}

        {result && (
          <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-5 text-emerald-950 dark:border-emerald-500/30 dark:bg-emerald-500/10 dark:text-emerald-100">
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
