import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const backendUrl = (env.VITE_API_URL || "http://127.0.0.1:8000").replace(
    /\/+$/,
    "",
  );

  return {
    plugins: [react(), tailwindcss()],
    server: {
      proxy: {
        "/api": {
          target: backendUrl,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
  };
});
