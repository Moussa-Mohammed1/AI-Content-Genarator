"use client";
import { useState, useEffect, use } from "react";
import { useRouter } from "next/navigation";
import ProtectedRoute from "@/components/ProtectedRoute";
import { generationApi, templateApi } from "@/lib/api";
import type { Template } from "@/types";
import { Sparkles, Loader2 } from "lucide-react";

interface GenerateSearchParams {
  template?: string;
  template_id?: string;
}

export default function GeneratePage(props: {
  searchParams?: Promise<GenerateSearchParams>;
}) {
  const sp = use(props.searchParams ?? Promise.resolve({} as GenerateSearchParams));
  const router = useRouter();
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState(sp.template || sp.template_id || "");
  const [title, setTitle] = useState("");
  const [prompt, setPrompt] = useState("");
  const [tone, setTone] = useState("professional");
  const [audience, setAudience] = useState("general");
  const [keywords, setKeywords] = useState("");
  const [language, setLanguage] = useState("english");
  const [wordCount, setWordCount] = useState(500);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{
    generated_text: string;
    model_used: string;
  } | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    templateApi.getAll().then((res) => {
      setTemplates(res.data.templates);
      const templateParam = sp.template || sp.template_id;
      if (templateParam && !selectedTemplate) {
        const found = res.data.templates.find(
          (t) => t.name.toLowerCase().replace(/\s+/g, "_") === templateParam
        );
        if (found) setSelectedTemplate(found.name.toLowerCase().replace(/\s+/g, "_"));
      }
    });
  }, [sp.template, sp.template_id, selectedTemplate]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    setResult(null);
    try {
      const res = await generationApi.generate({
        template_id: selectedTemplate || undefined,
        prompt,
        title: title || undefined,
        tone,
        audience,
        keywords: keywords || undefined,
        language,
        word_count: wordCount,
      });
      setResult(res.data);
    } catch (err: unknown) {
      const msg =
        err && typeof err === "object" && "response" in err
          ? (err as { response: { data: { detail: string } } }).response?.data
              ?.detail
          : "Generation failed";
      setError(msg || "Generation failed");
    } finally {
      setLoading(false);
    }
  };

  const tones = ["professional", "casual", "friendly", "persuasive", "humorous", "formal", "empathetic"];
  const audiences = ["general", "beginners", "experts", "executives", "developers", "marketers"];

  return (
    <ProtectedRoute>
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-2">Generate Content</h1>
        <p className="text-gray-500 mb-8">
          Describe what you want to create and let AI do the work
        </p>

        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl border p-6">
            <form onSubmit={handleGenerate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Template (optional)</label>
                <select
                  value={selectedTemplate}
                  onChange={(e) => setSelectedTemplate(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                >
                  <option value="">Custom prompt</option>
                  {templates.map((t) => (
                    <option
                      key={t.id}
                      value={t.name.toLowerCase().replace(/\s+/g, "_")}
                    >
                      {t.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  placeholder="My Amazing Content"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Prompt *</label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  required
                  rows={5}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none resize-none"
                  placeholder="Describe what you want to create..."
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Tone</label>
                  <select
                    value={tone}
                    onChange={(e) => setTone(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  >
                    {tones.map((t) => (
                      <option key={t} value={t}>
                        {t.charAt(0).toUpperCase() + t.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Audience</label>
                  <select
                    value={audience}
                    onChange={(e) => setAudience(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  >
                    {audiences.map((a) => (
                      <option key={a} value={a}>
                        {a.charAt(0).toUpperCase() + a.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Keywords (comma separated)</label>
                <input
                  type="text"
                  value={keywords}
                  onChange={(e) => setKeywords(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  placeholder="keyword1, keyword2"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Language</label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  >
                    {["english", "spanish", "french", "german", "italian", "portuguese", "dutch", "japanese", "chinese", "korean"].map((l) => (
                      <option key={l} value={l}>
                        {l.charAt(0).toUpperCase() + l.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Word Count</label>
                  <input
                    type="number"
                    value={wordCount}
                    onChange={(e) => setWordCount(Number(e.target.value))}
                    min={100}
                    max={5000}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  />
                </div>
              </div>

              {error && (
                <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-indigo-600 text-white py-2 rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50 flex items-center justify-center gap-2 transition"
              >
                {loading ? (
                  <Loader2 size={18} className="animate-spin" />
                ) : (
                  <Sparkles size={18} />
                )}
                {loading ? "Generating..." : "Generate Content"}
              </button>
            </form>
          </div>

          <div className="bg-white rounded-xl border p-6">
            <h2 className="font-semibold mb-4">Generated Result</h2>
            {result ? (
              <div>
                <div className="prose prose-sm max-w-none whitespace-pre-wrap text-sm text-gray-700 mb-4">
                  {result.generated_text}
                </div>
                <div className="text-xs text-gray-400">
                  Model: {result.model_used}
                </div>
              </div>
            ) : (
              <div className="text-gray-400 text-sm text-center py-12">
                {loading ? (
                  <div className="flex items-center justify-center gap-2">
                    <Loader2 size={18} className="animate-spin" />
                    Generating...
                  </div>
                ) : (
                  "Your generated content will appear here"
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
