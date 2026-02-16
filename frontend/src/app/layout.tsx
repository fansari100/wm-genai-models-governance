import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "WM GenAI Models & Governance",
  description: "5 Production GenAI Models + Governance System for WM Risk Model Control",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen">
          <nav className="border-b bg-white px-6 py-3 flex items-center gap-6">
            <a href="/" className="font-bold text-lg text-primary">WM GenAI Governance</a>
            <a href="/" className="text-sm text-gray-600 hover:text-primary">Dashboard</a>
            <a href="/models" className="text-sm text-gray-600 hover:text-primary">Models</a>
            <a href="/evaluations" className="text-sm text-gray-600 hover:text-primary">Evaluations</a>
            <a href="/compliance" className="text-sm text-gray-600 hover:text-primary">Compliance</a>
            <a href="/demo" className="text-sm text-gray-600 hover:text-primary">Live Demo</a>
          </nav>
          <main className="p-6 max-w-7xl mx-auto">{children}</main>
        </div>
      </body>
    </html>
  );
}
