export type JobMatch = {
  company: string;
  role: string;
  location: string;
  salary: string;
  fit_score: number;
  category: string;
  apply_link: string;
  why_match: string;
};

export type AnalyzeResponse = {
  resume_id: string;
  google_sheet_url: string | null;
  excel_file: string;
  jobs: JobMatch[];
  analysis_summary: Record<string, unknown>;
};
