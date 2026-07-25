"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import ProtectedRoute from "@/components/ProtectedRoute";
import { contentApi } from "@/lib/api";
import type { Content } from "@/types";
import {
  Search,
  Trash2,
  Star,
  Edit3,
  Loader2,
  FileText,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

export default function ContentsPage() {
  const [contents, setContents] = useState<Content[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const pageSize = 20;

  const fetchContents = async () => {
    setLoading(true);
    try {
      const res = await contentApi.getAll({
        page,
        page_size: pageSize,
        search: search || undefined,
        status: status || undefined,
      });
      setContents(res.data.contents);
      setTotal(res.data.total);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchContents();
  }, [page, status]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    fetchContents();
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this content?")) return;
    await contentApi.delete(id);
    fetchContents();
  };

  const toggleFavorite = async (content: Content) => {
    await contentApi.update(content.id, {
      is_favorite: !content.is_favorite,
    });
    fetchContents();
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <ProtectedRoute>
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold">Content History</h1>
            <p className="text-gray-500">{total} total pieces</p>
          </div>
          <Link
            href="/generate"
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            New Content
          </Link>
        </div>

        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <form onSubmit={handleSearch} className="flex-1 flex gap-2">
            <input
              type="text"
              placeholder="Search content..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              <Search size={18} />
            </button>
          </form>
          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setPage(1);
            }}
            className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
          >
            <option value="">All status</option>
            <option value="draft">Draft</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 size={24} className="animate-spin text-indigo-600" />
          </div>
        ) : contents.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <FileText size={48} className="mx-auto mb-4 opacity-50" />
            <p>No content found</p>
          </div>
        ) : (
          <div className="bg-white rounded-xl border overflow-hidden">
            {contents.map((content) => (
              <div
                key={content.id}
                className="flex items-center justify-between p-4 border-b last:border-b-0 hover:bg-gray-50 transition"
              >
                <Link
                  href={`/editor/${content.id}`}
                  className="flex-1 min-w-0"
                >
                  <div className="font-medium truncate">
                    {content.title || "Untitled"}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {new Date(content.created_at).toLocaleDateString()} ·{" "}
                    {content.model_used || "N/A"} ·{" "}
                    {content.word_count || 0} words
                  </div>
                </Link>
                <div className="flex items-center gap-2 ml-4">
                  <button
                    onClick={() => toggleFavorite(content)}
                    className={`p-2 rounded-lg hover:bg-gray-100 ${
                      content.is_favorite
                        ? "text-yellow-500"
                        : "text-gray-400"
                    }`}
                  >
                    <Star size={16} fill={content.is_favorite ? "currentColor" : "none"} />
                  </button>
                  <Link
                    href={`/editor/${content.id}`}
                    className="p-2 rounded-lg text-gray-400 hover:bg-gray-100"
                  >
                    <Edit3 size={16} />
                  </Link>
                  <button
                    onClick={() => handleDelete(content.id)}
                    className="p-2 rounded-lg text-red-400 hover:bg-red-50"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {totalPages > 1 && (
          <div className="flex items-center justify-center gap-4 mt-6">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 rounded-lg border hover:bg-gray-50 disabled:opacity-50"
            >
              <ChevronLeft size={18} />
            </button>
            <span className="text-sm text-gray-500">
              Page {page} of {totalPages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="p-2 rounded-lg border hover:bg-gray-50 disabled:opacity-50"
            >
              <ChevronRight size={18} />
            </button>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
