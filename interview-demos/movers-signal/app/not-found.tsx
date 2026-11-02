import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto max-w-xl py-16 text-center">
      <p className="text-xs font-semibold uppercase tracking-wider text-muted">Not found</p>
      <h1 className="mt-2 text-3xl font-semibold text-ink">There is no page here</h1>
      <p className="mt-3 text-muted">The site only shows verified seats. A seat that was rejected at review has no page.</p>
      <Link href="/" className="mt-6 inline-block rounded-lg bg-pine px-4 py-2 font-medium text-on-pine no-underline">
        Back to the Radar
      </Link>
    </div>
  );
}
