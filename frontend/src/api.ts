import type { AnalyzeResponse } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export async function analyzeResume(formData: FormData): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail ?? "Resume analysis failed.");
  }

  return response.json();
}
