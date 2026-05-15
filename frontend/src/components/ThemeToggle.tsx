import { Moon, Sun } from "lucide-react";

type Props = {
  darkMode: boolean;
  onToggle: () => void;
};

export function ThemeToggle({ darkMode, onToggle }: Props) {
  return (
    <button
      type="button"
      onClick={onToggle}
      className="inline-flex h-10 w-10 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-700 shadow-sm transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
      aria-label="Toggle dark mode"
      title="Toggle dark mode"
    >
      {darkMode ? <Sun size={18} /> : <Moon size={18} />}
    </button>
  );
}
