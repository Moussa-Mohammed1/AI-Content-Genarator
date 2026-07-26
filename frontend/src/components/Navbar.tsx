"use client";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import {
  LayoutDashboard,
  FileText,
  Sparkles,
  History,
  User,
  LogOut,
} from "lucide-react";

export default function Navbar() {
  const { user, logout, loading } = useAuth();

  if (loading) return null;

  return (
    <nav className="border-b bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-8">
            <Link href="/" className="font-bold text-xl text-indigo-600">
              ContentAI
            </Link>
            {user && (
              <div className="hidden md:flex items-center gap-6">
                <Link
                  href="/dashboard"
                  className="flex items-center gap-2 text-sm text-gray-600 hover:text-indigo-600"
                >
                  <LayoutDashboard size={18} />
                  Dashboard
                </Link>
                <Link
                  href="/templates"
                  className="flex items-center gap-2 text-sm text-gray-600 hover:text-indigo-600"
                >
                  <FileText size={18} />
                  Templates
                </Link>
                <Link
                  href="/generate"
                  className="flex items-center gap-2 text-sm text-gray-600 hover:text-indigo-600"
                >
                  <Sparkles size={18} />
                  Generate
                </Link>
                <Link
                  href="/contents"
                  className="flex items-center gap-2 text-sm text-gray-600 hover:text-indigo-600"
                >
                  <History size={18} />
                  History
                </Link>
              </div>
            )}
          </div>
          <div className="flex items-center gap-4">
            {user ? (
              <>
                <span className="text-sm text-gray-500">
                  {user.credits} credits
                </span>
                <Link
                  href="/profile"
                  className="flex items-center gap-2 text-sm text-gray-600 hover:text-indigo-600"
                >
                  <User size={18} />
                  {user.name}
                </Link>
                <button
                  onClick={logout}
                  className="flex items-center gap-2 text-sm text-red-500 hover:text-red-700"
                >
                  <LogOut size={18} />
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="text-sm text-gray-600 hover:text-indigo-600"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className="text-sm bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
