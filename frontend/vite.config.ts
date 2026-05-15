import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    setupFiles: "./src/test/setup.ts"
  },
  server: {
    port: 5173,
    proxy: {
      "/analyze": "http://localhost:8000",
      "/health": "http://localhost:8000"
    }
  }
});
