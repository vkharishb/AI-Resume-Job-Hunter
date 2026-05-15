import { FormEvent, useMemo, useState } from "react";
import { Link, Mail, Send, Upload } from "lucide-react";

type Props = {
  loading: boolean;
  onSubmit: (formData: FormData) => Promise<void>;
};

export function ResumeForm({ loading, onSubmit }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [githubUrl, setGithubUrl] = useState("");
  const [email, setEmail] = useState("");
  const canSubmit = useMemo(() => Boolean(email && (file || githubUrl) && !(file && githubUrl)), [email, file, githubUrl]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData();
    formData.append("email", email);
    if (file) formData.append("resume_pdf", file);
    if (githubUrl) formData.append("github_url", githubUrl);
    await onSubmit(formData);
  }

  return (
    <form onSubmit={handleSubmit} className="grid gap-5 rounded-lg border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900 sm:p-6">
      <label className="grid gap-2 text-center">
        <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">Resume PDF</span>
        <span className="flex min-h-32 cursor-pointer flex-col items-center justify-center gap-3 rounded-md border border-dashed border-slate-300 bg-slate-50 px-4 text-center transition hover:border-teal-500 hover:bg-teal-50 dark:border-slate-700 dark:bg-slate-950 dark:hover:bg-slate-800">
          <span className="inline-flex h-11 w-11 items-center justify-center rounded-md bg-teal-100 text-teal-700 dark:bg-teal-500/15 dark:text-teal-300">
            <Upload size={22} />
          </span>
          <span className="max-w-full break-words text-sm font-medium text-slate-700 dark:text-slate-200">{file ? file.name : "Upload a resume PDF"}</span>
          <input
            className="sr-only"
            type="file"
            accept="application/pdf"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
            disabled={loading || Boolean(githubUrl)}
          />
        </span>
      </label>

      <div className="flex items-center gap-3">
        <span className="h-px flex-1 bg-slate-200 dark:bg-slate-800" />
        <span className="text-xs font-semibold uppercase text-slate-400">or</span>
        <span className="h-px flex-1 bg-slate-200 dark:bg-slate-800" />
      </div>

      <label className="grid gap-2 text-center">
        <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">GitHub resume URL</span>
        <span className="relative">
          <Link size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            value={githubUrl}
            onChange={(event) => setGithubUrl(event.target.value)}
            disabled={loading || Boolean(file)}
            placeholder="https://github.com/user/repo/blob/main/resume.pdf"
            className="w-full rounded-md border border-slate-300 bg-white py-3 pl-10 pr-3 text-center text-sm text-slate-900 outline-none transition placeholder:text-center focus:border-teal-500 focus:ring-2 focus:ring-teal-100 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:focus:ring-teal-900"
          />
        </span>
      </label>

      <label className="grid gap-2 text-center">
        <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">Email</span>
        <span className="relative">
          <Mail size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            type="email"
            placeholder="you@example.com"
            className="w-full rounded-md border border-slate-300 bg-white py-3 pl-10 pr-3 text-center text-sm text-slate-900 outline-none transition placeholder:text-center focus:border-teal-500 focus:ring-2 focus:ring-teal-100 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:focus:ring-teal-900"
          />
        </span>
      </label>

      <button
        type="submit"
        disabled={!canSubmit || loading}
        className="mt-1 inline-flex min-h-12 items-center justify-center gap-2 rounded-md bg-teal-700 px-5 text-sm font-semibold text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-teal-500 dark:text-slate-950 dark:hover:bg-teal-400"
      >
        {loading ? <span className="h-5 w-5 animate-spin rounded-full border-2 border-white/30 border-t-white" /> : <Send size={18} />}
        {loading ? "Processing" : "Find matched jobs"}
      </button>
    </form>
  );
}
