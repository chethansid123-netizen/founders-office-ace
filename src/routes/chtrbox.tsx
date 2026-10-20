import { createFileRoute } from "@tanstack/react-router";

// The Creator Intelligence Engine is a self-contained page in public/chtrbox; this route frames it full screen.
export const Route = createFileRoute("/chtrbox")({
  head: () => ({
    meta: [
      { title: "Creator Intelligence Engine · Chtrbox prototype" },
      { name: "description", content: "AI creator matching, forecasting and verified-ROI analytics: a prototype for Chtrbox by Chethan N." },
    ],
  }),
  component: ChtrboxPage,
});

function ChtrboxPage() {
  return (
    <div className="fixed inset-0 flex flex-col bg-background">
      <div className="flex items-center justify-between gap-4 border-b border-border px-4 py-2 font-mono text-xs uppercase tracking-wider">
        <a href="/" className="hover:opacity-60">← Chethan.N</a>
        <div className="flex gap-4">
          <a href="/chtrbox/GTM-Plan.pdf" target="_blank" rel="noreferrer" className="hover:opacity-60">GTM plan (PDF)</a>
          <a href="/chtrbox/index.html" target="_blank" rel="noreferrer" className="hover:opacity-60">Open full window ↗</a>
        </div>
      </div>
      <iframe src="/chtrbox/index.html" title="Creator Intelligence Engine" className="w-full flex-1 border-0" allow="fullscreen; clipboard-write" />
    </div>
  );
}
