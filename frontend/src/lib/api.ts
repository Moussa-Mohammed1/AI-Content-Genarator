import axios from "axios";
import type {
  AuthResponse,
  User,
  Template,
  Content,
  GenerateRequest,
  GenerateResponse,
  UsageSummary,
  ContentStats,
} from "@/types";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        try {
          const res = await axios.post(
            `${api.defaults.baseURL}/auth/refresh`,
            { refresh_token: refreshToken }
          );
          localStorage.setItem("access_token", res.data.access_token);
          localStorage.setItem("refresh_token", res.data.refresh_token);
          originalRequest.headers.Authorization = `Bearer ${res.data.access_token}`;
          return api(originalRequest);
        } catch {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

// Auth
export const authApi = {
  register: (data: { name: string; email: string; password: string }) =>
    api.post<AuthResponse>("/auth/register", data),
  login: (data: { email: string; password: string }) =>
    api.post<AuthResponse>("/auth/login", data),
  refresh: (refresh_token: string) =>
    api.post<{ access_token: string; refresh_token: string }>("/auth/refresh", {
      refresh_token,
    }),
  logout: () => api.post("/auth/logout"),
};

// Templates
export const templateApi = {
  getAll: () =>
    api.get<{ templates: Template[]; total: number }>("/templates"),
  getById: (id: string) => api.get<Template>(`/templates/${id}`),
};

// Generation
export const generationApi = {
  generate: (data: GenerateRequest) =>
    api.post<GenerateResponse>("/generate", data),
  rewrite: (data: { content_id?: string; text: string; instruction: string }) =>
    api.post<{ generated_text: string; model_used: string }>("/generate/rewrite", data),
  summarize: (data: { content_id?: string; text: string }) =>
    api.post<{ generated_text: string; model_used: string }>("/generate/summarize", data),
  translate: (data: { content_id?: string; text: string; target_language: string }) =>
    api.post<{ generated_text: string; model_used: string }>("/generate/translate", data),
  seo: (data: { text: string; topic: string }) =>
    api.post<{
      seo_title: string;
      meta_description: string;
      url_slug: string;
      keywords: string;
      headings: string;
    }>("/generate/seo", data),
};

// Content
export const contentApi = {
  getAll: (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    status?: string;
    sort_by?: string;
    sort_order?: string;
  }) =>
    api.get<{ contents: Content[]; total: number; page: number; page_size: number }>(
      "/contents",
      { params }
    ),
  getById: (id: string) => api.get<Content>(`/contents/${id}`),
  update: (id: string, data: Partial<Content>) =>
    api.put<Content>(`/contents/${id}`, data),
  delete: (id: string) => api.delete(`/contents/${id}`),
  getStats: () => api.get<ContentStats>("/contents/stats/summary"),
};

// Profile
export const profileApi = {
  get: () => api.get<User>("/profile"),
  update: (data: { name?: string; email?: string }) =>
    api.put<User>("/profile", data),
};

// Usage
export const usageApi = {
  get: () => api.get<UsageSummary>("/usage"),
};

export default api;
