"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import ProtectedRoute from "@/components/ProtectedRoute";
import { useAuth } from "@/lib/auth-context";
import { contentApi, usageApi, templateApi } from "@/lib/api";
import type { Content, Template } from "@/types";
import {
  FileText,
  Sparkles,
  History,
  TrendingUp,
  Star,
  ArrowRight,
} from "lucide-react";

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState<{
    total: number;
    favorites: number;
    recent: Content[];
  } | null>(null);
  const [usage, setUsage] = useState<{
    total_tokens: number;
    total_generations: number;
  } | null>(null);
  const [templates, setTemplates] = useState<Template[]>([]);

  useEffect(() => {
    contentApi.getStats().then((res) => setStats(res.data));
    usageApi.get().then((res) =>
      setUsage({
        total_tokens: res.data.total_tokens,
        total_generations: res.data.total_generations,
      })
    );
    templateApi.getAll().then((res) => setTemplates(res.data.templates));
  }, []);

  return (
    <ProtectedRoute>
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold">
            Welcome back, {user?.name}
          </h1>
          <p className="text-gray-500">Here&apos;s your content overview</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          {[
            {
              label: "Total Content",
              value: stats?.total ?? 0,
              icon: FileText,
              color: "text-blue-600 bg-blue-50",
            },
            {
              label: "Generations",
              value: usage?.total_generations ?? 0,
              icon: Sparkles,
              color: "text-purple-600 bg-purple-50",
            },
            {
              label: "Credits Remaining",
              value: user?.credits ?? 0,
              icon: TrendingUp,
              color: "text-green-600 bg-green-50",
            },
            {
              label: "Favorites",
              value: stats?.favorites ?? 0,
              icon: Star,
              color: "text-yellow-600 bg-yellow-50",
            },
          ].map((card) => (
            <div
              key={card.label}
              className="bg-white rounded-xl p-6 border shadow-sm"
            >
              <div
                className={`w-10 h-10 rounded-lg ${card.color} flex items-center justify-center mb-3`}
              >
                <card.icon size={20} />
              </div>
              <div className="text-2xl font-bold">{card.value}</div>
              <div className="text-sm text-gray-500">{card.label}</div>
            </div>
          ))}
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl border shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-lg">Recent Content</h2>
              <Link
                href="/contents"
                className="text-sm text-indigo-600 flex items-center gap-1"
              >
                View all <ArrowRight size={14} />
              </Link>
            </div>
            {stats?.recent?.length ? (
              <div className="space-y-3">
                {stats.recent.slice(0, 5).map((c) => (
                  <Link
                    key={c.id}
                    href={`/editor/${c.id}`}
                    className="block p-3 rounded-lg hover:bg-gray-50 transition border"
                  >
                    <div className="font-medium text-sm truncate">
                      {c.title || "Untitled"}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {new Date(c.created_at).toLocaleDateString()}
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-gray-400 text-sm py-8 text-center">
                No content yet. Generate your first piece!
              </p>
            )}
          </div>

          <div className="bg-white rounded-xl border shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-lg">Quick Templates</h2>
              <Link
                href="/templates"
                className="text-sm text-indigo-600 flex items-center gap-1"
              >
                Browse all <ArrowRight size={14} />
              </Link>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {templates.slice(0, 6).map((t) => (
                <Link
                  key={t.id}
                  href={`/generate?template=${t.name.toLowerCase().replace(/\s+/g, "_")}`}
                  className="p-3 rounded-lg border hover:border-indigo-300 hover:bg-indigo-50 transition text-center"
                >
                  <div className="text-sm font-medium">{t.name}</div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
