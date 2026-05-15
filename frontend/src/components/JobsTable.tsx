import type { JobMatch } from "../types";

type Props = {
  jobs: JobMatch[];
};

export function JobsTable({ jobs }: Props) {
  if (!jobs.length) return null;

  return (
    <section className="mt-10">
      <div className="mb-4 flex flex-col gap-1 text-center sm:flex-row sm:items-end sm:justify-between sm:text-left">
        <div>
          <h2 className="text-2xl font-bold text-slate-950 dark:text-white">Top matched jobs</h2>
          <p className="text-sm text-slate-600 dark:text-slate-400">{jobs.length} ranked opportunities across India</p>
        </div>
      </div>
      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-left text-sm dark:divide-slate-800">
            <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500 dark:bg-slate-900 dark:text-slate-400">
              <tr>
                <th className="px-4 py-3">Company</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">Location</th>
                <th className="px-4 py-3">Score</th>
                <th className="px-4 py-3">Category</th>
                <th className="px-4 py-3">Why match</th>
                <th className="px-4 py-3">Apply</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {jobs.map((job) => (
                <tr key={`${job.company}-${job.role}-${job.apply_link}`} className="align-top">
                  <td className="px-4 py-4 font-semibold text-slate-950 dark:text-white">{job.company}</td>
                  <td className="px-4 py-4 text-slate-700 dark:text-slate-200">{job.role}</td>
                  <td className="px-4 py-4 text-slate-600 dark:text-slate-300">{job.location}</td>
                  <td className="px-4 py-4">
                    <span className="inline-flex min-w-14 justify-center rounded-md bg-teal-100 px-2 py-1 font-semibold text-teal-900 dark:bg-teal-500/20 dark:text-teal-200">
                      {job.fit_score}
                    </span>
                  </td>
                  <td className="px-4 py-4 text-slate-700 dark:text-slate-200">{job.category}</td>
                  <td className="max-w-md px-4 py-4 text-slate-600 dark:text-slate-300">{job.why_match}</td>
                  <td className="px-4 py-4">
                    <a className="font-semibold text-teal-700 hover:text-teal-900 dark:text-teal-300" href={job.apply_link} target="_blank" rel="noreferrer">
                      Open
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
