export interface User {
  id: string;
  name: string;
  email: string;
  subscription: string;
  credits: number;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export interface Template {
  id: string;
  name: string;
  description: string | null;
  category: string | null;
  prompt_template: string;
  icon: string | null;
  is_favorite: boolean;
  created_at: string;
}

export interface Content {
  id: string;
  user_id: string;
  template_id: string | null;
  title: string | null;
  prompt: string;
  generated_text: string | null;
  model_used: string | null;
  tone: string | null;
  audience: string | null;
  keywords: string | null;
  language: string | null;
  word_count: number | null;
  status: string;
  is_favorite: boolean;
  seo_title: string | null;
  seo_meta_description: string | null;
  seo_url_slug: string | null;
  seo_keywords: string | null;
  seo_headings: string | null;
  created_at: string;
  updated_at: string;
}

export interface GenerateRequest {
  template_id?: string;
  prompt: string;
  title?: string;
  tone?: string;
  audience?: string;
  keywords?: string;
  language?: string;
  word_count?: number;
}

export interface GenerateResponse {
  id: string;
  generated_text: string;
  model_used: string;
  tokens_used: number;
}

export interface UsageSummary {
  total_tokens: number;
  total_credits_used: number;
  total_generations: number;
  recent_usage: UsageRecord[];
}

export interface UsageRecord {
  id: string;
  user_id: string;
  tokens: number;
  credits_used: number;
  action: string | null;
  created_at: string;
}

export interface ContentStats {
  total: number;
  favorites: number;
  recent: Content[];
}
