const env = import.meta.env;

export const API_URL = (env.VITE_API_URL || "/api").replace(/\/+$/, "");
export const TOKEN_STORAGE_KEY = env.VITE_TOKEN_KEY || "alcla_access_token";
export const THEME_STORAGE_KEY = env.VITE_THEME_KEY || "alcla_dark_mode";
