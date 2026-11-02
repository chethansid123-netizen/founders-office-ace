import type { Metadata, Viewport } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { AS_OF, AUDIT, SEATS } from "@/lib/data";
import { formatDate } from "@/lib/format";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Movers Signal", template: "%s · Movers Signal" },
  description:
    "Leadership seats before the mandate: open and at-risk senior seats found in public NSE and BSE filings, ranked by a transparent priority rule.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#1c3a30" },
    { media: "(prefers-color-scheme: dark)", color: "#0f241d" },
  ],
};

function Mark() {
  return (
    <svg aria-hidden width="22" height="22" viewBox="0 0 22 22" className="shrink-0">
      <rect x="2" y="12" width="4" height="8" rx="1" fill="currentColor" opacity="0.55" />
      <rect x="9" y="7" width="4" height="13" rx="1" fill="currentColor" opacity="0.8" />
      <rect x="16" y="2" width="4" height="18" rx="1" fill="currentColor" />
    </svg>
  );
}

const NAV = [
  { href: "/", label: "Radar" },
  { href: "/pulse/", label: "Market pulse" },
  { href: "/method/", label: "Method" },
];

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en-IN">
      <body className="min-h-screen antialiased">
        <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded focus:bg-surface focus:px-3 focus:py-2">
          Skip to content
        </a>
        <header className="bg-pine text-on-pine">
          <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-6 gap-y-2 px-4 py-3 sm:px-6">
            <Link href="/" className="flex items-center gap-2 no-underline">
              <Mark />
              <span className="font-serif text-lg font-semibold tracking-tight">Movers Signal</span>
            </Link>
            <nav aria-label="Main" className="flex flex-wrap gap-x-5 gap-y-1 text-sm">
              {NAV.map((n) => (
                <Link key={n.href} href={n.href} className="opacity-85 no-underline hover:opacity-100 hover:underline hover:underline-offset-4">
                  {n.label}
                </Link>
              ))}
            </nav>
            <span className="ml-auto text-xs opacity-75">Data as of {formatDate(AS_OF)}</span>
          </div>
        </header>
        <main id="main" className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10">
          {children}
        </main>
        <footer className="border-t border-line">
          <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-6 text-sm text-muted sm:px-6">
            <p className="font-medium text-ink">Independent prototype built from public filings. Not affiliated with Positive Moves.</p>
            <p>
              <span data-metric="footer-seats">{SEATS.length}</span> verified seats from{" "}
              <span data-metric="footer-filings">{new Set(SEATS.map((s) => s.source_url)).size}</span> NSE and BSE filings dated{" "}
              {formatDate(AUDIT.window[0])} to {formatDate(AUDIT.window[1])}. Priority is a transparent rule, not a probability.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
