"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import ProtectedRoute from "@/components/ProtectedRoute";
import { templateApi } from "@/lib/api";
import type { Template } from "@/types";
import {
  FileText,
  Package,
  Mail,
  Share2,
  Layout,
  Search,
  HelpCircle,
  Video,
  Newspaper,
  Globe,
  MessageSquare,
} from "lucide-react";

const iconMap: Record<string, React.ElementType> = {
  FileText,
  Package,
  Mail,
  Share2,
  Layout,
  Search,
  HelpCircle,
  Video,
  Newspaper,
  Globe,
  MessageSquare,
};

export default function TemplatesPage() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");

  useEffect(() => {
    templateApi.getAll().then((res) => setTemplates(res.data.templates));
  }, []);

  const categories: string[] = [
    "all",
    ...new Set(templates.map((t) => t.category).filter((c): c is string => !!c)),
  ];

  const filtered = templates.filter((t) => {
    const matchesSearch =
      t.name.toLowerCase().includes(search.toLowerCase()) ||
      t.description?.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = category === "all" || t.category === category;
    return matchesSearch && matchesCategory;
  });

  return (
    <ProtectedRoute>
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold">Content Templates</h1>
          <p className="text-gray-500">
            Choose a template to start generating content
          </p>
        </div>

        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <input
            type="text"
            placeholder="Search templates..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
          />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((template) => {
            const Icon =
              iconMap[template.icon || "FileText"] || FileText;
            return (
              <Link
                key={template.id}
                href={`/generate?template=${template.name.toLowerCase().replace(/\s+/g, "_")}`}
                className="bg-white rounded-xl border p-6 hover:shadow-md hover:border-indigo-300 transition group"
              >
                <div className="w-10 h-10 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center mb-3 group-hover:bg-indigo-100 transition">
                  <Icon size={20} />
                </div>
                <h3 className="font-semibold mb-1">{template.name}</h3>
                <p className="text-sm text-gray-500">
                  {template.description}
                </p>
              </Link>
            );
          })}
        </div>
      </div>
    </ProtectedRoute>
  );
}
