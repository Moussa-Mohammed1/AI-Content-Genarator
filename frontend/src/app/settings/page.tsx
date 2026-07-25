"use client";
import ProtectedRoute from "@/components/ProtectedRoute";
import { Settings as SettingsIcon, Bell, Shield, Palette } from "lucide-react";

export default function SettingsPage() {
  return (
    <ProtectedRoute>
      <div className="max-w-2xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-8">Settings</h1>
        <div className="bg-white rounded-xl border divide-y">
          {[
            {
              icon: Bell,
              title: "Notifications",
              desc: "Manage email and push notifications",
            },
            {
              icon: Shield,
              title: "Security",
              desc: "Password and authentication settings",
            },
            {
              icon: Palette,
              title: "Appearance",
              desc: "Customize your experience",
            },
            {
              icon: SettingsIcon,
              title: "API Keys",
              desc: "Manage your API keys for integrations",
            },
          ].map((section) => (
            <div
              key={section.title}
              className="flex items-center gap-4 p-4 hover:bg-gray-50 transition cursor-pointer"
            >
              <div className="w-10 h-10 rounded-lg bg-gray-100 text-gray-600 flex items-center justify-center">
                <section.icon size={20} />
              </div>
              <div>
                <div className="font-medium">{section.title}</div>
                <div className="text-sm text-gray-500">{section.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </ProtectedRoute>
  );
}
