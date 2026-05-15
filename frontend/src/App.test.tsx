import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import App from "./App";

test("renders upload and GitHub URL inputs", () => {
  render(<App />);

  expect(screen.getByText("Upload a resume PDF")).toBeInTheDocument();
  expect(screen.getByPlaceholderText("https://github.com/user/repo/blob/main/resume.pdf")).toBeInTheDocument();
  expect(screen.getByPlaceholderText("you@example.com")).toBeInTheDocument();
});
