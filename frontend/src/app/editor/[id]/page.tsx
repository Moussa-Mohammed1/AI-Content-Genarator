"use client";
import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import ProtectedRoute from "@/components/ProtectedRoute";
import { contentApi, generationApi } from "@/lib/api";
import type { Content } from "@/types";
import {
  Save,
  RotateCcw,
  Sparkles,
  FileText,
  Loader2,
  Download,
  Copy,
} from "lucide-react";

export default function EditorPage(props: { params: Promise<{ id: string }> }) {
  const { id } = use(props.params);
  const router = useRouter();
  const [content, setContent] = useState<Content | null>(null);
  const [text, setText] = useState("");
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [aiLoading, setAiLoading] = useState<string | null>(null);
  const [selectionInfo, setSelectionInfo] = useState<{
    text: string;
    start: number;
    end: number;
  } | null>(null);

  useEffect(() => {
    contentApi
      .getById(id)
      .then((res) => {
        setContent(res.data);
        setText(res.data.generated_text || "");
        setTitle(res.data.title || "");
      })
      .catch(() => router.push("/contents"))
      .finally(() => setLoading(false));
  }, [id, router]);

  const handleSave = async () => {
    setSaving(true);
    try {
      const res = await contentApi.update(id, {
        title,
        generated_text: text,
        status: "completed",
      });
      setContent(res.data);
    } finally {
      setSaving(false);
    }
  };

  const handleSelect = () => {
    const textarea = document.getElementById("editor") as HTMLTextAreaElement;
    if (textarea.selectionStart !== textarea.selectionEnd) {
      setSelectionInfo({
        text: text.substring(textarea.selectionStart, textarea.selectionEnd),
        start: textarea.selectionStart,
        end: textarea.selectionEnd,
      });
    } else {
      setSelectionInfo(null);
    }
  };

  const applyAiAction = async (action: string, instruction?: string) => {
    const targetText = selectionInfo?.text || text;
    if (!targetText) return;

    setAiLoading(action);
    try {
      let result: string;
      switch (action) {
        case "rewrite":
          const r = await generationApi.rewrite({
            content_id: id,
            text: targetText,
            instruction: instruction || "Rewrite this text to be more engaging",
          });
          result = r.data.generated_text;
          break;
        case "summarize":
          const s = await generationApi.summarize({
            content_id: id,
            text: targetText,
          });
          result = s.data.generated_text;
          break;
        case "expand":
          const e = await generationApi.generate({
            prompt: `Expand this text with more details:\n\n${targetText}`,
          });
          result = e.data.generated_text;
          break;
        case "shorten":
          const sh = await generationApi.generate({
            prompt: `Shorten this text:\n\n${targetText}`,
          });
          result = sh.data.generated_text;
          break;
        default:
          return;
      }

      if (selectionInfo) {
        const newText =
          text.substring(0, selectionInfo.start) +
          result +
          text.substring(selectionInfo.end);
        setText(newText);
        setSelectionInfo(null);
      } else {
        setText(result);
      }
    } catch {
      alert("AI action failed. Please try again.");
    } finally {
      setAiLoading(null);
    }
  };

  const handleExport = async (format: string) => {
    switch (format) {
      case "copy":
        await navigator.clipboard.writeText(text);
        alert("Copied to clipboard!");
        break;
      case "txt":
        const blob = new Blob([text], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${title || "content"}.txt`;
        a.click();
        URL.revokeObjectURL(url);
        break;
      case "html":
        const htmlBlob = new Blob(
          [`<!DOCTYPE html><html><body>${text.replace(/\n/g, "<br>")}</body></html>`],
          { type: "text/html" }
        );
        const htmlUrl = URL.createObjectURL(htmlBlob);
        const htmlA = document.createElement("a");
        htmlA.href = htmlUrl;
        htmlA.download = `${title || "content"}.html`;
        htmlA.click();
        URL.revokeObjectURL(htmlUrl);
        break;
    }
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="flex items-center justify-center min-h-[60vh]">
          <Loader2 size={24} className="animate-spin text-indigo-600" />
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="text-2xl font-bold bg-transparent border-none outline-none focus:ring-0 w-full max-w-lg"
            placeholder="Untitled"
          />
          <div className="flex items-center gap-2">
            <button
              onClick={handleSave}
              disabled={saving}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              {saving ? (
                <Loader2 size={16} className="animate-spin" />
              ) : (
                <Save size={16} />
              )}
              Save
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-4 gap-6">
          <div className="md:col-span-3">
            <div className="bg-white rounded-xl border">
              <textarea
                id="editor"
                value={text}
                onChange={(e) => setText(e.target.value)}
                onSelect={handleSelect}
                onMouseUp={handleSelect}
                rows={25}
                className="w-full p-4 resize-none outline-none font-mono text-sm rounded-xl"
                placeholder="Start writing or generate content..."
              />
            </div>
          </div>

          <div className="space-y-4">
            <div className="bg-white rounded-xl border p-4">
              <h3 className="font-semibold text-sm mb-3">AI Tools</h3>
              <div className="space-y-2">
                {[
                  { label: "Rewrite", action: "rewrite" },
                  { label: "Summarize", action: "summarize" },
                  { label: "Expand", action: "expand" },
                  { label: "Shorten", action: "shorten" },
                ].map((tool) => (
                  <button
                    key={tool.action}
                    onClick={() => applyAiAction(tool.action)}
                    disabled={aiLoading !== null}
                    className="w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg border hover:bg-indigo-50 hover:border-indigo-300 transition disabled:opacity-50"
                  >
                    {aiLoading === tool.action ? (
                      <Loader2 size={14} className="animate-spin" />
                    ) : (
                      <Sparkles size={14} className="text-indigo-600" />
                    )}
                    {tool.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-xl border p-4">
              <h3 className="font-semibold text-sm mb-3">Export</h3>
              <div className="space-y-2">
                {[
                  { label: "Copy to Clipboard", format: "copy", icon: Copy },
                  { label: "Download TXT", format: "txt", icon: Download },
                  { label: "Download HTML", format: "html", icon: FileText },
                ].map((tool) => (
                  <button
                    key={tool.format}
                    onClick={() => handleExport(tool.format)}
                    className="w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg border hover:bg-gray-50 transition"
                  >
                    <tool.icon size={14} />
                    {tool.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
